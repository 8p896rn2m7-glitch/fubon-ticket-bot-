import requests
import time
import hashlib

BOT_TOKEN = "8910259457:AAHpwewaaZUEwxw8uGF8E0A2VKaev2UPxu0"
CHAT_ID = "8699744629"

URL = "https://guardians.fami.life/UTK0204_"

CHECK_INTERVAL = 10  # 秒（建議 10~15）
TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

last_hash = None
fail_count = 0


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

        current_hash = hashlib.md5(text.encode()).hexdigest()

        # 第一次初始化
        if last_hash is None:
            last_hash = current_hash
            print("初始化完成，開始監控...")
            time.sleep(CHECK_INTERVAL)
            continue

        # 有變化 => 可能釋票
        if current_hash != last_hash:
            print("偵測到更新！")

            send_telegram(f"""🎫 富邦悍將疑似釋票！

🔗 {URL}
🕒 系統偵測頁面更新
""")

            last_hash = current_hash

        fail_count = 0  # 成功就歸零

    except Exception as e:
        fail_count += 1
        print(f"錯誤 ({fail_count}):", e)

        # 避免一直炸
        if fail_count >= 5:
            send_telegram("⚠️ 監控系統異常（連線失敗過多）")
            fail_count = 0

    time.sleep(CHECK_INTERVAL)
