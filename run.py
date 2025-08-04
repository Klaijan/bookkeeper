# run.py
import uvicorn
import os
from app.main import create_app

# Create the FastAPI app
app = create_app()

if __name__ == "__main__":
    # Create upload directory if it doesn't exist
    os.makedirs("static/uploads", exist_ok=True)
    
    # Run the application with uvicorn
    port = int(os.environ.get("PORT", 5000))
    
    uvicorn.run(
        "run:app",  # app module
        host="0.0.0.0",
        port=port,
        reload=True,  # Auto-reload on code changes
        log_level="info"
    )