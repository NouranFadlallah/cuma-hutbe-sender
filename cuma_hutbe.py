import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from pdf2image import convert_from_bytes
import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv

# === Load .env file ===
load_dotenv()


# === SETTINGS ===
languages = [e.strip() for e in os.getenv("LANGUAGES").split(",")]
url_dict = {"en": "https://dinhizmetleri.diyanet.gov.tr/kategoriler/yayinlarimiz/hutbeler/english-(ingilizce)",
            "ar": "https://dinhizmetleri.diyanet.gov.tr/kategoriler/yayinlarimiz/hutbeler/%D8%B9%D8%B1%D8%A8%D9%8A-(arap%C3%A7a)",
            "tr": "https://dinhizmetleri.diyanet.gov.tr/kategoriler/yayinlarimiz/hutbeler/t%C3%BCrk%C3%A7e",
            "ru": "https://dinhizmetleri.diyanet.gov.tr/kategoriler/yayinlarimiz/hutbeler/%D1%80%D1%83%D1%81%D1%81%D0%BA%D0%B8%D0%B9-(rus%C3%A7a)",
            "de": "https://dinhizmetleri.diyanet.gov.tr/kategoriler/yayinlarimiz/hutbeler/deutsche-(almanca)",
            "fr": "https://dinhizmetleri.diyanet.gov.tr/kategoriler/yayinlarimiz/hutbeler/fran%C3%A7ais-(frans%C4%B1zca)",
            "es": "https://dinhizmetleri.diyanet.gov.tr/kategoriler/yayinlarimiz/hutbeler/espanol-(ispanyolca)",
            "it": "https://dinhizmetleri.diyanet.gov.tr/kategoriler/yayinlarimiz/hutbeler/italiano-(italyanca)",
            "sq": "https://dinhizmetleri.diyanet.gov.tr/kategoriler/yayinlarimiz/hutbeler/shqiptare-(arnavut%C3%A7a)"
            }
urls = [url_dict[lang] for lang in languages]
sender_email = os.getenv("SENDER_EMAIL")
receiver_emails = [e.strip() for e in os.getenv("RECEIVER_EMAILS").split(",")]
app_password = os.getenv("APP_PASSWORD")
image_filename = "converted_page"


def fetch_pdf_and_save_image(url: str, num: int):
    # Fetch the page
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the table and extract the first data row with PDF link
    tables = soup.find_all('table')
    target_table = tables[1]  # Adjust index as needed

    pdf_url = None
    for row in target_table.find_all('tr'):
        if row.find('td'):
            link = row.find('a', href=True)
            if link:
                pdf_url = urljoin(url, link['href'])
                print("Found PDF link:", pdf_url)
                if " " in pdf_url:
                    pdf_url.replace(" ", "%20")
                    print("Fixed pdf url link:", pdf_url)
            break

    # Download the PDF
    if pdf_url:
        pdf_response = requests.get(pdf_url)
        pdf_response.raise_for_status()

        # Convert PDF to image
        images = convert_from_bytes(pdf_response.content)
        image = images[0]  # First (and only) page
        image.save(f"{image_filename}{num}.jpg", 'JPEG')
        print(f"Converted PDF to image: {image_filename}{num}.jpg")
        return True
    else:
        print("No PDF link found.")
        return None

def send_image_in_email(sender_email, receiver_email, num):
    # Email the image
    msg = EmailMessage()
    msg['Subject'] = "Here’s your latest file as an image"
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg.set_content("Attached is the latest document as an image.")

    for i in range(num):
        with open(f"{image_filename}{i}.jpg", 'rb') as f:
            msg.add_attachment(f.read(), maintype='image', subtype='jpeg', filename=f"{image_filename}{i}.jpg")

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(sender_email, app_password)
        smtp.send_message(msg)

    print("Email sent successfully.")

if __name__ == "__main__":

    for num, url in enumerate(urls):
        res = fetch_pdf_and_save_image(url, num)
        if not res:
            exit()

    for email in receiver_emails:
        send_image_in_email(sender_email, email, len(urls))
        print(f"✅ Email sent successfully to {email}")

    # Cleanup
    for i in range(len(urls)):
        os.remove(f"{image_filename}{i}.jpg")
