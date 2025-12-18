from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from uuid import UUID
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.intelligence import InputCreate, InputUpdate, SignalExtractionResponse
from app.services.intelligence import IntelligenceService

router = APIRouter()

@router.post("/", response_model=None)
async def create_input(
    input_data: InputCreate, 
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    service = IntelligenceService(db)
    
    # Run intelligence pipeline in background to not block API
    # Note: For production, use Celery/APScheduler. 
    # For MVP, FastAPI BackgroundTasks is okay but verify DB session handling.
    # Actually, for simplicity/MVP debugging, let's run it synchronously first 
    # to see errors immediately.
    
    try:
        result = await service.process_input(input_data)
        return {"status": "processed", "extraction": result}
    except Exception as e:
        print(f"Error processing input: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=None)
def get_all_inputs(db: Session = Depends(get_db)):
    from app.models.input import Input
    from app.models.account import Account
    results = db.query(Input, Account.name.label("account_name")).join(Account, Input.account_id == Account.id).order_by(Input.created_at.desc()).all()
    
    # Format to return flat objects for easier frontend consumption
    formatted = []
    for input_obj, account_name in results:
        data = {c.name: getattr(input_obj, c.name) for c in input_obj.__table__.columns}
        data["account_name"] = account_name
        formatted.append(data)
    return formatted

@router.get("/accounts/{account_id}", response_model=None)
def get_inputs_for_account(
    account_id: str,
    db: Session = Depends(get_db)
):
    try:
        from app.models.input import Input
        inputs = db.query(Input).filter(Input.account_id == account_id).order_by(Input.created_at.desc()).all()
        # Manual serialization since we don't have a response model
        return [{c.name: getattr(i, c.name) for c in i.__table__.columns} for i in inputs]
    except Exception as e:
        print(f"ERROR in get_inputs_for_account: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{input_id}", response_model=None)
def update_input(
    input_id: str,
    input_update: InputUpdate,
    db: Session = Depends(get_db)
):
    from app.models.input import Input
    db_input = db.query(Input).filter(Input.id == input_id).first()
    if not db_input:
        raise HTTPException(status_code=404, detail="Input not found")
    
    update_data = input_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_input, key, value)
    
    db.commit()
    db.refresh(db_input)
    return db_input
