from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import enum

class UserRole(str, enum.Enum):
    user = "user"
    chef_verified = "chef_verified"
    admin = "admin"

class VerificationStatus(str, enum.Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    bio = Column(Text, default="")
    profile_image = Column(String, nullable=True)
    role = Column(Enum(UserRole), default=UserRole.user, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relação com solicitações de verificação
    verification_requests = relationship(
        "ChefVerificationRequest",
        back_populates="user",
        foreign_keys="[ChefVerificationRequest.user_id]"
    )
    
    # Relação com receitas
    recipes = relationship("Recipe", back_populates="author")
    
    # Relação com comentários
    comments = relationship("Comment", back_populates="user")


class ChefVerificationRequest(Base):
    __tablename__ = "chef_verification_requests"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    justification = Column(Text, nullable=True)
    document_path = Column(String, nullable=True)  # Pode ser caminho para upload
    status = Column(Enum(VerificationStatus), default=VerificationStatus.pending, nullable=False)
    admin_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # Admin que avaliou
    admin_reason = Column(Text, nullable=True)  # Motivo da recusa, se houver
    reviewed_at = Column(DateTime(timezone=True), nullable=True)
    requested_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship(
        "User",
        foreign_keys=[user_id],
        back_populates="verification_requests"
    )
    admin = relationship(
        "User",
        foreign_keys=[admin_id]
    )


class Recipe(Base):
    __tablename__ = "recipes"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    ingredients = Column(Text, nullable=False)
    preparation = Column(Text, nullable=False)
    preparation_time_minutes = Column(Integer, nullable=True)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    author = relationship("User", back_populates="recipes")
    comments = relationship("Comment", back_populates="recipe")
    favorites = relationship("FavoriteRecipe", back_populates="recipe")


class Comment(Base):
    __tablename__ = "comments"
    
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User", back_populates="comments")
    recipe = relationship("Recipe", back_populates="comments")


class FavoriteRecipe(Base):
    __tablename__ = "favorite_recipes"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User")
    recipe = relationship("Recipe", back_populates="favorites")
