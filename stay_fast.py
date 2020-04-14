from sanic import response
from enum import Enum
from datetime import timedelta, datetime
import dataclasses


class RequestBucket(Enum):
    GLOBAL = 0
    IP = 1
    TOKEN = 2


@dataclasses.dataclass()
class CachedData:
    data: str
    timestamp: datetime = dataclasses.field(default_factory=datetime.utcnow)


class cache_response:
    def __init__(self, level=RequestBucket.GLOBAL, **td_options):
        self.level = level
        self.td = timedelta(**td_options)
        self.cache = {}

    def get_cache_key(self, request):
        if self.level == RequestBucket.GLOBAL:
            return "global"

        elif self.level == RequestBucket.IP:
            return request.remote_addr or request.ip

        elif self.level == RequestBucket.TOKEN:
            return request.headers.get("Authorization")

    def set_data(self, request, data):
        key = self.get_cache_key(request)
        self.cache[key] = CachedData(data)

    def get_data(self, request):
        key = self.get_cache_key(request)

        cached = self.cache.get(key)
        if cached is None:
            # Cache has expired; ignore
            return None

        if (datetime.utcnow() - cached.timestamp) > self.td:
            return None

        return cached.data

    def __call__(self, handler):
        async def wrapper(request, *args, **kwargs):
            cached = self.get_data(request)
            if cached is not None:
                return cached

            new = await handler(request, *args, **kwargs)
            self.set_data(request, new)
            return new

        return wrapper


@dataclasses.dataclass()
class RatelimitCounter:
    counter: int = 1
    last: datetime = dataclasses.field(default_factory=datetime.utcnow)


class ratelimit:
    def __init__(self, level=RequestBucket.IP, limit=1, **per_td):
        self.level = level
        self.limit = limit
        self.per = timedelta(**per_td)

        self.limits = {}

    def get_limit_key(self, request):
        if self.level == RequestBucket.GLOBAL:
            return "global"

        elif self.level == RequestBucket.IP:
            return request.remote_addr or request.ip

        elif self.level == RequestBucket.TOKEN:
            return request.headers.get("Authorization")

    def check_limit(self, request):
        key = self.get_limit_key(request)
        limit = self.limits.get(key)
        if limit is None:
            self.limits[key] = RatelimitCounter()
            return True

        if (datetime.utcnow() - limit.last) > self.per:
            # Limit has expired; reset
            limit.counter = 0

        if limit.counter >= self.limit:
            # Limit exceeded
            return False

        limit.counter += 1
        limit.last = datetime.utcnow()
        return True

    def __call__(self, handler):
        async def wrapper(request, *args, **kwargs):
            if not self.check_limit(request):
                return response.json({
                    "error": "You got ratelimited",
                    "retry_after": self.per.total_seconds() * 1000
                }, status=429)

            return await handler(request, *args, **kwargs)

        return wrapper
