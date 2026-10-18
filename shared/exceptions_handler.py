from shared.exceptions import NotFound
from fastapi import  Request
from fastapi.responses import JSONResponse


async def  not_found_exception_handler(request: Request, exc: NotFound):
    return JSONResponse(status_code=404, content={"Mensagem": f"Item não encontrato: {exc.name}"})