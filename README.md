## 🧬 Gemini Chatbot

**A full-stack AI assistant** using the [Google Gemini API](https://ai.google.dev), built with Python (Flask) and a modern HTML/CSS/JS frontend.

---

## 📌 Overview

This project has 3 main phases:

| Phase       | Description                                                                 |
| ----------- | --------------------------------------------------------------------------- |
| **Phase 1** | CLI chatbot using Gemini API and Python                                     |
| **Phase 2** | Flask API (`/ask`) for programmatic question/answer interaction             |
| **Phase 3** | Beautiful front-end UI with chat bubbles, avatars, animations, and JS logic |

---

## 🧱 Project Structure

```
Phentech/
├── app.py               # Flask API for Gemini
├── config.py            # Stores Gemini API key
├── main.py              # CLI version of Gemini chat
├── templates/
│   └── index.html       # Web frontend interface
├── static/
│   ├── style.css        # Responsive UI styling
│   └── script.js        # Frontend logic (chat sending)
└── README.md            # Project documentation
```

---

## ✅ How to Run

1. **Clone the repo** & activate virtual environment:

   ```bash
   git clone https://github.com/your-username/gemini-chatbot.git
   cd gemini-chatbot
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Add your API key to `config.py`:**

   ```python
   GEMINI_API_KEY = "your_gemini_api_key"
   ```

4. **Run the Flask server:**

   ```bash
   python app.py
   ```

5. Open in browser:
   👉 [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 📬 Testing the API

You can test the `/ask` endpoint using **Postman** or **cURL**:

```http
POST http://localhost:5000/ask
Content-Type: application/json

{
  "question": "Tell me about quantum computing"
}
```

---

## ✨ Features

* Google Gemini 2.5 Pro integration
* Modern responsive UI (mobile-friendly)
* Chat bubble styling with avatars
* Auto-scroll and Enter key support
* Gemini “typing…” status indicator
* Clean folder structure for production

---

## 📁 Key Files (Click to View)

| File                                             | Purpose                                 |
| ------------------------------------------------ | --------------------------------------- |
| [`main.py`](./main.py)                           | CLI chatbot via terminal                |
| [`app.py`](./app.py)                             | Flask API server                        |
| [`templates/index.html`](./templates/index.html) | Web UI markup                           |
| [`static/style.css`](./static/style.css)         | CSS styling for chat layout             |
| [`static/script.js`](./static/script.js)         | JS logic for sending/receiving messages |

---

## 🔐 Gemini API Key Setup

1. Go to: [https://makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey)
2. Create a `config.py` file with:

   ```python
   GEMINI_API_KEY = "your_api_key_here"
   ```

---

## 🚀 Future Ideas

* 🌓 Dark mode toggle
* 🖼️ Gemini Vision image support
* 📜 Save chat history (session/localStorage)
* 🔐 User login via OAuth
* 📱 Convert to PWA (mobile app feel)

---

## 👨‍💻 Author

**Umar Tariq**
Cybersecurity & AI Developer
