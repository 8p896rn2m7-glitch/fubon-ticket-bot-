import requests
import time
import hashlib

BOT_TOKEN = "8910259457:AAHpwewaaZUEwxw8uGF8E0A2VKaev2UPxu0"
CHAT_ID = "8699744629"

URL = "https://guardians.fami.life/UTK0204_"

CHECK_INTERVAL = 10
TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

last_hash = None
last_found = False


def send_telegram(msg):
    try:
        requests.post(
            TELEGRAM_API,
            data={
                "chat_id": CHAT_ID,
                "text": msg
            },
            timeout=10
        )
    except:
        pass


while True:
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        r = requests.get(URL, headers=headers, timeout=10)
        text = r.text

        # 只看「內野」
        found_infield = "內野" in text

        current_hash = hashlib.md5(text.encode()).hexdigest()

        # 初始化
        if last_hash is None:
            last_hash = current_hash
            last_found = found_infield
            print("初始化完成")
            time.sleep(CHECK_INTERVAL)
            continue

        # 條件：內野出現 + 頁面有更新
        if found_infield and (current_hash != last_hash or not last_found):
            print("🎫 內野釋票偵測到！")

            send_telegram(f"""🎫 內野釋票！

🔗 {URL}
""")

            last_hash = current_hash
            last_found = True

        # 如果內野消失，狀態重置
        if not found_infield:
            last_found = False

    except Exception as e:
        print("錯誤:", e)

    time.sleep(CHECK_INTERVAL)
