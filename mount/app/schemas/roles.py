from pydantic import BaseModel


class RoleResponse(BaseModel):
	role: str

	class Config:
		form_attributes = True
