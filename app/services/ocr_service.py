# app/services/ocr_service.py
import easyocr
import cv2
import numpy as np
from PIL import Image
import re
from langdetect import detect, DetectorFactory
import logging

# Set seed for consistent language detection
DetectorFactory.seed = 0

class OCRService:
    def __init__(self):
        """Initialize OCR service with multiple language support"""
        # Start with common languages, can be expanded
        # TODO - add more languages to the list
        self.reader = easyocr.Reader(["en"])
        self.logger = logging.getLogger(__name__)
        
    def preprocess_image(self, image_path):
        """Preprocess image for better OCR results"""
        try:
            # Read image
            img = cv2.imread(image_path)
            
            # Convert to grayscale
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # Apply gaussian blur to reduce noise
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            
            # Apply adaptive thresholding
            thresh = cv2.adaptiveThreshold(
                blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
            )
            
            return thresh
            
        except Exception as e:
            self.logger.error(f"Image preprocessing failed: {e}")
            return cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    
    def extract_text_from_image(self, image_path, target_language=None):
        """Extract text from book cover image"""
        try:
            # Preprocess image
            processed_img = self.preprocess_image(image_path)
            
            # Perform OCR
            results = self.reader.readtext(processed_img)
            
            # Extract text and confidence scores
            extracted_text = []
            for (bbox, text, confidence) in results:
                if confidence > 0.3:  # Filter low confidence text
                    extracted_text.append({
                        "text": text.strip(),
                        "confidence": confidence,
                        "bbox": bbox
                    })
            
            return extracted_text
            
        except Exception as e:
            self.logger.error(f"OCR extraction failed: {e}")
            return []
    
    def detect_language(self, text_list):
        """Detect the primary language of extracted text"""
        try:
            # Combine all text
            combined_text = " ".join([item["text"] for item in text_list])
            
            if len(combined_text.strip()) < 3:
                return "unknown"
                
            detected_lang = detect(combined_text)
            
            # Map language codes to full names
            lang_map = {
                "en": "English",
                "es": "Spanish", 
                "fr": "French",
                "de": "German",
                "it": "Italian",
                "pt": "Portuguese",
                "ja": "Japanese",
                "ko": "Korean",
                "zh-cn": "Chinese",
                "zh": "Chinese"
            }
            
            return lang_map.get(detected_lang, detected_lang)
            
        except Exception as e:
            self.logger.error(f"Language detection failed: {e}")
            return "unknown"
    
    def parse_book_info(self, text_list):
        """Parse extracted text to identify title, author, etc."""
        try:
            # Sort by confidence and position (top to bottom)
            sorted_text = sorted(text_list, key=lambda x: (-x["confidence"], x["bbox"][0][1]))
            
            title = ""
            author = ""
            translator = ""
            publisher = ""
            
            # Common patterns for identifying different fields
            author_patterns = [
                r'^by\s+(.+)$',
                r'^(.+)\s+author$',
                r'written\s+by\s+(.+)$'
            ]
            
            translator_patterns = [
                r'translated\s+by\s+(.+)$',
                r'translator:\s*(.+)$',
                r'trans\.\s+(.+)$'
            ]
            
            publisher_patterns = [
                r'published\s+by\s+(.+)$',
                r'publisher:\s*(.+)$'
            ]
            
            # First high-confidence, large text is likely the title
            if sorted_text:
                title = sorted_text[0]["text"]
            
            # Look for author, translator, publisher patterns
            for item in sorted_text[1:]:  # Skip first item (title)
                text = item["text"].lower().strip()
                
                # Check for author patterns
                for pattern in author_patterns:
                    match = re.search(pattern, text, re.IGNORECASE)
                    if match and not author:
                        author = match.group(1).strip()
                        break
                
                # Check for translator patterns
                for pattern in translator_patterns:
                    match = re.search(pattern, text, re.IGNORECASE)
                    if match and not translator:
                        translator = match.group(1).strip()
                        break
                
                # Check for publisher patterns
                for pattern in publisher_patterns:
                    match = re.search(pattern, text, re.IGNORECASE)
                    if match and not publisher:
                        publisher = match.group(1).strip()
                        break
                
                # If no patterns match, use heuristics
                if not author and len(text.split()) <= 4 and item["confidence"] > 0.7:
                    # Likely an author name
                    author = item["text"]
            
            return {
                "title": title,
                "author": author,
                "translator": translator,
                "publisher": publisher
            }
            
        except Exception as e:
            self.logger.error(f"Book info parsing failed: {e}")
            return {
                "title": "",
                "author": "",
                "translator": "",
                "publisher": ""
            }
    
    def process_book_cover(self, image_path, target_language=None):
        """Main method to process book cover and extract book information"""
        try:
            # Extract text from image
            extracted_text = self.extract_text_from_image(image_path, target_language)
            
            if not extracted_text:
                return {
                    "success": False,
                    "error": "No text detected in image"
                }
            
            # Detect language
            detected_language = self.detect_language(extracted_text)
            
            # Parse book information
            book_info = self.parse_book_info(extracted_text)
            
            # Add detected language
            book_info["language"] = detected_language
            
            return {
                "success": True,
                "book_info": book_info,
                "raw_text": extracted_text,
                "detected_language": detected_language
            }
            
        except Exception as e:
            self.logger.error(f"Book cover processing failed: {e}")
            return {
                "success": False,
                "error": f"Processing failed: {str(e)}"
            }

# Example usage
if __name__ == "__main__":
    ocr = OCRService()
    result = ocr.process_book_cover("path/to/book_cover.jpg")
    print(result)