import logging
import json
import time

logger = logging.getLogger(__name__)


class UserActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()

        response = self.get_response(request)

        duration_ms = round((time.time() - start_time) * 1000, 2)

        username = (
            request.user.username
            if request.user.is_authenticated
            else "anonymous"
        )

        log_data = {
            "event": "request_finished",
            "user": username,
            "method": request.method,
            "path": request.path,
            "status_code": response.status_code,
            "duration_ms": duration_ms,
        }

        logger.info(json.dumps(log_data, ensure_ascii=False))

        return response