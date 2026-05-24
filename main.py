import requests
import time

BOT_TOKEN = "8910259457:AAHpwewaaZUEwxw8uGF8E0A2VKaev2UPxu0"
CHAT_ID = "8699744629"

URL = "https://guardians.fami.life/UTK0204_"

sent = False

while True:
    try:
        r = requests.get(URL)
        text = r.text

        keywords = [
            "內野",
            "B1",
            "A1"
        ]

        found = any(k in text for k in keywords)

        if found and not sent:
            message = f"""
🎫 富邦悍將可能有釋票！

立即查看：
{URL}
"""

            api = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

            requests.post(api, data={
                "chat_id": CHAT_ID,
                "text": message
            })

            sent = True

        time.sleep(30)

    except Exception as e:
        print(e)
        time.sleep(30)
