from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
from app import schemas, models
from app.core.database import get_db
from app.core.auth import get_current_user
from sqlalchemy.sql import func
from datetime import datetime
import os

router = APIRouter()

# Usuário solicita verificação (agora permite múltiplas)
@router.post("/", response_model=schemas.ChefVerificationRequestOut)
def request_verification(
    justification: str = Form(...),
    document: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    if current_user.role == models.UserRole.chef_verified:
        raise HTTPException(status_code=400, detail="Usuário já é chef verificado.")

    # Salva o arquivo (caso enviado)
    document_path = None
    if document:
        uploads_dir = "uploads"
        os.makedirs(uploads_dir, exist_ok=True)
        file_path = f"{uploads_dir}/{current_user.id}_{document.filename}"
        with open(file_path, "wb") as f:
            f.write(document.file.read())
        document_path = file_path

    new_request = models.ChefVerificationRequest(
        user_id=current_user.id,
        justification=justification,
        document_path=document_path,
        status=models.VerificationStatus.pending,
        requested_at=datetime.utcnow()
    )
    db.add(new_request)
    db.commit()
    db.refresh(new_request)
    return new_request

# Admin vê todas as solicitações pendentes
@router.get("/pending", response_model=List[schemas.ChefVerificationRequestOut])
def get_pending_requests(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    if current_user.role != models.UserRole.admin:
        raise HTTPException(status_code=403, detail="Acesso negado.")

    return db.query(models.ChefVerificationRequest).filter_by(
        status=models.VerificationStatus.pending
    ).all()

# Admin aprova ou rejeita uma solicitação
@router.post("/{request_id}/review", response_model=schemas.ChefVerificationRequestOut)
def review_request(
    request_id: int,
    status: schemas.VerificationStatus,
    reason: str = "",
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    if current_user.role != models.UserRole.admin:
        raise HTTPException(status_code=403, detail="Acesso negado.")

    req = db.query(models.ChefVerificationRequest).get(request_id)
    if not req:
        raise HTTPException(status_code=404, detail="Solicitação não encontrada.")

    if req.status != models.VerificationStatus.pending:
        raise HTTPException(status_code=400, detail="Solicitação já foi analisada.")

    req.status = status
    req.reviewed_at = datetime.utcnow()
    req.admin_id = current_user.id
    req.admin_reason = reason if status == schemas.VerificationStatus.rejected else None

    if status == models.VerificationStatus.approved:
        user = db.query(models.User).get(req.user_id)
        user.role = models.UserRole.chef_verified

    db.commit()
    db.refresh(req)
    return req  