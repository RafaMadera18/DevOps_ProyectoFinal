import logging
import time
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)

class APILoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.start_time = time.time()

    def process_response(self, request, response):
        duration = time.time() - getattr(request, 'start_time', time.time())
        log_data = {
            "method": request.method,
            "path": request.get_full_path(),
            "status": response.status_code,
            "duration": round(duration * 1000, 2),  # ms
        }
        if request.method in ['POST', 'PUT', 'PATCH']:
            log_data["body"] = getattr(request, 'body', b'').decode('utf-8')[:500]

        level = logging.INFO
        if 400 <= response.status_code < 500:
            level = logging.WARNING
        elif response.status_code >= 500:
            level = logging.ERROR

        logger.log(level, json.dumps(log_data))
        return response
