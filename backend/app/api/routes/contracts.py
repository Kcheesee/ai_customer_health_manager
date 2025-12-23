from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
import shutil
import os
from uuid import UUID, uuid4
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.contract import Contract
from app.schemas.contract import ContractCreate, ContractUpdate, ContractResponse

router = APIRouter()

# Upload directory: backend/app/static/uploads
UPLOAD_DIR = "app/static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload/")
async def upload_contract_document(file: UploadFile = File(...)):
    try:
        # Generate safe filename
        ext = os.path.splitext(file.filename)[1]
        filename = f"{uuid4()}{ext}"
        file_path = os.path.join(UPLOAD_DIR, filename)
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Return relative path for storage
        return {"path": file_path, "filename": file.filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")

@router.get("/", response_model=List[ContractResponse])
def get_all_contracts(db: Session = Depends(get_db)):
    return db.query(Contract).all()

@router.get("/accounts/{account_id}/contracts", response_model=List[ContractResponse])
def get_contracts_for_account(account_id: str, db: Session = Depends(get_db)):
    try:
        contracts = db.query(Contract).filter(Contract.account_id == account_id).all()
        return contracts
    except Exception as e:
        print(f"ERROR in get_contracts_for_account: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/", response_model=ContractResponse)
def create_contract(contract: ContractCreate, db: Session = Depends(get_db)):
    db_contract = Contract(**contract.model_dump())
    db.add(db_contract)
    db.commit()
    db.refresh(db_contract)
    return db_contract

@router.put("/{contract_id}", response_model=ContractResponse)
def update_contract(contract_id: str, contract: ContractUpdate, db: Session = Depends(get_db)):
    db_contract = db.query(Contract).filter(Contract.id == contract_id).first()
    if not db_contract:
        raise HTTPException(status_code=404, detail="Contract not found")
    
    update_data = contract.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_contract, key, value)
    
    db.commit()
    db.refresh(db_contract)
    return db_contract

@router.delete("/{contract_id}")
def delete_contract(contract_id: str, db: Session = Depends(get_db)):
    db_contract = db.query(Contract).filter(Contract.id == contract_id).first()
    if not db_contract:
        raise HTTPException(status_code=404, detail="Contract not found")
    
    db.delete(db_contract)
    db.commit()
    return {"status": "success"}
