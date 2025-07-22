from flask import Flask, request, jsonify, render_template, session, redirect, url_for, g
import google.generativeai as genai
from config import GEMINI_API_KEY
from database import init_db, save_chat, get_all_chats, update_chat, delete_chat, create_user, get_user_by_username, get_user_by_id
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize SQLite database
init_db()

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-pro")

# Create Flask app
app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change this in production
app.config['SESSION_PERMANENT'] = False

@app.before_request
def load_logged_in_user():
    user_id = session.get("user_id")
    if user_id is None:
        g.user = None
    else:
        user = get_user_by_id(user_id)
        if user is None:
            session.clear()  # Clear session if user_id is invalid
            g.user = None
        else:
            g.user = user

# ────────────────────────────────
# Authentication Routes
# ────────────────────────────────

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if get_user_by_username(username):
            return render_template("signup.html", error="Username already exists.")
        password_hash = generate_password_hash(password)
        create_user(username, password_hash)
        return redirect(url_for("login"))
    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = get_user_by_username(username)
        if user and check_password_hash(user[2], password):
            session["user_id"] = user[0]
            session["username"] = user[1]
            return redirect(url_for("home"))
        return render_template("login.html", error="Invalid username or password.")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# ────────────────────────────────
# Routes
# ────────────────────────────────

# Homepage
@app.route("/")
def home():
    if g.user is None:
        return redirect(url_for("login"))
    chats = get_all_chats(g.user[0])
    chats.reverse()  # Show the most recent chats first
    return render_template("index.html", username=g.user[1], chats=chats)

# Ask Gemini a question
@app.route("/ask", methods=["POST"])
def ask_gemini():
    if g.user is None:
        return jsonify({"error": "Authentication required"}), 401
    data = request.get_json()
    question = data.get("question", "")

    if not question:
        return jsonify({"error": "No question provided"}), 400

    try:
        response = model.generate_content(question)
        gemini_response = response.text
        save_chat(g.user[0], question, gemini_response)
        return jsonify({"response": gemini_response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# View chat history
@app.route("/history_page")
def history_page():
    if g.user is None:
        return redirect(url_for("login"))
    chats = get_all_chats(g.user[0])
    return render_template("history.html", chats=chats)

# View chat history as JSON for frontend
@app.route("/history")
def history_json():
    if g.user is None:
        return jsonify({"error": "Authentication required"}), 401
    chats = get_all_chats(g.user[0])
    return jsonify({"history": chats})

@app.route("/history/<int:chat_id>")
def history_single(chat_id):
    if g.user is None:
        return jsonify({"error": "Authentication required"}), 401
    # This requires a new function to get a single chat by its ID
    # For now, we'll find it in the list of all chats
    chats = get_all_chats(g.user[0])
    chat = next((c for c in chats if c['id'] == chat_id), None)
    if chat:
        return jsonify({"chat": chat})
    return jsonify({"error": "Chat not found"}), 404

# Update a specific chat entry by ID
@app.route("/update/<int:chat_id>", methods=["PUT"])
def update_chat_entry(chat_id):
    if g.user is None:
        return jsonify({"error": "Authentication required"}), 401
    data = request.get_json()
    new_question = data.get("question")
    new_response = data.get("response")

    if not new_question or not new_response:
        return jsonify({"error": "Both question and response are required"}), 400

    try:
        update_chat(chat_id, new_question, new_response)
        return jsonify({"message": "Chat updated successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Delete a chat entry by ID
@app.route("/delete/<int:chat_id>", methods=["DELETE"])
def delete_chat_entry(chat_id):
    if g.user is None:
        return jsonify({"error": "Authentication required"}), 401
    try:
        delete_chat(g.user[0], chat_id)
        return jsonify({"message": "Chat deleted successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ────────────────────────────────

if __name__ == "__main__":
    app.run(debug=True)
