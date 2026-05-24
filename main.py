import requests
import time
import hashlib

BOT_TOKEN = "8910259457:AAHpwewaaZUEwxw8uGF8E0A2VKaev2UPxu0"
CHAT_ID = "8699744629"

URL = "https://guardians.fami.life/UTK0204_"

CHECK_INTERVAL = 8  # 🔥 更接近秒級
TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

# 🎯 熱門區優先排序（越前面越重要）
priority_zones = [
    # B1 熱門
    "B1_108", "B1_109", "B1_110",
    "B1_112", "B1_113", "B1_114",
    "B1_116", "B1_117", "B1_118",

    # 次熱門
    "B1_111", "B1_115",

    # 一般 B1
    "B1_102", "B1_103", "B1_106", "B1_120", "B1_123", "B1_124",

    # L2
    "L2-211", "L2_212", "L2-214", "L2_215",

    # L4
    "L4_401", "L4-402", "L4_403", "L4-404", "L4_405", "L4_406",
    "L4_407", "L4_408", "L4_410", "L4_411", "L4_412", "L4_413",
    "L4_414", "L4_415", "L4_416", "L4_417",

    # L5
    "L5_503", "L5_504", "L5_505", "L5_506", "L5_507", "L5_508",
    "L5_509", "L5_510", "L5_511", "L5_512", "L5_513", "L5_514", "L5_515"
]

last_hash = None
last_found = set()


def send(msg):
    try:
        requests.post(
            TELEGRAM_API,
            data={"chat_id": CHAT_ID, "text": msg},
            timeout=10
        )
    except:
        pass


while True:
    try:
        r = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        text = r.text

        current_hash = hashlib.md5(text.encode()).hexdigest()

        # 找出目前出現的區
        found = {z for z in priority_zones if z in text}

        if last_hash is None:
            last_hash = current_hash
            last_found = found
            print("初始化完成")
            time.sleep(CHECK_INTERVAL)
            continue

        # 🔥 只抓「新出現的區」
        new_found = found - last_found

        if current_hash != last_hash and new_found:
            # 按優先順序排序
            ordered = [z for z in priority_zones if z in new_found]

            msg = "🎫 富邦悍將釋票（PRO監控）\n\n"
            msg += "🔥 新釋出熱門區：\n"
            msg += "\n".join(ordered)
            msg += f"\n\n🔗 {URL}"

            send(msg)

            print("通知:", ordered)

        last_hash = current_hash
        last_found = found

    except Exception as e:
        print("錯誤:", e)

    time.sleep(CHECK_INTERVAL)
