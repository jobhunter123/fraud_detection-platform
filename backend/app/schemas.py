from pydantic import BaseModel, Field
from typing import Optional, List


class UserRegister(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=6, max_length=100)


class UserLogin(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TransactionInput(BaseModel):
    user_id: int = Field(gt=0)
    amount: float = Field(gt=0, lt=10_000_000, description="Amount in INR")
    device_id: str = Field(min_length=1, max_length=100)
    location: str = Field(min_length=1, max_length=100)
    device_new: Optional[bool] = False
    location_change: Optional[bool] = False
    rapid_transactions: Optional[bool] = False


class TransactionResponse(BaseModel):
    id: int
    user_id: int
    amount: float
    device_id: str
    location: str
    risk_score: float
    flagged: bool
    risk_reasons: List[str] = []
    investigation_report: Optional[str] = None

    class Config:
        from_attributes = True