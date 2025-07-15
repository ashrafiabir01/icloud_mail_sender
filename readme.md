Thanks! Since your script sends emails via **iCloud SMTP (`smtp.mail.me.com`)**, I’ve updated the `README.md` to reflect that clearly and tailored the wording for **iCloud Mail Sender** use.

---

### ✅ Updated `README.md` (for iCloud Mail Sender with License System)

```markdown
# 🍎 iCloud SMTP Bulk Email Sender with License System

A powerful multithreaded **bulk email sender using iCloud Mail** (`smtp.mail.me.com`).  
Includes content randomization, attachment support, and a hardware-locked license system.

## ✉️ Features

- 🔐 **License-based access** — only authorized users (UUID-based)
- 🧵 **Multithreaded** email sending
- 🗂️ Supports multiple email formats:
  - Plain Text
  - HTML Content
  - Image or PDF attachments
  - Combined HTML + Attachment
- 📄 Dynamic subject & sender name selection
- 🧠 Automatic logging and retry for failed emails
- 📑 Modular folder-based body/attachment structure

---

## 📁 Folder Structure

```

📂 Project/
├── main.py                 # Main script
├── auth.py                 # License key system (UUID-based)
├── smtp\_credentials.txt    # Your iCloud SMTP credentials (email\:password)
├── to\_emails.txt           # Target email list
├── subject.txt             # Subjects (randomly picked)
├── sendername.txt          # Friendly sender names
├── reply\_mail.txt          # Reply-to email
├── html/                   # HTML bodies
├── body/                   # Plain text bodies
├── img/                    # Images for attachment
├── pdf/                    # PDFs for attachment
├── email\_log.txt           # Successful email logs
├── failed\_smtp\_log.txt     # Bad SMTPs
├── failed\_email\_log.txt    # Failed deliveries
└── to\_emails\_failed.txt    # Failed emails (re-queued)

````

---

## ⚙️ How It Works

1. Reads iCloud SMTP credentials from `smtp_credentials.txt`
2. Picks a random subject and sender name
3. Sends customized emails using multiple content formats
4. Logs delivery status for each recipient
5. Retries failed sends at the end

---

## 🧪 Usage

1. Edit your files:
   - `smtp_credentials.txt` — Format: `icloud_email@icloud.com:app-specific-password`
   - `to_emails.txt` — Recipients list (one per line)
   - `subject.txt` — Subjects pool
   - `sendername.txt` — Random display names (for `From:`)
   - `reply_mail.txt` — Your reply-to email address
2. Place body/HTML/attachments in respective folders
3. Run:
```bash
python main.py
````

4. Choose email format (1–6)
5. Set sleep interval between batches

---

## 🔐 License Protection (UUID-based)

On first run:

* A **hardware-based UUID hash** is generated and shown
* This is **copied to clipboard**
* Admin must **add this key to the remote server** (used in `auth.py`)
* Only verified machines can send emails

> Key verification is done via:

```
https://yourhost.com/view/data/raw
```

---

## 🧾 Dependencies

Install required packages:

```bash
pip install pyperclip
```

Other requirements:

* Windows (due to `wmic`)
* Python 3.7+

---

## 📢 Disclaimer

This tool is made for **educational and authorized business use only**.
**Do not use for unsolicited spam** or you may violate iCloud’s and local regulations.

---

## 👤 Credits

Developed by: **Ashrafi Khandaker Abir**
Website: [https://devabir.com](https://devabir.com)

---

## 🔗 Connect

For license approvals or support:
📧 **[admin@devabir.com](mailto:admin@devabir.com)**

---

```

---

Would you like me to generate a sample `smtp_credentials.txt`, `subject.txt`, and `sendername.txt` to go with it?
```
