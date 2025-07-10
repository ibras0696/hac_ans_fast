from .user import router as user_rout
from .auth import router as auth_rout
from .technologies import router as project_technologies_rout
from .this_comand import router as this_command_rout
from .activities import router as activities_rout
from .moder_activities import router as moder_activities

from fastapi import APIRouter

router = APIRouter()

router.include_router(user_rout)

router.include_router(auth_rout, prefix="/auth")

router.include_router(project_technologies_rout, prefix='/project_technologies')

router.include_router(this_command_rout, prefix='/this_command')

router.include_router(activities_rout, prefix='/activities')

router.include_router(moder_activities, prefix='/moder')
