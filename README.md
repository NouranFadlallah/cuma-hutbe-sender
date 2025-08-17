# Turkiye Friday Prayer Sermon -Cuma Hutbe- Automatic Sender

## Description

This Python script automatically:

1. Fetches the english hutbe page from the turkish government's diyanet website that updates weekly.
2. Extracts and downloads the PDF file of the **most recent posted hutbe**.
3. Converts the PDF to an **image (JPEG)**.
4. Emails the image as an attachment using your Gmail account.

---

## 🚀 Requirements

### Python Packages

Install all dependencies using:
```bash
pip install -r requirements.txt
```

### System Dependencies

🔧 On Ubuntu/Debian:
```bash
sudo apt-get install poppler-utils
```

🧰 On macOS (with Homebrew):
```bash
brew install poppler
```

🪟 On Windows:
1. Download Poppler for Windows from this repo
2. Extract it to a folder (e.g., C:\poppler)
3. Add the bin subfolder to your system PATH

### ⚙️ .env Configuration

Create a .env file in the project root with the following:

```bash
URL=https://dinhizmetleri.diyanet.gov.tr/kategoriler/yayinlarimiz/hutbeler/english-(ingilizce)
SENDER_EMAIL=your@gmail.com
RECEIVER_EMAIL=target@example.com
APP_PASSWORD=your_gmail_app_password
```

URL: The page containing the hutbes table, you can use the turkish or arabic pages just replace the url.


### 📧 Gmail App Password Setup

To use Gmail securely, you must create an App Password:

- Go to: https://myaccount.google.com/apppasswords
- Create an app password and use it in .env as APP_PASSWORD

## 🏁 Running the Script
```bash
python main.py
```