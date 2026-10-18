from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from fastapi.security import HTTPAuthorizationCredentials

from shared.security import validar_token

security = HTTPBearer()



def usuario_logado(
    credenciais: HTTPAuthorizationCredentials = Depends(security)
):

    token = credenciais.credentials

    payload = validar_token(token)

    if not payload:
        raise HTTPException(
            status_code=401,
            detail="Token inválido"
        )

    return payload