from flask import Flask
import requests
import feedparser

app = Flask(__name__)

BOT_TOKEN = "8157752553:AAFPbfwjZS5J_SohGQiKNl1COwdCGYU4wvY"
CHAT_ID = "-4824341433"

RSS_FEEDS = {
    "BBC": "https://feeds.bbci.co.uk/news/business/rss.xml",
    "Investing": "https://www.investing.com/rss/news.rss"
}

sent_links = set()

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }
    return requests.post(url, json=payload)

@app.route("/run", methods=["GET"])
def run_bot():
    for name, url in RSS_FEEDS.items():
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers)
        feed = feedparser.parse(r.content)
        for entry in feed.entries[:3]:
            title = entry.title
            link = entry.link
            if link not in sent_links:
                msg = f"<b>{title}</b>\n{link}"
                send_message(msg)
                sent_links.add(link)
    return "Správy odoslané."
