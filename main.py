import requests
import time

BOT_TOKEN = "8910259457:AAHpwewaaZUEwxw8uGF8E0A2VKaev2UPxu0"
CHAT_ID = "8699744629"

TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

CHECK_INTERVAL = 10


targets = [
    {
        "name": "富邦場",
        "url": "https://guardians.fami.life/UTK0204_",
        "zones": ["B1_108","B1_109","B1_110","B1_112","B1_113","B1_114","B1_116","B1_117","B1_118","內野"]
    },
    {
        "name": "ibon新場",
        "url": "https://orders.ibon.com.tw/application/UTK02/UTK0201_000.aspx?PERFORMANCE_ID=B0B5MPY0&PRODUCT_ID=B0B5LWGN&strItem=WEB網站入口1",
        "zones": ["A1","A2","A3"]
    }
]


state = {
    t["url"]: {"found": set(), "fail": 0}
    for t in targets
}


def send(msg):
    try:
        requests.post(
            TELEGRAM_API,
            data={"chat_id": CHAT_ID, "text": msg},
            timeout=10
        )
    except:
        pass


def fetch(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(url, headers=headers, timeout=10)
    return r.text


while True:
    for t in targets:
        url = t["url"]
        name = t["name"]
        zones = t["zones"]

        try:
            text = fetch(url)

            found = {z for z in zones if z in text}

            prev = state[url]["found"]

            added = found - prev
            removed = prev - found

            # 🔥 有變化才通知
            if added:
                msg = f"🎫 釋票更新｜{name}\n\n"
                msg += "🆕 新出現區域：\n"
                msg += "\n".join(sorted(added))
                msg += f"\n\n🔗 {url}"

                send(msg)

            # 更新狀態
            state[url]["found"] = found
            state[url]["fail"] = 0

        except Exception as e:
            state[url]["fail"] += 1
            print(f"{name} error:", e)

            # 連續失敗提醒
            if state[url]["fail"] == 5:
                send(f"⚠️ {name} 監控異常（連線失敗）")

    time.sleep(CHECK_INTERVAL)
