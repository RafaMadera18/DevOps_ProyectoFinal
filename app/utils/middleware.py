import logging
import time
import json
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)

class APILoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.start_time = time.time()
        # Leer el cuerpo una vez y guardarlo en una variable personalizada
        try:
            request._cached_body = request.body
        except Exception:
            request._cached_body = b''

    def process_response(self, request, response):
        duration = time.time() - getattr(request, 'start_time', time.time())
        log_data = {
            "method": request.method,
            "path": request.get_full_path(),
            "status": response.status_code,
            "duration": round(duration * 1000, 2),  # en milisegundos
        }

        if request.method in ['POST', 'PUT', 'PATCH']:
            try:
                body = getattr(request, '_cached_body', b'').decode('utf-8')[:500]
                log_data["body"] = body
            except Exception:
                log_data["body"] = "[Unable to decode body]"

        level = logging.INFO
        if 400 <= response.status_code < 500:
            level = logging.WARNING
        elif response.status_code >= 500:
            level = logging.ERROR

        logger.log(level, json.dumps(log_data))
        return response
