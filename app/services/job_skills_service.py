from app.repositories.job_skills import JobSkillRepository
from app.schemas.job_skill import (
    JobSkillDetailResponse,
    JobSkillListResponse,
    JobSkillResponse,
    JobSkillSchema,
)
from fastapi import HTTPException, UploadFile
import pandas as pd
import io


class JobSkillService:
    def __init__(self):
        self.repository = JobSkillRepository()

    async def get_job_skills(self) -> JobSkillListResponse:
        documents = await self.repository.get_job_skills()
        return {
            "success": True,
            "data": documents,
            "message": "Job skills retrieved successfully",
        }

    async def get_job_skill_by_id(self, job_skill_id) -> JobSkillDetailResponse:
        document = await self.repository.get_job_skill_by_id(job_skill_id)
        return {
            "success": True,
            "data": document,
            "message": "Job skill retrieved successfully",
        }

    async def create_job_skill(self, job_skill: JobSkillSchema):
        await self.repository.create_job_skill(job_skill)
        return {"success": True, "message": "Job skill created successfully"}

    async def update_job_skill(self, job_skill_id, job_skill: JobSkillSchema):
        await self.repository.update_job_skill(job_skill_id, job_skill)
        return {"success": True, "message": "Job skill updated successfully"}

    async def delete_job_skill(self, job_skill_id: JobSkillSchema):
        await self.repository.delete_job_skill(job_skill_id)
        return {"success": True, "message": "Job skill deleted successfully"}
    
    async def bulk_upload_job_skills(self, file: UploadFile):
        try:
            if not (file.filename.endswith(".csv") or file.filename.endswith(".xlsx")):
                raise HTTPException(status_code=400, detail="Only CSV or XLSX files are supported.")

            # Read file contents
            content = await file.read()
            try:
                if file.filename.endswith(".csv"):
                    df = pd.read_csv(io.BytesIO(content))
                else:
                    df = pd.read_excel(io.BytesIO(content))
            except Exception:
                raise HTTPException(status_code=400, detail="Error reading file content.")

            # Validate 'Name' column
            if "Name" not in df.columns:
                raise HTTPException(status_code=400, detail="File must contain a 'Name' column.")

            # Clean and get unique names
            names = df["Name"].dropna().astype(str).str.strip().unique().tolist()

            # Check existing skills
            existing = await self.repository.get_existing_skill_names(names)
            existing_names = {doc["name"] for doc in existing}

            # Filter out already existing
            new_names = [name for name in names if name not in existing_names]

            if not new_names:
                return {"message": "All skills already exist. No new entries added."}

            # Insert new ones
            await self.repository.bulk_create_job_skills([JobSkillSchema(name=name) for name in new_names])

            return {
                "message": f"Added {len(new_names)} new skills successfully.",
                "added_skills": new_names,
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
