from fastapi import FastAPI, Depends
from pydantic import BaseModel
from src.agent import generate_water_insight
from src.database import SessionLocal, get_db
from src.models import WaterLog
from sqlalchemy.orm import Session

app = FastAPI(
    title="💧 AI Water Tracker API",
    description="FastAPI backend that stores hydration data and returns AI-generated insights.",
    version="1.0.0"
)

# Pydantic model for request body
class WaterInput(BaseModel):
    user_id: str = "user_1"
    amount_ml: float


@app.post("/log_water")
def log_water(data: WaterInput, db: Session = Depends(get_db)):
    """
    API endpoint to log water intake and get an AI-generated hydration insight.
    """
    try:
        # Generate AI insight
        ai_message = generate_water_insight(data.amount_ml, data.user_id)

        # Create and save the record manually here too
        new_entry = WaterLog(
            user_id=data.user_id,
            amount_ml=data.amount_ml,
            ai_insight=ai_message
        )
        db.add(new_entry)
        db.commit()
        db.refresh(new_entry)

        return {
            "status": "success",
            "message": ai_message,
            "entry_id": new_entry.id,
            "amount_logged": data.amount_ml
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}
