# app/main.py
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
import logging

# Import routers
from app.routes.ocr_routes import router as ocr_router

def create_app():
    """Application factory pattern"""
    app = FastAPI(
        title="BookKeeper",
        description="Home library service",
        version="1.0.0"
    )
    
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    
    # Mount static files
    app.mount("/static", StaticFiles(directory="static"), name="static")
    
    # Setup templates
    templates = Jinja2Templates(directory="app/templates")
    
    # Include routers
    app.include_router(ocr_router, prefix="/ocr", tags=["OCR"])
    
    # Main routes
    @app.get("/", response_class=HTMLResponse)
    async def index(request: Request):
        """Home page with options to add books"""
        return templates.TemplateResponse("index.html", {"request": request})
    
    @app.get("/add-book", response_class=HTMLResponse)
    async def add_book(request: Request):
        """Book addition options"""
        return templates.TemplateResponse("add_book.html", {"request": request})
    
    # Error handlers
    @app.exception_handler(404)
    async def not_found_handler(request: Request, exc):
        return HTMLResponse("<h1>404 - Page Not Found</h1><a href='/'>← Back to BookKeeper</a>", status_code=404)

    @app.exception_handler(500)
    async def internal_error_handler(request: Request, exc):
        return templates.TemplateResponse("500.html", {"request": request}, status_code=500)
    
    return app

# For development
if __name__ == "__main__":
    import uvicorn
    app = create_app()
    uvicorn.run(app, host="0.0.0.0", port=5000, reload=True)