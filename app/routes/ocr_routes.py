# app/routes/ocr_routes.py
from fastapi import APIRouter, Request, File, UploadFile, Form, HTTPException, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from app.services.ocr_service import OCRService
from app.models.book import OCRResult, BookCreate
import uuid
import os
import aiofiles
from typing import Optional

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

# Dependency injection for OCR service
def get_ocr_service() -> OCRService:
    return OCRService()

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "bmp", "tiff", "webp"}
UPLOAD_FOLDER = "static/uploads"

def allowed_file(filename: str) -> bool:
    """Check if file extension is allowed"""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@router.get("/upload-photo", response_class=HTMLResponse)
async def upload_photo_page(request: Request):
    """Display photo upload page"""
    return templates.TemplateResponse("upload_photo.html", {"request": request})

@router.post("/upload-photo", response_class=HTMLResponse)
async def process_photo_upload(
    request: Request,
    photo: UploadFile = File(..., description="Book cover image"),
    target_language: Optional[str] = Form(None, description="Target language for OCR"),
    ocr_service: OCRService = Depends(get_ocr_service)
):
    """Handle photo upload and OCR processing"""
    
    # Validate file
    if not photo.filename:
        raise HTTPException(status_code=400, detail="No file selected")
    
    if not allowed_file(photo.filename):
        raise HTTPException(
            status_code=400, 
            detail="Invalid file type. Please upload an image file (PNG, JPG, JPEG, GIF, BMP, TIFF, WEBP)"
        )
    
    try:
        # Create unique filename
        file_extension = photo.filename.split(".")[-1].lower()
        filename = f"{uuid.uuid4()}.{file_extension}"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        
        # Ensure upload directory exists
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        
        # Save uploaded file asynchronously
        async with aiofiles.open(filepath, "wb") as buffer:
            content = await photo.read()
            await buffer.write(content)
        
        # Process with OCR
        result = ocr_service.process_book_cover(filepath, target_language)
        
        # Clean up uploaded file
        try:
            os.remove(filepath)
        except:
            pass
        
        if result["success"]:
            # Return confirmation page with extracted data
            return templates.TemplateResponse("confirm_book.html", {
                "request": request,
                "book_data": result["book_info"],
                "source": "ocr",
                "raw_text": result["raw_text"],
                "detected_language": result["detected_language"]
            })
        else:
            raise HTTPException(status_code=500, detail=f"OCR failed: {result['error']}")
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

@router.post("/api/process-photo", response_model=OCRResult)
async def api_process_photo(
    photo: UploadFile = File(..., description="Book cover image"),
    target_language: Optional[str] = Form(None, description="Target language for OCR"),
    ocr_service: OCRService = Depends(get_ocr_service)
):
    """API endpoint for photo processing (for AJAX calls)"""
    
    try:
        # Validate file
        if not photo.filename:
            return OCRResult(success=False, error="No file uploaded")
        
        if not allowed_file(photo.filename):
            return OCRResult(success=False, error="Invalid file type")
        
        # Save and process file
        file_extension = photo.filename.split(".")[-1].lower()
        filename = f"{uuid.uuid4()}.{file_extension}"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        
        async with aiofiles.open(filepath, "wb") as buffer:
            content = await photo.read()
            await buffer.write(content)
        
        # Process with OCR
        result = ocr_service.process_book_cover(filepath, target_language)
        
        # Clean up
        try:
            os.remove(filepath)
        except:
            pass
        
        return OCRResult(**result)
        
    except Exception as e:
        return OCRResult(success=False, error=str(e))

@router.get("/test-ocr", response_class=HTMLResponse)
async def test_ocr(request: Request):
    """Test route for OCR functionality"""
    return templates.TemplateResponse("test_ocr.html", {"request": request})# app/routes/ocr_routes.py
from fastapi import APIRouter, Request, File, UploadFile, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from app.services.ocr_service import OCRService
import uuid
import os
import aiofiles
from typing import Optional

router = APIRouter()
ocr_service = OCRService()
templates = Jinja2Templates(directory="app/templates")

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "bmp", "tiff", "webp"}
UPLOAD_FOLDER = "static/uploads"

def allowed_file(filename: str) -> bool:
    """Check if file extension is allowed"""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@router.get("/upload-photo", response_class=HTMLResponse)
async def upload_photo_page(request: Request):
    """Display photo upload page"""
    return templates.TemplateResponse("upload_photo.html", {"request": request})

@router.post("/upload-photo", response_class=HTMLResponse)
async def process_photo_upload(
    request: Request,
    photo: UploadFile = File(...),
    target_language: Optional[str] = Form(None)
):
    """Handle photo upload and OCR processing"""
    
    # Validate file
    if not photo.filename:
        raise HTTPException(status_code=400, detail="No file selected")
    
    if not allowed_file(photo.filename):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload an image file.")
    
    try:
        # Create unique filename
        file_extension = photo.filename.split(".")[-1]
        filename = f"{uuid.uuid4()}.{file_extension}"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        
        # Ensure upload directory exists
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        
        # Save uploaded file
        async with aiofiles.open(filepath, "wb") as buffer:
            content = await photo.read()
            await buffer.write(content)
        
        # Process with OCR
        result = ocr_service.process_book_cover(filepath, target_language)
        
        # Clean up uploaded file
        try:
            os.remove(filepath)
        except:
            pass
        
        if result["success"]:
            # Return confirmation page with extracted data
            return templates.TemplateResponse("confirm_book.html", {
                "request": request,
                "book_data": result["book_info"],
                "source": "ocr",
                "raw_text": result["raw_text"]
            })
        else:
            raise HTTPException(status_code=500, detail=f"OCR failed: {result['error']}")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

@router.post("/api/process-photo")
async def api_process_photo(
    photo: UploadFile = File(...),
    target_language: Optional[str] = Form(None)
):
    """API endpoint for photo processing (for AJAX calls)"""
    
    try:
        # Validate file
        if not photo.filename:
            return JSONResponse({"success": False, "error": "No file uploaded"})
        
        if not allowed_file(photo.filename):
            return JSONResponse({"success": False, "error": "Invalid file type"})
        
        # Save and process file
        file_extension = photo.filename.split(".")[-1]
        filename = f"{uuid.uuid4()}.{file_extension}"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        
        async with aiofiles.open(filepath, "wb") as buffer:
            content = await photo.read()
            await buffer.write(content)
        
        # Process with OCR
        result = ocr_service.process_book_cover(filepath, target_language)
        
        # Clean up
        try:
            os.remove(filepath)
        except:
            pass
        
        return JSONResponse(result)
        
    except Exception as e:
        return JSONResponse({"success": False, "error": str(e)})

@router.get("/test-ocr", response_class=HTMLResponse)
async def test_ocr(request: Request):
    """Test route for OCR functionality"""
    return templates.TemplateResponse("test_ocr.html", {"request": request})