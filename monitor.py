"""A program for monitoring campground availability at Yellowstone."""
import time
import threading
from threading import Event
import smtplib
import signal
from email.mime.text import MIMEText
import requests
import json
from bs4 import BeautifulSoup
from config import sender_email, sender_password, recipient_emails

SENDER_EMAIL = sender_email 
SENDER_PASSWORD = sender_password # if using Gmail, check https://support.google.com/accounts/answer/185833
RECIPIENT_EMAILS = recipient_emails # list of recipients' emails, e.g., ["waleyz@umich.edu", "waley_zheng@sjtu.edu.cn"]
UPDATE_INTERVAL = 15  # Time to wait between requests in seconds

exit = Event()


class Monitor:
    """A Web page monitor."""

    def monitor_run(self):
        """Run monitor thread."""
        while not exit.is_set():
            try:
                response = requests.get("https://webapi.xanterra.net/v1/api/availability/hotels/yellowstonenationalparklodges/YLYC:RV?date=08/01/2022&is_group=false&nights=1")
                data = response.json()
                response.raise_for_status()
                min13 = data["availability"]["08/13/2022"]["YLYC:RV"]["min"]
                min14 = data["availability"]["08/14/2022"]["YLYC:RV"]["min"]
            except (requests.exceptions.RequestException, requests.exceptions.HTTPError, json.JSONDecodeError, KeyError) as e:
                print(f"ERROR: {e}")
                exit.wait(UPDATE_INTERVAL)
                continue

            # print query result
            t = time.localtime()
            current_time = time.strftime("%H:%M:%S", t)
            print(f"{current_time} min is ${min13} ${min14}.")
            if min13 * min14 == 0:
                exit.wait(UPDATE_INTERVAL)
            else:
                print("Campground is available now!")
                msg = MIMEText("Book Canyon Campground now!\nhttps://secure.yellowstonenationalparklodges.com/booking/lodging-search?destination=ALL&adults=1&children=0&infants=0&animals=0&rateCode=&rateType=&nights=2&dateFrom=08-13-2022")
                msg["Subject"] = f"[Canyon Campground] Booking Reminder"
                msg["From"] = f"Hongxiao Zheng <{SENDER_EMAIL}>"
                msg["To"] = ", ".join(RECIPIENT_EMAILS)
                s = smtplib.SMTP("smtp.gmail.com", 587)
                s.starttls()
                s.login(SENDER_EMAIL, SENDER_PASSWORD)
                s.sendmail(SENDER_EMAIL, RECIPIENT_EMAILS, msg.as_string())
                s.quit()
                break

    def __init__(self):
        threading.Thread(target=self.monitor_run).start()


def quit(signo, _frame):
    """Handle interuptions."""
    print(f"Interrupted by {signo}, shutting down")
    exit.set()


def main():
    """Run multiple monitors."""
    Monitor()


if __name__ == "__main__":
    for sig in ("TERM", "HUP", "INT"):
        signal.signal(getattr(signal, "SIG"+sig), quit)
    main()
