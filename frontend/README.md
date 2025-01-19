# StarScraper 🌟

> A powerful web review scraping tool with a cyberpunk-themed UI. Built with Flask and Vue.js.

---

## ⚡ Features

📊 **Core Capabilities**
- Dynamic Web Scraping | Intelligent content extraction
- Smart Pagination | Automatic page navigation
- Real-time Analytics | Instant data visualization

🎨 **User Experience**
- Cyberpunk UI | Modern, responsive design
- Error Handling | Comprehensive error management
- Review Analysis | Detailed review insights

## 🛠️ Tech Stack

**Backend**
- Python | Flask | Playwright
- Beautiful Soup | OpenAI API

**Frontend**
- Vue.js
- Tailwind CSS
- Vite

## 📋 Prerequisites

```
Python 3.8+
Node.js and npm
Virtual Environment (venv)
OpenAI API Key
```

## 📁 Project Structure

```
starscraper/
├── 📂 backend/
│   ├── 📜 app.py                 # Flask application
│   └── 📜 requirements.txt       # Python dependencies
├── 📂 frontend/
│   ├── 📂 src/
│   │   ├── 📜 App.vue           # Main Vue component
│   │   ├── 📜 main.js           # Vue entry point
│   │   └── 📂 assets/           # Static assets
│   ├── 📜 package.json          # Node dependencies
│   └── 📜 vite.config.js        # Vite configuration
└── 📜 README.md
```

## 🚀 Installation

### Backend Setup

1️⃣ Create and activate virtual environment:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

2️⃣ Install dependencies:
```bash
cd backend
pip install -r requirements.txt
playwright install
```

3️⃣ Configure environment variables:
```bash
# Create .env file in backend directory
echo "OPENAI_API_KEY=your_api_key_here" > .env
```

### Frontend Setup

1️⃣ Create Vue project:
```bash
npm init vue@latest frontend
cd frontend
```

2️⃣ Install dependencies:
```bash
npm install
npm install tailwindcss @tailwindcss/forms postcss autoprefixer
npx tailwindcss init -p
```

## 💻 Usage

1️⃣ Start backend server:
```bash
cd backend
flask run
```

2️⃣ Start frontend development server:
```bash
cd frontend
npm run dev
```

3️⃣ Access the application at `http://localhost:5173`

## 🔌 API Reference

### GET /api/reviews

Scrapes reviews from specified URL.

**Parameters:**
| Name | Type | Description |
|------|------|-------------|
| url | string | Target website URL (required) |
| max_reviews | integer | Maximum reviews to scrape (optional, default: 500) |

**Example Response:**
```json
{
  "reviews": [
    {
      "rating": 5,
      "title": "Great Product!",
      "body": "Review content...",
      "reviewer": "John D."
    }
  ],
  "reviews_count": 1,
  "pages_with_unique_reviews": 1,
  "scrape_date": "2025-01-19 14:30:00"
}
```

## ⚡ Quick Start

1. Enter target URL in the input field
2. Set maximum number of reviews (optional)
3. Click "INITIATE_SCRAPING"
4. View results in the dashboard

## ⚠️ Error Handling

**Built-in Protection**
- ✓ Invalid URL validation
- ✓ Network error detection
- ✓ Server error management
- ✓ Rate limiting protection
- ✓ Timeout handling

## 🔧 Troubleshooting

Common issues and solutions:

| Issue | Solution |
|-------|----------|
| Connection Error | Check if both servers are running |
| CORS Error | Verify CORS configuration in Flask |
| Scraping Failed | Ensure URL is accessible and valid |
| No Reviews Found | Check if website structure is supported |

## 📝 Developer Notes

**Key Features**
- Tailwind CSS for styling
- CORS enabled for development
- Playwright for dynamic content
- Real-time error feedback
- Responsive design principles

## 📄 License

MIT License - see LICENSE for details

---

## 👩‍💻 Creator

**Developed with ❤️ by Pavithra C**

---

"Making data extraction elegant and efficient."