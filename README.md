# 🤖 Telegram Messaging Assistant Bot 
**بوت تليجرام المساعد لإعادة توجيه الرسائل**

[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![python-telegram-bot](https://img.shields.io/badge/python--telegram--bot-v21.x-success.svg)](https://python-telegram-bot.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[English](#english) | [العربية](#arabic)

---

<a name="english"></a>
## 🌐 English Description
A personal Telegram bot that acts as a middleman for communication. When users message the bot, the owner is notified and can reply to them directly through the bot. All user data, blocks, and states are kept in memory without the need for an external database.

### ✨ Features
* **Bilingual Support**: Automatically detects the user's language (Arabic/English) and responds accordingly.
* **Message Forwarding**: Forwards text, photos, voice notes, stickers, and documents to the owner with user details.
* **Reply System**: Simple `/reply <user_id> <message>` command for the owner.
* **Blocking System**: Owner can block/unblock users dynamically using `/block` and `/unblock`.
* **Typing Indicator**: Shows "typing..." action for 1 second before forwarding to make the bot feel responsive.

### 🚀 Installation & Run
1. Install dependencies:
   ```bash
   pip install python-telegram-bot python-dotenv
   ```
2. Copy `.env.example` to `.env` and fill in your details (`BOT_TOKEN`, `OWNER_ID`, `OWNER_NAME`).
3. Run the bot:
   ```bash
   python bot.py
   ```

### 👨‍💻 Developer
Developed by **Omar Luay**.

[![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/Asteroid404)
[![Instagram](https://img.shields.io/badge/Instagram-E4405F?style=for-the-badge&logo=instagram&logoColor=white)](https://www.instagram.com/42l6)

---

<a name="arabic"></a>
## 🌍 العربية (Arabic Description)
بوت شخصي على تليجرام يعمل كوسيط للتواصل. عندما يرسل المستخدمون رسالة إلى البوت، يتم إخطار المالك ويمكنه الرد عليهم مباشرة من خلال البوت. يتم حفظ جميع بيانات وحظر المستخدمين في الذاكرة دون الحاجة لقاعدة بيانات خارجية.

### ✨ المميزات
* **دعم ثنائي اللغة**: يتعرف تلقائيًا على لغة المستخدم (العربية/الإنجليزية) ويتفاعل بناءً عليها.
* **إعادة توجيه الرسائل**: إعادة توجيه النصوص والصور والتسجيلات الصوتية والملصقات والمستندات إلى المالك مع تفاصيل المرسل.
* **نظام الرد**: أمر بسيط للمالك `/reply <user_id> <الرسالة>` للرد مباشرة.
* **نظام الحظر**: يمكن للمالك حظر أو إلغاء حظر المستخدمين ديناميكيًا باستخدام `/block` و `/unblock`.
* **مؤشر الكتابة**: يظهر حالة "يكتب الآن..." لمدة ثانية قبل إعادة التوجيه لتبدو استجابة البوت طبيعية وسريعة.

### 🚀 التثبيت والتشغيل
1. تثبيت المكتبات المطلوبة:
   ```bash
   pip install python-telegram-bot python-dotenv
   ```
2. انسخ ملف الإعدادات `.env.example` إلى اسم `.env` وقم بتعبئة بياناتك.
3. تشغيل البوت:
   ```bash
   python bot.py
   ```

### 👨‍💻 المطور والتواصل
تم التطوير بواسطة **عمر لؤي (Omar Luay)**.

[![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/Asteroid404)
[![Instagram](https://img.shields.io/badge/Instagram-E4405F?style=for-the-badge&logo=instagram&logoColor=white)](https://www.instagram.com/42l6)
