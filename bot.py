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
from googletrans import Translator

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

# OpenAI API Key
OPENAI_API_KEY = "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"  # استبدل هذا بمفتاحك

# Numverify API Key
NUMVERIFY_API_KEY = "8d6ce257e7b6502633705e2330fd0439"  # استبدل هذا بمفتاحك المجاني

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
    GETTING_TEXT_TO_TRANSLATE,
    GETTING_CODE_TO_FIX,
) = range(12)

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
    [InlineKeyboardButton("ترجمة إلى العربية 🌍", callback_data='translate_text'), InlineKeyboardButton("تصحيح أكواد برمجة 🤖", callback_data='fix_code')],
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

# ======================== ميزة الترجمة ========================

async def translate_text(update: Update, context) -> int:
    """Ask user for text to translate"""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        "🌍 الرجاء إرسال النص الذي تريد ترجمته إلى العربية:\n\nمثال: Hello, how are you?",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]])
    )
    return GETTING_TEXT_TO_TRANSLATE

async def get_translation(update: Update, context) -> int:
    """Translate text to Arabic"""
    text = update.message.text.strip()
    
    if not text:
        await update.message.reply_text(
            "❌ الرجاء إرسال نص صحيح للترجمة.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]])
        )
        return GETTING_TEXT_TO_TRANSLATE
    
    try:
        translator = Translator()
        translation = translator.translate(text, dest='ar')
        
        result = f"""
🌍 **الترجمة إلى العربية**

📝 **النص الأصلي:**
{text}

🔤 **اللغة الأصلية:** {translation.src}

📖 **الترجمة:**
{translation.text}

📊 **معلومات إضافية:**
• درجة الثقة: {translation.pronunciation if translation.pronunciation else 'غير متوفرة'}
"""
        
        await update.message.reply_text(
            result,
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔄 ترجمة نص آخر", callback_data='translate_text')],
                [InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]
            ])
        )
        
    except Exception as e:
        await update.message.reply_text(
            f"⚠️ حدث خطأ أثناء الترجمة: {e}\nالرجاء المحاولة مرة أخرى.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔄 إعادة المحاولة", callback_data='translate_text')],
                [InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]
            ])
        )
    
    return CHOOSING_MAIN_MENU

# ======================== ميزة تصحيح الأكواد ========================

async def fix_code(update: Update, context) -> int:
    """Ask user for code to fix"""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        "🤖 الرجاء إرسال الكود البرمجي الذي تريد تصحيحه:\n\n"
        "📌 **ملاحظة:** سيتم استخدام OpenAI API لتحليل وتصحيح الكود.",
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]])
    )
    return GETTING_CODE_TO_FIX

async def get_fixed_code(update: Update, context) -> int:
    """Fix code using OpenAI API"""
    code = update.message.text.strip()
    
    if not code:
        await update.message.reply_text(
            "❌ الرجاء إرسال كود برمجي صحيح.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]])
        )
        return GETTING_CODE_TO_FIX
    
    if OPENAI_API_KEY == "YOUR_OPENAI_API_KEY":
        await update.message.reply_text(
            "⚠️ **تنبيه:** لم يتم إعداد مفتاح OpenAI API.\n\n"
            "الرجاء إضافة مفتاح API في الكود ثم إعادة التشغيل.\n\n"
            "💡 **بديل:** يمكنك استخدام هذا الكود للاختبار:",
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔄 إعادة المحاولة", callback_data='fix_code')],
                [InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]
            ])
        )
        return CHOOSING_MAIN_MENU
    
    try:
        # إرسال رسالة "جاري المعالجة"
        processing_msg = await update.message.reply_text("⏳ جاري تحليل الكود وتصحيحه...")
        
        # استخدام OpenAI API لتصحيح الكود
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }
        
        prompt = f"""
قم بتحليل الكود التالي وقم بتصحيح أي أخطاء موجودة فيه.

**قواعد التصحيح:**
1. إذا كان الكود صحيح 100%، اكتب فقط: "✅ كود صحيح مايحتاج تعديل"
2. إذا كان هناك أخطاء، قم بتصحيحها واشرح الأخطاء التي تم إصلاحها
3. أرسل الكود المصحح فقط مع شرح بسيط

**الكود المراد تحليله:**
