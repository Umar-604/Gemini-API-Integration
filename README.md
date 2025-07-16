# Gemini-API-Integration

Here's a complete and professional `README.md` file for your project, documenting all **3 phases**:

---

## 🧬 Gemini Chatbot – Flask + Gemini API + Web UI

A smart, full-stack chatbot powered by **Google Gemini API**, with a Python backend (Flask) and a modern, responsive HTML/CSS/JS frontend.

---

## 📂 Project Structure

```
Phentech/
├── app.py                # Flask backend
├── config.py             # Gemini API key
├── templates/
│   └── index.html        # Chat frontend UI
├── static/
│   ├── style.css         # Custom chat styling
│   └── script.js         # JavaScript for messaging
├── venv/                 # Python virtual environment
└── README.md             # Documentation
```

---

## 🚀 Phase 1 – CLI Gemini Chat (Terminal)

Interact with Gemini from the command line using Python.

### ✅ Setup

1. **Install packages:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install google-generativeai
   ```

2. **Create `config.py`:**

   ```python
   GEMINI_API_KEY = "your_real_api_key"
   ```

3. **Create `main.py`:**

   ```python
   import google.generativeai as genai
   from config import GEMINI_API_KEY

   genai.configure(api_key=GEMINI_API_KEY)
   model = genai.GenerativeModel("gemini-2.5-pro")

   print("🧬 Welcome to Gemini Chat. Type 'exit' to quit.")
   while True:
       prompt = input("You: ")
       if prompt.lower() == "exit":
           break
       response = model.generate_content(prompt)
       print("Gemini:", response.text)
   ```

4. **Run it:**

   ```bash
   python main.py
   ```

---

## 🌐 Phase 2 – Flask REST API + Postman

Expose Gemini's power via an HTTP API you can test with Postman.

### ✅ Setup

1. **Install Flask:**

   ```bash
   pip install flask
   ```

2. **Update `app.py`:**

   ```python
   from flask import Flask, request, jsonify
   import google.generativeai as genai
   from config import GEMINI_API_KEY

   genai.configure(api_key=GEMINI_API_KEY)
   model = genai.GenerativeModel("gemini-2.5-pro")

   app = Flask(__name__)

   @app.route("/ask", methods=["POST"])
   def ask():
       data = request.get_json()
       question = data.get("question", "")
       if not question:
           return jsonify({"error": "No question provided"}), 400
       try:
           response = model.generate_content(question)
           return jsonify({"response": response.text})
       except Exception as e:
           return jsonify({"error": str(e)}), 500

   if __name__ == "__main__":
       app.run(debug=True)
   ```

3. **Test in Postman:**

* URL: `http://127.0.0.1:5000/ask`
* Method: `POST`
* Body (JSON):

  ```json
  {
    "question": "What is machine learning?"
  }
  ```

---

## 💬 Phase 3 – Beautiful Frontend (HTML/CSS/JS)

User-friendly chat interface with avatars, animations, and mobile support.

### ✅ Folder Structure

```
templates/index.html
static/style.css
static/script.js
```

### ✅ Key Features

* Modern layout with avatars
* Auto-scroll and smooth chat
* Responsive mobile-friendly design
* Gemini "thinking" indicator
* Enter key support

### 🖥️ Preview UI

![](https://user-images.githubusercontent.com/placeholder/mockup.png) <!-- You can replace with actual screenshot -->

### ✅ How to Run

```bash
python app.py
```

Then open: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 🔒 Configuration

All secrets are stored in `config.py`:

```python
GEMINI_API_KEY = "your_api_key_here"
```

To get your Gemini API key:

* Visit: [https://makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey)

---

## 📦 Requirements

```bash
pip install flask google-generativeai
```

---

## 🧠 Future Improvements

* ✅ Dark mode toggle
* ✅ Chat history (localStorage or database)
* 🖼️ Gemini Vision (image support)
* 🔐 Login with Google (OAuth)
* 🚀 Deployment to Render or Railway

---

## 👨‍💻 Author

**Umar Tariq**
Cybersecurity & AI Developer
Project under: **PhenTech Private Limited** Internship (Machine Learning Department)

---

Let me know if you want the actual `.zip`, deployment guide, or real screenshot placeholder for your GitHub repo!
