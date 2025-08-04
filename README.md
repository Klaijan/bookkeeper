📋 BookKeeper

BookKeeper helps you organize your personal book collection using modern technology. Add books by taking photos of covers (OCR), scanning barcodes (ISBN lookup), or manual entry. Manage multiple shelves and sync with Google Sheets.

Show Image

✨ Features
📸 Photo OCR: Take a photo of any book cover, AI extracts title, author, translator, and language
🔍 Barcode Scanner: Scan ISBN barcodes to automatically fetch book details
📚 Multiple Shelves: Organize books into custom-named shelves
🌍 Language Support: Currently supports books in English
📊 Google Sheets Integration: Sync your library to spreadsheets for backup and sharing
📱 Mobile-Friendly: Responsive web interface works great on phones and tablets
🏠 Home-Focused: Designed specifically for personal home libraries
🚀 Quick Start
Prerequisites
Python 3.8 or higher
Virtual environment (recommended)
Installation
Clone the repository
bash
git clone https://github.com/Klaijan/bookkeeper.git
cd bookkeeper
Create virtual environment
bash
python -m venv bookkeeper-env

# Activate it
# On Windows:
bookkeeper-env\Scripts\activate
# On macOS/Linux:
source bookkeeper-env/bin/activate
Install dependencies
bash
pip install -r requirements.txt
Run the application
bash
python run.py
Open your browser
http://localhost:5000
📖 How to Use
Adding Books by Photo
Click "Add by Photo" on the home page
Either take a photo with your camera or upload an image
Optionally select the book's language to improve OCR accuracy
Review and edit the extracted information
Save to your library
Adding Books by Barcode
Click "Scan Barcode"
Use your camera to scan the ISBN barcode
Book details will be fetched automatically
Review and edit if needed
Save to your library
Managing Your Library
View all books organized by shelves
Update reading status (To Read, Reading, Read)
Add personal ratings and notes
Export your library to Excel or Google Sheets
🛠️ Technology Stack
Backend: Flask (Python)
OCR: EasyOCR with multi-language support
Book Database: Google Books API
Storage: Google Sheets integration
Frontend: HTML5, CSS3, Vanilla JavaScript
Barcode: pyzbar for ISBN scanning
📋 Book Data Fields
BookKeeper tracks these fields for each book:

Title (required)
Author
Translator
Publisher
Language
Original Language
Type (book, manga, etc.)
Reading Status (to read, reading, read)
Shelf Number
Fiction/Non-fiction
On Shelf? (physical location tracking)
Personal Rating
Tags
Other Remarks
🔧 Configuration
Google Books API Setup (Optional)
Get a Google Books API key from Google Cloud Console
Set environment variable: export GOOGLE_BOOKS_API_KEY=your_key_here
Without API key, you'll use the free tier with rate limits
Google Sheets Integration (Optional)
Create a Google Cloud project
Enable Google Sheets API
Download service account credentials
Place credentials.json in the project root
🏗️ Project Structure
bookkeeper/
├── app/
│   ├── main.py              # Flask application
│   ├── routes/              # URL routes
│   │   ├── ocr_routes.py    # Photo OCR handling
│   │   ├── barcode_routes.py # Barcode scanning
│   │   └── book_routes.py   # Book management
│   ├── services/            # Business logic
│   │   ├── ocr_service.py   # EasyOCR integration
│   │   ├── api_service.py   # Google Books API
│   │   └── sheets_service.py # Google Sheets
│   ├── models/              # Data models
│   └── templates/           # HTML templates
├── static/                  # CSS, JS, uploads
├── requirements.txt
└── run.py                   # Application entry point
🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

📝 License
This project is licensed under the MIT License - see the LICENSE file for details.

🔮 Roadmap
 Barcode scanning implementation
 Google Sheets integration
 Book recommendation system
 Reading statistics and analytics
 Book lending tracker
 Mobile app version
 Advanced search and filtering
 Book condition tracking
 Library sharing with friends
🐛 Issues & Support
If you encounter any issues or have questions:

Check the Issues page
Create a new issue with detailed description
Include error messages and steps to reproduce
🙏 Acknowledgments
EasyOCR - For excellent OCR capabilities
Google Books API - For comprehensive book database
Flask - For the elegant web framework
Made with ❤️ for book lovers everywhere

