from app.schemas import UserCreate, UserRole
import pytest


def test_user_create_valid():
    user = UserCreate(
        full_name="Maria Oliveira",
        email="maria@example.com",
        password="senha123",
        bio="Chef amadora",
        role=UserRole.user
    )
    assert user.email == "maria@example.com"
    assert user.role == UserRole.user


def test_user_create_invalid_email():
    with pytest.raises(ValueError):
        UserCreate(
            full_name="Erro",
            email="email-invalido",
            password="123456"
        )


def test_enum_role():
    user = UserCreate(
        full_name="João",
        email="joao@example.com",
        password="1234",
        role="chef_verified"
    )
    assert user.role == UserRole.chef_verified
