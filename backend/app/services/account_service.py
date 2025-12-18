from sqlalchemy.orm import Session
from uuid import UUID
from typing import List, Optional
from app.models.account import Account
from app.schemas.account import AccountCreate, AccountUpdate

def get_account(db: Session, account_id: UUID) -> Optional[Account]:
    return db.query(Account).filter(Account.id == account_id).first()

def get_accounts(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    owner_id: Optional[UUID] = None
) -> List[Account]:
    query = db.query(Account)
    if owner_id:
        query = query.filter(Account.owner_id == owner_id)
    return query.offset(skip).limit(limit).all()

def create_account(db: Session, account: AccountCreate) -> Account:
    db_account = Account(
        name=account.name,
        account_type=account.account_type,
        account_email=account.account_email,
        industry=account.industry,
        tier=account.tier,
        owner_id=account.owner_id,
        parent_account_id=account.parent_account_id,
        check_in_interval_days=account.check_in_interval_days
    )
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account

def update_account(db: Session, account_id: UUID, account_update: AccountUpdate) -> Optional[Account]:
    db_account = get_account(db, account_id)
    if not db_account:
        return None
    
    update_data = account_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_account, key, value)
    
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account

def get_children(db: Session, parent_id: UUID) -> List[Account]:
    return db.query(Account).filter(Account.parent_account_id == parent_id).all()
