# 🍎 iCloud SMTP Bulk Email Sender with License System

A powerful multithreaded **bulk email sender using iCloud Mail** (`smtp.mail.me.com`).  
Includes content randomization, attachment support, and a hardware-locked license system.

## ✉️ Features

- 🔐 License-based access (hardware-locked)
- 🧵 Multithreaded email sending
- 🗂️ Supports multiple email formats:
  - Plain Text
  - HTML Body
  - Text + Image Attachment
  - Text + PDF Attachment
  - HTML + Image
  - HTML + PDF
- 📄 Dynamic subject & sender name selection
- 📥 SMTP rotation and failure logging
- 🔁 Failed emails are retried

---

## 📁 Folder Structure

```

📂 Project/
├── main.py                 # Main script
├── auth.py                 # License system (UUID-based)
├── smtp\_credentials.txt    # iCloud SMTP credentials (email\:password)
├── to\_emails.txt           # Target email list
├── subject.txt             # Subjects pool
├── sendername.txt          # Display names
├── reply\_mail.txt          # Reply-to email
├── html/                   # HTML bodies
├── body/                   # Plain text bodies
├── img/                    # Images
├── pdf/                    # PDFs
├── email\_log.txt           # Sent email logs
├── failed\_smtp\_log.txt     # Invalid SMTPs
├── failed\_email\_log.txt    # Failed deliveries
└── to\_emails\_failed.txt    # Failed emails for retry

````

---

## 🧪 How to Use

1. Edit your files:
   - `smtp_credentials.txt`: `icloud_email@icloud.com:app-password`
   - `to_emails.txt`: Recipients list
   - `subject.txt`: Multiple subjects (one per line)
   - `sendername.txt`: Friendly sender names
   - `reply_mail.txt`: Reply-to email address
2. Add your message content:
   - `body/` – plain text files
   - `html/` – HTML templates
   - `img/` – image files
   - `pdf/` – PDF files
3. Run the script:

```bash
python main.py
````

4. Choose the email format:

```
1 = Plain Text
2 = HTML Body
3 = Text + Image
4 = Text + PDF
5 = HTML + Image
6 = HTML + PDF
```

5. Set sleep interval between batches

---

## 🔐 License System

This tool uses a **hardware-bound license key system**:

- Your unique device UUID is hashed and copied to clipboard
- Admin must add your key to the remote server
- Unauthorized devices will be denied access

> License validation checks:
> `https://yourhost.com/view/data/raw`

---

## 💻 Requirements

- Python 3.7+
- Windows OS (uses `wmic`)
- Install required packages:

```bash
pip install pyperclip
```

---

## ⚠️ Disclaimer

This software is for **educational or authorized business use only**.
Do **not** use for unsolicited bulk email ("spam") as it violates both iCloud’s policy and anti-spam laws.

---

## 👤 Credits

**Developer**: Ashrafi Khandaker Abir
🌐 [https://devabir.com](https://devabir.com)

---
