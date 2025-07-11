from .user import router as user_rout
from .auth import router as auth_rout
from .technologies import router as project_technologies_rout
from .this_comand import router as this_command_rout
from .activities import router as activities_rout
from .moder_activities import router as moder_activities
from .personal_detail import router as personal_detail_rout
from .favorites import router as favorites_rout
from .recommendations import router as recommendations_rout

from fastapi import APIRouter

router = APIRouter()

router.include_router(user_rout)

router.include_router(auth_rout, prefix="/auth")

router.include_router(project_technologies_rout, prefix='/project_technologies')

router.include_router(this_command_rout, prefix='/this_command')

router.include_router(activities_rout, prefix='/activities')

router.include_router(moder_activities, prefix='/moder')

router.include_router(personal_detail_rout, prefix='/profile')

router.include_router(favorites_rout, prefix='/favorites')

router.include_router(recommendations_rout, prefix='/recommendations')
