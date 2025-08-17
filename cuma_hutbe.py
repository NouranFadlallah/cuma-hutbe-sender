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
url = "https://dinhizmetleri.diyanet.gov.tr/kategoriler/yayinlarimiz/hutbeler/english-(ingilizce)"
sender_email = os.getenv("SENDER_EMAIL")
receiver_email = os.getenv("RECEIVER_EMAIL")
app_password = os.getenv("APP_PASSWORD")
image_filename = "converted_page.jpg"


# === STEP 1: Fetch the page ===
response = requests.get(url)
response.raise_for_status()
soup = BeautifulSoup(response.text, 'html.parser')

# === STEP 2: Find the table and extract the first data row with PDF link ===
tables = soup.find_all('table')
target_table = tables[1]  # Adjust index as needed

pdf_url = None
for row in target_table.find_all('tr'):
    if row.find('td'):
        link = row.find('a', href=True)
        if link:
            pdf_url = urljoin(url, link['href'])
            print("Found PDF link:", pdf_url)
        break

# === STEP 3: Download the PDF ===
if pdf_url:
    pdf_response = requests.get(pdf_url)
    pdf_response.raise_for_status()

    # === STEP 4: Convert PDF to image ===
    images = convert_from_bytes(pdf_response.content)
    image = images[0]  # First (and only) page
    image.save(image_filename, 'JPEG')
    print(f"Converted PDF to image: {image_filename}")
else:
    print("No PDF link found.")
    exit()

# === STEP 5: Email the image ===
msg = EmailMessage()
msg['Subject'] = "Here’s your latest file as an image"
msg['From'] = sender_email
msg['To'] = receiver_email
msg.set_content("Attached is the latest document as an image.")

with open(image_filename, 'rb') as f:
    msg.add_attachment(f.read(), maintype='image', subtype='jpeg', filename=image_filename)

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(sender_email, app_password)
    smtp.send_message(msg)

print("Email sent successfully.")

# === Optional Cleanup ===
os.remove(image_filename)
