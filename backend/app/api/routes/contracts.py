from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.contract import Contract
from app.schemas.contract import ContractCreate, ContractUpdate, ContractResponse

router = APIRouter()

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

@router.post("/contracts/", response_model=ContractResponse)
def create_contract(contract: ContractCreate, db: Session = Depends(get_db)):
    db_contract = Contract(**contract.model_dump())
    db.add(db_contract)
    db.commit()
    db.refresh(db_contract)
    return db_contract

@router.put("/contracts/{contract_id}", response_model=ContractResponse)
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

@router.delete("/contracts/{contract_id}")
def delete_contract(contract_id: str, db: Session = Depends(get_db)):
    db_contract = db.query(Contract).filter(Contract.id == contract_id).first()
    if not db_contract:
        raise HTTPException(status_code=404, detail="Contract not found")
    
    db.delete(db_contract)
    db.commit()
    return {"status": "success"}
