from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime
from uuid import UUID

class ContractBase(BaseModel):
    contract_name: str
    contract_type: str
    status: str
    effective_date: date
    end_date: date
    term_length: Optional[str] = None
    auto_renewal: bool = True
    notice_period_days: int = 30
    total_contract_value: Optional[float] = 0
    arr: Optional[float] = 0
    primary_signer: Optional[str] = None
    products_modules: Optional[List[str]] = []

class ContractCreate(ContractBase):
    account_id: UUID

class ContractUpdate(ContractBase):
    pass

class ContractResponse(ContractBase):
    id: UUID
    account_id: UUID
    created_at: date
    updated_at: date

    class Config:
        from_attributes = True
