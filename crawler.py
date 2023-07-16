"""
Crawler for some show

MiaoTony
"""

import requests
import time
import datetime
import random


last_success_time = datetime.datetime.now()


def crawl():
    project_id = 73710
    url = "https://sh"+"ow.bi" + "lib" + "ili.com/api/ti" + \
        f"cket/project/get?version=134&id={project_id}&project_id={project_id}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    # proxies = {"https": "socks5://127.0.0.1:7890"}
    r = requests.get(url, headers=headers)  # proxies=proxies
    r.encoding = "utf-8"

    # print(r.text)
    r_json = r.json()
    sale_flag = r_json["data"]["sale_flag"]
    time_now = datetime.datetime.now()
    print("====>", time_now, sale_flag)
    if sale_flag not in ["暂时售罄", "已售罄"]:
        action_success(r_json, time_now)


def action_success(resp, time_now):
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print(resp["data"]["sale_flag_number"])
    screen_list = resp["data"]["screen_list"]
    # print(screen_list)

    # parse detailed ticket info
    desc = ""
    for screen in screen_list:
        day_name = screen["name"]
        if screen["clickable"] == True:
            for ticket in screen["ticket_list"]:
                if ticket['clickable'] == True:
                    desc += f"{ticket['screen_name']}_{ticket['desc']}: {ticket['num']}\n"
    print(desc)
    with open('bilibilishow.log', 'a+', encoding='utf-8') as f:
        f.write(
            f'{time_now} {resp["data"]["sale_flag"]}, {resp["data"]["sale_flag_number"]}\n{screen_list}\n')
        f.write(f'{desc}\n')

    global last_success_time
    if time_now - last_success_time > datetime.timedelta(seconds=10):
        last_success_time = time_now
        desp = f"""
*有票啦！*
{time_now} {resp["data"]["sale_flag"]}, {resp["data"]["sale_flag_number"]}

{desc}
""".strip()
        telegram_push("【MongoliaB】", desp)


def telegram_push(text, desp):
    """
    Telegram push
    """
    # Insert your telegram bot token and your id here.
    TOKEN = "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
    tg_chat_ids = ['123456789']
    telegram_URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    tmp = f"*{text}*\n{desp}"

    for tg_chat_id in tg_chat_ids:
        payload = {'chat_id': tg_chat_id,
                   'text': tmp, 'parse_mode': 'Markdown'}
        # proxies = {"https": "socks5://127.0.0.1:7890"}
        r = requests.post(telegram_URL, data=payload)  # proxies=proxies
        print(r.text)


if __name__ == "__main__":
    while True:
        try:
            crawl()
            time.sleep(1 + random.random())
        except Exception as e:
            print(e)
            with open('bilibilishow.log', 'a+', encoding='utf-8') as f:
                f.write(f'{datetime.datetime.now()} [!] ERROR!\n{e}\n')
