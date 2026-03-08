import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
import os
import json

URLS = {
    "Black": "https://www.cricketwireless.com/shop/smartphones/apple-iphone-16e-128gb-black",
    "White": "https://www.cricketwireless.com/shop/smartphones/apple-iphone-16e-128gb-white"
}

EMAIL_FROM = os.environ["EMAIL_FROM"]
EMAIL_TO = os.environ["EMAIL_TO"]
EMAIL_PASSWORD = os.environ["EMAIL_PASSWORD"]

ALERT_FILE = "alerted.json"

headers = {
    "User-Agent": "Mozilla/5.0"
}


def send_email(color, link):

    body = f"""
Stock available!

Model: iPhone 16e 128GB {color}

Buy here:
{link}
"""

    msg = MIMEText(body)
    msg["Subject"] = f"iPhone Stock Alert ({color})"
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(EMAIL_FROM, EMAIL_PASSWORD)
    server.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())
    server.quit()


def load_alerts():
    if os.path.exists(ALERT_FILE):
        with open(ALERT_FILE) as f:
            return json.load(f)
    return {}


def save_alerts(data):
    with open(ALERT_FILE, "w") as f:
        json.dump(data, f)


def is_available(html):

    soup = BeautifulSoup(html, "html.parser")

    # Look for Add to Cart button
    buttons = soup.find_all("button")

    for b in buttons:
        text = b.get_text().lower()
        if "add to cart" in text or "buy now" in text:
            if not b.has_attr("disabled"):
                return True

    return False


def check_stock():

    alerted = load_alerts()

    for color, url in URLS.items():

        r = requests.get(url, headers=headers)
        available = is_available(r.text)

        print(color, "available:", available)

        if available and not alerted.get(color):

            send_email(color, url)
            alerted[color] = True

    save_alerts(alerted)


check_stock()
