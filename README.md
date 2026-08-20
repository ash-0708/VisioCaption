# visioCaption 🔍✨

A multimodal AI web app that generates smart, tone-controlled captions for your images using **Google Gemini Vision API** — supports single and batch image uploads.

![Python](https://img.shields.io/badge/Python-3.9+-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35-red?style=flat-square&logo=streamlit)
![Gemini](https://img.shields.io/badge/Google_Gemini-Vision_API-4285F4?style=flat-square&logo=google)

---

## 🖼️ What it does

- Upload **one or multiple images** (JPG, PNG, WEBP)
- Choose a **caption tone**:
  - 📋 **Descriptive** — detailed, factual description
  - 💼 **Professional** — polished, formal language
  - 🎉 **Social Media** — fun and catchy with emojis
- Get AI-generated captions instantly
- **Download all captions** as a `.txt` file

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python | Core language |
| Streamlit | Web UI framework |
| Google Gemini Vision API (`gemini-1.5-flash`) | Multimodal AI captioning |
| Pillow (PIL) | Image loading & processing |

---

## 🚀 How to Run Locally

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/visioCaption.git
cd visioCaption
```

### 2. Create a virtual environment (recommended)
```bash
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Get a Gemini API Key
- Go to [https://aistudio.google.com](https://aistudio.google.com)
- Sign in with your Google account
- Click **"Get API Key"** — it's free!

### 5. Run the app
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

> **Note:** Enter your API key directly in the sidebar inside the app. Never hardcode it in the source code.

---

## 📁 Project Structure

```
visioCaption/
│
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── .gitignore          # Files to exclude from Git
└── README.md           # This file
```

---

## 💡 Key Features

- **Prompt Engineering** — Custom prompts per tone type for better caption quality
- **Batch Processing** — Handle multiple images in one click
- **Clean UI** — Dark-themed, minimal interface
- **Downloadable Output** — Export all captions to a `.txt` file

---

## ⚠️ Important

- Never commit your API key to GitHub
- The `.gitignore` already excludes `.env` and `secrets.toml` for safety

---


