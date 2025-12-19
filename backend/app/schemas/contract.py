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
    economic_buyer: Optional[str] = None
    products_modules: Optional[List[str]] = []
    
    # Federal Compliance Fields - The Differentiator!
    fedramp_required: bool = False
    fisma_level: str = "none"  # none, low, moderate, high
    hipaa_required: bool = False
    section_508_required: bool = False
    ato_status: str = "none"  # none, pending, active, expired
    ato_expiry_date: Optional[date] = None


class ContractCreate(ContractBase):
    account_id: UUID


class ContractUpdate(BaseModel):
    """All fields optional for partial updates."""
    contract_name: Optional[str] = None
    contract_type: Optional[str] = None
    status: Optional[str] = None
    effective_date: Optional[date] = None
    end_date: Optional[date] = None
    term_length: Optional[str] = None
    auto_renewal: Optional[bool] = None
    notice_period_days: Optional[int] = None
    total_contract_value: Optional[float] = None
    arr: Optional[float] = None
    primary_signer: Optional[str] = None
    economic_buyer: Optional[str] = None
    products_modules: Optional[List[str]] = None
    # Federal compliance
    fedramp_required: Optional[bool] = None
    fisma_level: Optional[str] = None
    hipaa_required: Optional[bool] = None
    section_508_required: Optional[bool] = None
    ato_status: Optional[str] = None
    ato_expiry_date: Optional[date] = None


class ContractResponse(ContractBase):
    id: UUID
    account_id: UUID
    created_at: date
    updated_at: date

    class Config:
        from_attributes = True
