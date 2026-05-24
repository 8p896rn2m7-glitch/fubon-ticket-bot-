import requests
import time

BOT_TOKEN = "8910259457:AAHpwewaaZUEwxw8uGF8E0A2VKaev2UPxu0"
CHAT_ID = "8699744629"

TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

CHECK_INTERVAL = 8


targets = [
    {
        "name": "富邦悍將",
        "url": "https://guardians.fami.life/UTK0204_",
        "zones": [
            "B1_108","B1_109","B1_110","B1_112","B1_113","B1_114",
            "B1_116","B1_117","B1_118",
            "B1_111","B1_115",
            "B1_102","B1_103","B1_106","B1_120","B1_123","B1_124",
            "L2-211","L2_212","L2-214","L2_215",
            "L4_401","L4-402","L4_403","L4-404","L4_405","L4_406",
            "L4_407","L4_408","L4_410","L4_411","L4_412","L4_413",
            "L4_414","L4_415","L4_416","L4_417",
            "L5_503","L5_504","L5_505","L5_506","L5_507","L5_508",
            "L5_509","L5_510","L5_511","L5_512","L5_513","L5_514","L5_515"
        ]
    },
    {
        "name": "耀燮場",
        "url": "https://orders.ibon.com.tw/application/UTK02/UTK0201_000.aspx?PERFORMANCE_ID=B0B5MPY0&PRODUCT_ID=B0B5LWGN&strItem=WEB網站入口1",
        "zones": ["A2"]
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

            if added:
                msg = f"🎫 釋票通知｜{name}\n\n"
                msg += "🔥 新釋出區域：\n"
                msg += "\n".join(sorted(added))
                msg += f"\n\n🔗 {url}"

                send(msg)

                print(name, ":", added)

            state[url]["found"] = found
            state[url]["fail"] = 0

        except Exception as e:
            state[url]["fail"] += 1
            print(name, "error:", e)

            if state[url]["fail"] == 5:
                send(f"⚠️ {name} 監控異常")

    time.sleep(CHECK_INTERVAL)
