import requests
import selectorlib
import smtplib
import ssl
import time

def scrape(url):
    """ Scrape the page source from the URL"""
    response = requests.get(url)
    source = response.text
    return source

def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(source)["tours"]   # tours the name of text inside the extract.yaml file
    return value

def send_email(message):
    port = 465   # For ssl

    PASSWORD = "oymabiteixnekwwv"
    SENDER = "mypythonprotfolio@gmail.com"
    RECEIVER = "mypythonprotfolio@gmail.com"

    context = ssl.create_default_context()   # Create a secure ssl context

    email_message = f"Subject: New upcoming tour was found\n\n{message}"

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(SENDER, PASSWORD)
        server.sendmail(SENDER, RECEIVER, email_message)
    print("Email was sent")


def store(extracted):
    with open("data.txt", "a") as file:
        file.write(extracted + "\n")

def read(extracted):
    with open("data.txt", "r") as file:
        text = file.read()
    return text

URL = "https://programmer100.pythonanywhere.com/tours/"

if __name__ == "__main__":
    while True:
      scraped = scrape(URL)
      extracted = extract(scraped)
      print(extracted)
      content = read(extracted)
      if extracted != "No upcoming tours":
          if extracted not in content:
              store(extracted)
              send_email(extracted)
      time.sleep(2)   # every 2 seconds the program checks for a new tour