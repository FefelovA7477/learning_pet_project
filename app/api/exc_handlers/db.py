from fastapi import Request, Response, status
from fastapi.responses import JSONResponse
from typing import List, Callable, Tuple
from sqlalchemy.exc import NoResultFound, IntegrityError, SQLAlchemyError


async def no_result_found_handler(request: Request, exc: NoResultFound) -> Response:
    return JSONResponse(content={'details': 'No result found'}, 
                        status_code=status.HTTP_404_NOT_FOUND)


async def integrity_error_handler(request: Request, exc: IntegrityError) -> Response:
    print(exc)
    return JSONResponse(content={'details': 'Integrity error: duplicate or invalid data.'},
                        status_code=status.HTTP_400_BAD_REQUEST)


db_exc_handlers: List[Tuple[SQLAlchemyError, Callable[[Request, SQLAlchemyError], Response]]] = [
    (IntegrityError, integrity_error_handler),
    (NoResultFound, no_result_found_handler)
]