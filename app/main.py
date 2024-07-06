from fastapi import FastAPI, Depends

from api.routers import routers
from api.dependencies.tg import tg_verify_signature
from api.exc_handlers import db_exc_handlers
# from api.middleware.log import log_into_server_logger

app = FastAPI(dependencies=[Depends(tg_verify_signature)])

for router in routers:
    app.include_router(router)

for exc_handler in db_exc_handlers:
    app.add_exception_handler(*exc_handler)

# app.middleware('http')(log_into_server_logger)