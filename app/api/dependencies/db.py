from fastapi import Depends
from typing import Annotated

from services.uow.usertasks import UserTaskUOW, BaseUOW


UowDependency = Annotated[BaseUOW, Depends(UserTaskUOW)]