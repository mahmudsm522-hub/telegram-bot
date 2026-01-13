import os
import time
import telebot
from fpdf import FPDF

# ================== CONFIG ==================
TOKEN = os.getenv("BOT_TOKEN")   # <<< SA TOKEN DAGA BOTFATHER
ADMIN_ID = 6648308251              # <<< SA TELEGRAM ID NAKA (BA USERNAME BA)

bot = telebot.TeleBot(TOKEN)

# ================== DATA ==================
users = {}

python_questions = [
    {"q": "Which keyword is used to print in Python?", "a": "print"},
    {"q": "How do you create a list in Python? (just symbols)", "a": "[]"},
    {"q": "Which keyword is used to define a function?", "a": "def"},
    {"q": "Which data type uses {} ?", "a": "dict"},
]

# ================== START ==================
@bot.message_handler(commands=["start"])
def start(message):
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, "👋 Welcome! Please enter your name:")
    bot.register_next_step_handler(msg, get_name)

def get_name(message):
    chat_id = message.chat.id
    users[chat_id] = {
        "name": message.text.strip(),
        "score": 0,
        "q_index": 0,
        "attempts": 0
    }
    bot.send_message(chat_id, f"Nice to meet you, {message.text.strip()} 😊")
    show_main_menu(chat_id)

# ================== MAIN MENU ==================
def show_main_menu(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("/Python", "/Physics", "/Profile")

    bot.send_message(chat_id, "📌 Choose an option:", reply_markup=markup)

    links = types.InlineKeyboardMarkup()
    links.add(
        types.InlineKeyboardButton("🌐 Facebook", url="https://www.facebook.com/share/1GWma4DRsg/"),
        types.InlineKeyboardButton("📣 Telegram Channel", url="https://t.me/Mahmudsm1"),
        types.InlineKeyboardButton("🐦 X (Twitter)", url="https://x.com/Mahmud_sm1"),
    )
    bot.send_message(chat_id, "🔗 My Links:", reply_markup=links)

# ================== ABOUT / PROFILE ==================
@bot.message_handler(commands=["Profile"])
def profile(message):
    chat_id = message.chat.id
    if chat_id in users:
        u = users[chat_id]
        bot.send_message(chat_id, f"👤 Name: {u['name']}\n🏆 Score: {u['score']}")
    else:
        bot.send_message(chat_id, "⚠️ Use /start first")

# ================== PHYSICS ==================
@bot.message_handler(commands=["Physics"])
def physics(message):
    text = (
        "📚 PHYSICS\n\n"
        "Physics is the branch of science that studies matter, energy, motion, force, space and time.\n\n"
        "It teaches us about:\n"
        "- Motion\n"
        "- Energy\n"
        "- Electricity\n"
        "- Light\n"
        "- Atoms\n"
        "- Universe"
    )
    bot.send_message(message.chat.id, text)

# ================== PYTHON QUIZ ==================
@bot.message_handler(commands=["Python"])
def start_python_quiz(message):
    chat_id = message.chat.id
    if chat_id not in users:
        bot.send_message(chat_id, "⚠️ Use /start first")
        return

    users[chat_id]["score"] = 0
    users[chat_id]["q_index"] = 0
    users[chat_id]["attempts"] = 0

    bot.send_message(chat_id, "🐍 Python Quiz Started!")
    ask_question(chat_id)

def ask_question(chat_id):
    idx = users[chat_id]["q_index"]

    if idx >= len(python_questions):
        score = users[chat_id]["score"]
        total = len(python_questions)

        if score == total:
            bot.send_message(chat_id, "🎓 Congratulations! You passed all questions and earned a certificate! 🏆")
        else:
            bot.send_message(chat_id, f"❌ Quiz finished. Your score: {score}/{total}")

        show_main_menu(chat_id)
        return

    q = python_questions[idx]["q"]
    msg = bot.send_message(chat_id, f"❓ Question {idx+1}: {q}")
    bot.register_next_step_handler(msg, check_answer)

def check_answer(message):
    chat_id = message.chat.id
    answer = message.text.strip().lower()

    idx = users[chat_id]["q_index"]
    correct = python_questions[idx]["a"].lower()

    if answer == correct:
        users[chat_id]["score"] += 1
        users[chat_id]["q_index"] += 1
        users[chat_id]["attempts"] = 0
        bot.send_message(chat_id, "✅ Correct!")
    else:
        users[chat_id]["attempts"] += 1
        if users[chat_id]["attempts"] >= 3:
            bot.send_message(chat_id, f"❌ Failed! Correct answer was: {correct}")
            users[chat_id]["q_index"] += 1
            users[chat_id]["attempts"] = 0
        else:
            bot.send_message(chat_id, f"⚠️ Wrong! Try again. Attempts left: {3 - users[chat_id]['attempts']}")
            ask_question(chat_id)
            return

    ask_question(chat_id)

# ================== ADMIN BROADCAST ==================
@bot.message_handler(commands=["send"])
def admin_send(message):
    if message.chat.id != ADMIN_ID:
        bot.send_message(message.chat.id, "❌ Access Denied")
        return

    msg = bot.send_message(message.chat.id, "✍️ Send the message you want to broadcast:")
    bot.register_next_step_handler(msg, broadcast)

def broadcast(message):
    if message.chat.id != ADMIN_ID:
        return

    for uid in users.keys():
        try:
            bot.send_message(uid, f"📢 Admin Message:\n{message.text}")
        except:
            pass

    bot.send_message(message.chat.id, "✅ Message sent to all users!")

# ================== RUN ==================
print("🤖 Bot is running...")
bot.infinity_polling()
