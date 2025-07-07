from pydantic import BaseModel, EmailStr
from typing import Optional, List
from enum import Enum
from datetime import datetime

class Token(BaseModel):
    access_token: str
    token_type: str

# Enums compatíveis com os models
class UserRole(str, Enum):
    user = "user"
    chef_verified = "chef_verified"
    admin = "admin"

class VerificationStatus(str, Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"


# ========== USER ==========
class UserBase(BaseModel):
    full_name: str
    email: EmailStr
    bio: Optional[str] = None
    role: UserRole = UserRole.user
    profile_image: Optional[str] = None

class UserCreate(UserBase):
    password: str  # senha em texto plano recebida via API

class UserUpdate(BaseModel):
    full_name: Optional[str]
    email: Optional[EmailStr]
    bio: Optional[str]
    profile_image: Optional[str]
    password: Optional[str]

class UserOut(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


# ========== RECIPE ==========
class RecipeBase(BaseModel):
    title: str
    ingredients: str
    preparation: str
    preparation_time_minutes: Optional[int] = None

class RecipeCreate(RecipeBase):
    pass

class RecipeOut(RecipeBase):
    id: int
    author_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ========== COMMENT ==========
class CommentBase(BaseModel):
    content: str

class CommentCreate(CommentBase):
    recipe_id: int

class CommentOut(CommentBase):
    id: int
    user_id: int
    recipe_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ========== FAVORITE ==========
class FavoriteRecipeCreate(BaseModel):
    recipe_id: int

class FavoriteRecipeOut(BaseModel):
    id: int
    user_id: int
    recipe_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ========== CHEF VERIFICATION ==========
class ChefVerificationRequestBase(BaseModel):
    justification: Optional[str]
    document_path: Optional[str]

class ChefVerificationRequestCreate(ChefVerificationRequestBase):
    pass

class ChefVerificationRequestOut(ChefVerificationRequestBase):
    id: int
    user_id: int
    status: VerificationStatus
    admin_id: Optional[int]
    admin_reason: Optional[str]
    requested_at: datetime
    reviewed_at: Optional[datetime]

    class Config:
        from_attributes = True

class VerificationStatus(str, Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"