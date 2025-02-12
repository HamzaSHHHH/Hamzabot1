import os
from telethon import TelegramClient, events
from telethon.sessions import StringSession

api_id = int(os.getenv("21794078"))  # جلب API_ID من المتغيرات البيئية
api_hash = os.getenv("7eb1bfa0ccbd88d1716b756ef23f3587")  # جلب API_HASH من المتغيرات البيئية
session_string = os.getenv("1BJWap1wBuwiHAk2P5Qy5Z8jgZOA6IJHZtWnC5gR9tnl4wR4QtrCHImuzrPXhnVngJK9oaQkMj0shaG9Ssct6Etc3j57KkKVG04Videzl6Mi7PvlFN3KkB2_p50FR92TTLf0WKHncOgmvJT4FlxSJvZn9FdrttEgOwJNPGr07CU05lhEVHxb3MzmEVuFfg3D93KrayHszH6AOlclP1iA7v3UoTO_Qomvb6_joGIY9Y7r-4jViEE2Uh1S9RQ7IWMqqZGXl_xOJBjGZYttx3BdYsLYOJTY-H4LeJiMgV7NmdFPgOvfWVr8gpM-0Mxlo_n2o7DbeBIBdfIPQV17I11iCVPlv1KMP2rM=")  # جلب الجلسة من المتغيرات البيئية

client = TelegramClient(StringSession(session_string), api_id, api_hash)

# معرف القناة للبحث
channel_username = "@MoviesHM9"

# رابط مجموعة الطلبات
REQUEST_GROUP_LINK = "https://t.me/Movies_group4"

# رسالة الترحيب
WELCOME_MESSAGE = f"""
مرحباً بك في بوت البحث عن الأفلام! 🎬

يمكنك استخدام الأمر التالي للبحث عن الأفلام:
/movie <اسم الفيلم>

مثال:
/movie Inception

سيقوم البوت بالبحث في القناة وإرسال النتائج لك. 😊

إذا لم يتم العثور على الفيلم، سيتم توجيهك إلى مجموعة الطلبات:
{REQUEST_GROUP_LINK}
"""

# رسالة توجيه إلى مجموعة الطلبات
REQUEST_MESSAGE = f"""
دورت كتير وما لقيت طلبك 😔
تأكد من الاسم واذا ما لقيتو 
بتقدر تطلب الفيلم من خلال كروب الطلبات 
{REQUEST_GROUP_LINK}
"""

@client.on(events.NewMessage(pattern='/start'))
async def start_handler(event):
    await event.reply(WELCOME_MESSAGE)

@client.on(events.NewMessage(pattern=r'/movie\s+(.+)'))
async def movie_handler(event):
    movie_name = event.pattern_match.group(1).strip()
    print(f"تم استلام طلب بحث عن فيلم: {movie_name}")

    # البحث في القناة
    results = await client.get_messages(
        entity=channel_username,
        limit=15,
        search=movie_name
    )
    
    if results:
        reversed_results = list(reversed(results))
        await event.reply(f"تم العثور على {len(results)} نتيجة...")
        
        for msg in reversed_results:
            if msg.media:
                await client.send_file(
                    event.chat_id,
                    msg.media,
                    caption=msg.text or ""
                )
    else:
        await event.reply(REQUEST_MESSAGE)

def main():
    print("جارِ بدء البوت...")
    try:
        client.start()
        print("تم تسجيل الدخول بنجاح. البوت في انتظار الطلبات...")
        client.run_until_disconnected()
    except Exception as e:
        print(f"حدث خطأ: {e}")

if __name__ == "__main__":
    main()
