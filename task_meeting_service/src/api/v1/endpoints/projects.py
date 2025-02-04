from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from src.services.crud.project_service import ProjectService
from src.database.db import db_manager
from src.schemas.api.project import ProjectCreateSchema, ProjectUpdateSchema

router = APIRouter()


@router.post("/projects/")
async def create_project(project: ProjectCreateSchema):
    project_service = ProjectService(db_manager)
    data = await project_service.create_project(project)
    return JSONResponse(
        content={
            "new_project": data["project_oid"],
        }
    )


@router.get("/projects/{oid}/")
async def get_project(oid: str):
    project_service = ProjectService(db_manager)
    project = await project_service.get_project_by_oid(oid)
    return JSONResponse(content=project)


@router.put("/projects/{project_id}/")
async def update_project(project_id: int, project: ProjectUpdateSchema):
    project_service = ProjectService(db_manager)
    await project_service.update_project(project_id, project.dict())
    return JSONResponse(content={"message": "Project updated successfully"})
