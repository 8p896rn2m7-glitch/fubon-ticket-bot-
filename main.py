import requests
import time
import datetime
BOT_TOKEN = "8910259457:AAHpwewaaZUEwxw8uGF8E0A2VKaev2UPxu0"
CHAT_ID = "8699744629"
TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
CHECK_INTERVAL = 8
target = {
    "name": "富邦悍將",
    "url": "https://guardians.fami.life/UTK0204_",
    "zones": [
        "B1_108","B1_109","B1_110",
        "B1_112","B1_113","B1_114",
        "B1_116","B1_117","B1_118",
        "B1_111","B1_115",
        "B1_102","B1_103","B1_106",
        "B1_120","B1_123","B1_124",
        "L2-211","L2_212","L2-214","L2_215",
        "L4_401","L4-402","L4_403","L4-404",
        "L4_405","L4_406","L4_407","L4_408",
        "L4_410","L4_411","L4_412","L4_413",
        "L4_414","L4_415","L4_416","L4_417",
        "L5_503","L5_504","L5_505","L5_506",
        "L5_507","L5_508","L5_509","L5_510",
        "L5_511","L5_512","L5_513","L5_514",
        "L5_515"
    ]
}
state_found = set()
def send(msg):
    try:
        requests.post(
            TELEGRAM_API,
            data={
                "chat_id": CHAT_ID,
                "text": msg
            },
            timeout=10
        )
    except Exception as e:
        print("Telegram error:", e)
def fetch(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    try:
        r = requests.get(
            url,
            headers=headers,
            timeout=10
        )
        return r.text
    except Exception as e:
        print("Fetch error:", e)
        return ""
def is_valid(text, zone):
    """
    區域附近判斷
    """
    idx = text.find(zone)
    if idx == -1:
        return False
    # 只看區域附近內容
    context = text[idx:idx + 120]
    print("======")
    print(zone)
    print(context)
    # 排除輪椅席
    if "輪椅" in context:
        return False
    # 排除售完
    bad_words = [
        "售完",
        "已售完",
        "無票",
        "不可選",
        "disabled"
    ]
    for b in bad_words:
        if b in context:
            return False
    return True
# 啟動通知
send("✅ 富邦監控已啟動")
while True:
    try:
        text = fetch(target["url"])
        print("HTML長度:", len(text))
        if not text:
            time.sleep(CHECK_INTERVAL)
            continue
        found = set()
        for z in target["zones"]:
            if is_valid(text, z):
                found.add(z)
        new = found - state_found
        if new:
            msg = f"""🎫 富邦悍將釋票通知
🏟 主場例行賽｜臺北大巨蛋
🟢 可購買區：
"""
            for z in sorted(new):
                msg += f"🟢 {z}\n"
            msg += f"""
⏰ 檢查時間：
{datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')}
🔗 購票連結：
{target['url']}
"""
            send(msg)
            print("NEW:", new)
        state_found = found
    except Exception as e:
        print("Main loop error:", e)
    time.sleep(CHECK_INTERVAL)
