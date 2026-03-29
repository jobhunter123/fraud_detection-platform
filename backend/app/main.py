from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import engine, Base, get_db
from app import models
from app.schemas import (
    UserRegister, TokenResponse,
    TransactionInput, TransactionResponse
)
from app.auth import (
    hash_password, verify_password,
    create_access_token, get_current_user
)
from app.risk_engine import calculate_risk
from app.attack_simulator import generate_attack
from app.llm_reporter import generate_investigation_report

# ── APP SETUP ────────────────────────────────────────────────
app = FastAPI(
    title="Fraud Detection API",
    description="AI-Powered Real-Time Fraud Detection & Attack Simulation Platform",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)


# ── PUBLIC ROUTES ────────────────────────────────────────────

@app.get("/", tags=["Health"])
def home():
    return {
        "message": "Fraud Detection API is running",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.post("/register", tags=["Auth"], status_code=201)
def register(data: UserRegister, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(
        models.User.username == data.username
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    user = models.User(
        username=data.username,
        hashed_password=hash_password(data.password)
    )
    db.add(user)
    db.commit()
    return {"message": f"User '{data.username}' registered successfully"}


@app.post("/login", response_model=TokenResponse, tags=["Auth"])
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(
        models.User.username == form_data.username
    ).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}


# ── PROTECTED ROUTES (JWT required) ─────────────────────────

@app.post("/transaction", tags=["Fraud Detection"])
def create_transaction(
    data: TransactionInput,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    result = calculate_risk(data.model_dump())

    transaction = models.Transaction(
        user_id=data.user_id,
        amount=data.amount,
        device_id=data.device_id,
        location=data.location,
        risk_score=result["score"],
        flagged=result["score"] > 70,
    )
    db.add(transaction)
    db.commit()
    db.refresh(transaction)

    report = None
    if transaction.flagged:
        report = generate_investigation_report(
            data.model_dump(), result["score"], result["reasons"]
        )

    return {
        "id": transaction.id,
        "user_id": transaction.user_id,
        "amount": transaction.amount,
        "device_id": transaction.device_id,
        "location": transaction.location,
        "risk_score": result["score"],
        "flagged": transaction.flagged,
        "risk_reasons": result["reasons"],
        "investigation_report": report,
    }


@app.get("/transactions", tags=["Fraud Detection"])
def get_transactions(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return db.query(models.Transaction).order_by(
        models.Transaction.id.desc()
    ).all()


@app.get("/fraud", tags=["Fraud Detection"])
def get_fraud_transactions(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return db.query(models.Transaction).filter(
        models.Transaction.flagged == True
    ).order_by(models.Transaction.id.desc()).all()


@app.get("/simulate_attack", tags=["Attack Simulation"])
def simulate_attack(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    data = generate_attack()
    result = calculate_risk(data)

    transaction = models.Transaction(
        user_id=data["user_id"],
        amount=data["amount"],
        device_id=data["device_id"],
        location=data["location"],
        risk_score=result["score"],
        flagged=result["score"] > 70,
    )
    db.add(transaction)
    db.commit()
    db.refresh(transaction)

    report = None
    if transaction.flagged:
        report = generate_investigation_report(
            data, result["score"], result["reasons"]
        )

    return {
        "id": transaction.id,
        "input_data": data,
        "risk_score": result["score"],
        "flagged": transaction.flagged,
        "risk_reasons": result["reasons"],
        "investigation_report": report,
    }


@app.get("/stats", tags=["Analytics"])
def get_stats(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    total = db.query(models.Transaction).count()
    fraud = db.query(models.Transaction).filter(
        models.Transaction.flagged == True
    ).count()
    return {
        "total_transactions": total,
        "fraud_detected": fraud,
        "safe_transactions": total - fraud,
        "fraud_rate_percent": round((fraud / total * 100), 2) if total else 0,
    }