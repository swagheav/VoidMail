<h3 align="center">VOID//MAIL — Multi-Provider Temp Mail Console</h3>

<p align="center">
  Self-hosted disposable inboxes with automatic provider fallback.<br>
  Fast · Lightweight · Zero config
</p>

<p align="center">
  <img src="https://img.shields.io/badge/VOID-MAIL-red?style=for-the-badge&logo=maildotru&logoColor=white" alt="VoidMail"/>
  <img src="https://img.shields.io/badge/Python-3.x-blue?style=for-the-badge&logo=python" alt="Python"/>
  <img src="https://img.shields.io/badge/Flask-Web%20UI-green?style=for-the-badge&logo=flask" alt="Flask"/>
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" alt="License"/>
  <img src="https://img.shields.io/badge/Made%20in-2026-purple?style=for-the-badge" alt="2026"/>
</p>

<p align="center">
  <b>Developer:</b> #SWAG – Heaven Swag ·
  <a href="https://t.me/he6ca">DM</a> ·
  <a href="https://t.me/SWGHEV">Channel</a>
</p>

---

## Overview

**VOID//MAIL** is a self-hosted temporary email client built with Flask. It generates disposable inboxes, polls for incoming messages every 5 seconds, and reads them in a clean terminal-styled web UI.

It supports **two providers with automatic fallback**:
- **Mail.tm** — primary provider (full API account creation)
- **1secmail** — automatic fallback if Mail.tm is unavailable

---

## Features

- Multi-provider fallback (Mail.tm → 1secmail)
- Auto-generated disposable addresses
- Live inbox polling every 5 seconds
- Read full message bodies in-browser
- VOID//POST-inspired terminal UI (scanlines, noise, monospace)
- Copy-to-clipboard for the active address
- Activity log with timestamps
- Zero database, zero configuration

---

## Requirements

| Component | Minimum |
|-----------|---------|
| OS | Windows / Linux / macOS |
| Python | 3.7+ |
| Browser | Any modern browser |
| Internet | Required |

---

## Installation

```bash
# Clone the repository
git clone https://github.com/swagheav/VoidMail.git
cd VoidMail

# Install dependencies
pip install flask requests

# Run
python VoidMail.py
```

Then open **http://127.0.0.1:5000** in your browser.

---

## Usage

1. Launch the app — an address is generated automatically.
2. Click **Copy** to copy the address.
3. Use it wherever you need a disposable inbox.
4. Switch to the **Inbox** tab — messages appear automatically every 5 seconds.
5. Click any message to read the full body.
6. Click **Generate New** to rotate to a fresh address.

---

## Project Structure

```
VoidMail/
├── VoidMail.py        # Flask app + frontend
├── requirements.txt   # flask, requests
├── README.md
└── LICENSE
```

---

## Technical Details

| Property | Details |
|----------|---------|
| Language | Python 3.x |
| Framework | Flask |
| Providers | Mail.tm (primary), 1secmail (fallback) |
| Frontend | Single-file HTML/CSS/JS |
| Polling | 5-second interval |
| Storage | None — fully stateless |

---

## Notes

- VOID//MAIL is intended for legitimate use cases: signing up for services you don't want to share your real email with, testing email flows, and avoiding spam.
- It is not intended for bypassing platform verification, evading bans, or fraud.
- All requests go to the official Mail.tm and 1secmail APIs.

---

## Contact

| Type | Link |
|------|------|
| 📢 Channel | [t.me/SWGHEV](https://t.me/SWGHEV) |
| 💬 DM | [t.me/he6ca](https://t.me/he6ca) |
| 🐙 GitHub | [@swagheav](https://github.com/swagheav) |
| 📦 Repo | [github.com/swagheav/VoidMail](https://github.com/swagheav/VoidMail) |

---

<p align="center">© 2026 VOID//MAIL • All Rights Reserved</p>
