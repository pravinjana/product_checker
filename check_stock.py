import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
import os

URLS = [
    "https://www.cricketwireless.com/shop/smartphones/apple-iphone-16e-128gb-black",
    "https://www.cricketwireless.com/shop/smartphones/apple-iphone-16e-128gb-white"
]

EMAIL_FROM = os.environ["EMAIL_FROM"]
EMAIL_TO = os.environ["EMAIL_TO"]
EMAIL_PASSWORD = os.environ["EMAIL_PASSWORD"]

def send_email(link):
    msg = MIMEText(f"Stock available!\n\nBuy here: {link}")
    msg["Subject"] = "iPhone Back in Stock"
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(EMAIL_FROM, EMAIL_PASSWORD)
    server.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())
    server.quit()

def check_stock():

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    for url in URLS:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        page_text = soup.get_text().lower()

        if "notify me when it's back in stock" not in page_text:
            send_email(url)
            print("Stock detected")
            return

    print("Still out of stock")

check_stock()
