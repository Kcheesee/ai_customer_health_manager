from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from uuid import UUID
from datetime import datetime
from enum import Enum

class AccountType(str, Enum):
    STANDARD = "standard"
    ELA_PARENT = "ela_parent"
    ELA_CHILD = "ela_child"

class Tier(str, Enum):
    ENTERPRISE = "enterprise"
    MID_MARKET = "mid_market"
    SMB = "smb"
    STARTUP = "startup"

class AccountBase(BaseModel):
    name: str
    account_type: AccountType
    account_email: Optional[EmailStr] = None
    industry: Optional[str] = None
    tier: Optional[Tier] = None
    owner_id: Optional[UUID] = None
    parent_account_id: Optional[UUID] = None
    check_in_interval_days: int = 14

class AccountCreate(AccountBase):
    pass

class AccountUpdate(BaseModel):
    name: Optional[str] = None
    account_type: Optional[AccountType] = None
    account_email: Optional[EmailStr] = None
    industry: Optional[str] = None
    tier: Optional[Tier] = None
    owner_id: Optional[UUID] = None
    check_in_interval_days: Optional[int] = None
    is_active: Optional[bool] = None

class AccountResponse(AccountBase):
    id: UUID
    is_active: bool
    # We avoid full recursion here, just basic info
    children_count: int = 0 

    class Config:
        from_attributes = True
