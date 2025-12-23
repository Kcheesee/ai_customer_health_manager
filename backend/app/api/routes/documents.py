from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
import shutil
import os
from uuid import UUID, uuid4
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.document import AccountDocument
from app.schemas.document import DocumentCreate, DocumentResponse

router = APIRouter()

# Reuse existing upload dir or create new one
UPLOAD_DIR = "app/static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload", response_model=DocumentResponse)
async def upload_document(
    account_id: UUID,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    try:
        # Generate safe filename
        ext = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid4()}{ext}"
        file_path = os.path.join(UPLOAD_DIR, unique_filename)
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Create database record
        new_doc = AccountDocument(
            account_id=account_id,
            name=file.filename,
            file_path=file_path,
            file_type=ext.lstrip('.') or 'unknown'
        )
        db.add(new_doc)
        db.commit()
        db.refresh(new_doc)
        
        return new_doc
    except Exception as e:
        print(f"Error uploading document: {e}")
        raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")

@router.get("/account/{account_id}", response_model=List[DocumentResponse])
def get_account_documents(account_id: UUID, db: Session = Depends(get_db)):
    return db.query(AccountDocument).filter(AccountDocument.account_id == account_id).order_by(AccountDocument.created_at.desc()).all()

@router.delete("/{document_id}")
def delete_document(document_id: UUID, db: Session = Depends(get_db)):
    doc = db.query(AccountDocument).filter(AccountDocument.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Optionally delete file from disk here
    # os.remove(doc.file_path) 
    
    db.delete(doc)
    db.commit()
    return {"status": "success"}
