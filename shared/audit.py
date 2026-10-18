import time
import uuid

from fastapi import Request
from fastapi.security import HTTPBearer
from starlette.middleware.base import BaseHTTPMiddleware
from shared.logger import logger

security = HTTPBearer(
    bearerFormat="JWT"
)

class AuditMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        request_id = str(uuid.uuid4())
        inicio = time.time()

        ip = request.client.host if request.client else "desconhecido"

        try:
            response = await call_next(request)

            tempo_ms = round((time.time() - inicio) * 1000, 2)

            logger.info(
                f"[{request_id}] "
                f"METODO={request.method} "
                f"PATH={request.url.path} "
                f"QUERY={request.url.query} "
                f"IP={ip} "
                f"STATUS={response.status_code} "
                f"TEMPO={tempo_ms}ms "
                f"USER_AGENT={request.headers.get('user-agent')}"
            )

            return response

        except Exception as e:

            tempo_ms = round((time.time() - inicio) * 1000, 2)

            logger.exception(
                f"[{request_id}] "
                f"ERRO={str(e)} "
                f"METODO={request.method} "
                f"PATH={request.url.path} "
                f"IP={ip} "
                f"TEMPO={tempo_ms}ms"
            )

            raise


