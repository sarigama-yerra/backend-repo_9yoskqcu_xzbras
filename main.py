import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

from schemas import QuoteRequest
from database import create_document

app = FastAPI(title="Eastside Insurance Brokers API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QuoteResponse(BaseModel):
    id: str
    message: str

@app.get("/")
def read_root():
    return {"message": "Eastside Insurance Brokers API is running"}

@app.get("/api/insurance-types", response_model=List[str])
def get_insurance_types():
    return [
        "Car Insurance",
        "Householders Insurance",
        "Building Insurance",
        "Contractors All Risk",
        "Performance Guarantee",
        "Personal Liability",
        "Business Insurance",
        "Workmanship Compensation",
        "Life Cover",
        "Disability Cover",
        "Critical Illness Cover",
        "Income Protection",
        "Funeral Cover",
        "Investment Planning",
        "Retirement Annuities",
        "Portfolio Management",
    ]

@app.post("/api/quotes", response_model=QuoteResponse)
def create_quote(request: QuoteRequest):
    try:
        inserted_id = create_document("quoterequest", request)
        return {"id": inserted_id, "message": "Thank you! Your request was submitted successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to submit quote request: {str(e)}")

@app.get("/api/hello")
def hello():
    return {"message": "Hello from the backend API!"}

@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    
    try:
        # Try to import database module
        from database import db
        
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            
            # Try to list collections to verify connectivity
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]  # Show first 10 collections
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
            
    except ImportError:
        response["database"] = "❌ Database module not found (run enable-database first)"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"
    
    # Check environment variables
    import os
    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    
    return response


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
