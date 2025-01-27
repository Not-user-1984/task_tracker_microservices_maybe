from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from src.services.crud.project_service import ProjectService
from src.database.db import DatabaseSessionManager
from src.schemas.api.project import ProjectCreateSchema, ProjectUpdateSchema

router = APIRouter()

db_manager = DatabaseSessionManager()


@router.post("/projects/")
async def create_project(project: ProjectCreateSchema):
    project_service = ProjectService(db_manager)
    project_id = await project_service.create_project(project.dict())
    return JSONResponse(content={"project_id": project_id})


@router.get("/projects/{project_id}/")
async def get_project(project_id: int):
    project_service = ProjectService(db_manager)
    project = await project_service.get_project_by_id(project_id)
    return JSONResponse(content=project)


@router.put("/projects/{project_id}/")
async def update_project(project_id: int, project: ProjectUpdateSchema):
    project_service = ProjectService(db_manager)
    await project_service.update_project(project_id, project.dict())
    return JSONResponse(content={"message": "Project updated successfully"})
