from typing import Optional

from pydantic import BaseModel


class TokenData(BaseModel):
	token_type: str
	id: int
	username: Optional[str] = None
	email: Optional[str] = None
	full_name: Optional[str] = None
	photo: Optional[str] = None
	role: Optional[str] = None
