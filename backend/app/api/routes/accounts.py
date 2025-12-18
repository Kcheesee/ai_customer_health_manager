from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from app.core.database import get_db
from app.schemas.account import AccountCreate, AccountResponse, AccountUpdate
from app.services import account_service

router = APIRouter()

@router.post("/", response_model=AccountResponse)
def create_account(account: AccountCreate, db: Session = Depends(get_db)):
    return account_service.create_account(db=db, account=account)

@router.get("/", response_model=List[AccountResponse])
def read_accounts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    accounts = account_service.get_accounts(db, skip=skip, limit=limit)
    # Populate children_count for response (simple approach for now)
    for acc in accounts:
        acc.children_count = len(acc.children) if acc.children else 0
    return accounts

@router.get("/{account_id}", response_model=AccountResponse)
def read_account(account_id: UUID, db: Session = Depends(get_db)):
    db_account = account_service.get_account(db, account_id=account_id)
    if db_account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    db_account.children_count = len(db_account.children) if db_account.children else 0
    return db_account

@router.put("/{account_id}", response_model=AccountResponse)
def update_account(account_id: UUID, account: AccountUpdate, db: Session = Depends(get_db)):
    db_account = account_service.update_account(db, account_id=account_id, account_update=account)
    if db_account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return db_account

@router.get("/{account_id}/children", response_model=List[AccountResponse])
def read_account_children(account_id: UUID, db: Session = Depends(get_db)):
    return account_service.get_children(db, parent_id=account_id)
