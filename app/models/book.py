# app/models/book.py
from pydantic import BaseModel, Field
from typing import Optional, Literal
from enum import Enum

class ReadingStatus(str, Enum):
    """Reading status options"""
    TO_READ = "to_read"
    READING = "reading" 
    READ = "read"

class BookType(str, Enum):
    """Book type options"""
    BOOK = "book"
    MANGA = "manga"
    COMIC = "comic"
    TEXTBOOK = "textbook"
    MAGAZINE = "magazine"
    OTHER = "other"

class FictionType(str, Enum):
    """Fiction classification"""
    FICTION = "fiction"
    NON_FICTION = "non_fiction"
    UNKNOWN = "unknown"

class BookBase(BaseModel):
    """Base book model with core fields"""
    title: str = Field(..., min_length=1, description="Book title (required)")
    author: Optional[str] = Field(None, description="Book author")
    translator: Optional[str] = Field(None, description="Translator name")
    publisher: Optional[str] = Field(None, description="Publisher name")
    language: Optional[str] = Field(None, description="Book language")
    original_language: Optional[str] = Field(None, description="Original language if translated")
    book_type: BookType = Field(BookType.BOOK, description="Type of book")
    reading_status: ReadingStatus = Field(ReadingStatus.TO_READ, description="Current reading status")
    shelf_number: Optional[str] = Field("Shelf 1", description="Which shelf the book is on")
    fiction_type: FictionType = Field(FictionType.UNKNOWN, description="Fiction or non-fiction")
    on_shelf: bool = Field(True, description="Is the book physically on the shelf?")
    personal_rating: Optional[int] = Field(None, ge=1, le=5, description="Personal rating 1-5")
    tags: Optional[str] = Field(None, description="Comma-separated tags")
    remarks: Optional[str] = Field(None, description="Additional notes")

class BookCreate(BookBase):
    """Model for creating a new book"""
    pass

class BookUpdate(BaseModel):
    """Model for updating book information"""
    title: Optional[str] = Field(None, min_length=1)
    author: Optional[str] = None
    translator: Optional[str] = None
    publisher: Optional[str] = None
    language: Optional[str] = None
    original_language: Optional[str] = None
    book_type: Optional[BookType] = None
    reading_status: Optional[ReadingStatus] = None
    shelf_number: Optional[str] = None
    fiction_type: Optional[FictionType] = None
    on_shelf: Optional[bool] = None
    personal_rating: Optional[int] = Field(None, ge=1, le=5)
    tags: Optional[str] = None
    remarks: Optional[str] = None

class Book(BookBase):
    """Complete book model with ID"""
    id: str = Field(..., description="Unique book identifier")
    created_at: str = Field(..., description="Creation timestamp")
    updated_at: str = Field(..., description="Last update timestamp")

class OCRResult(BaseModel):
    """OCR processing result"""
    success: bool
    book_info: Optional[dict] = None
    raw_text: Optional[list] = None
    detected_language: Optional[str] = None
    error: Optional[str] = None

class APIResponse(BaseModel):
    """Standard API response format"""
    success: bool
    message: str
    data: Optional[dict] = None
    error: Optional[str] = None