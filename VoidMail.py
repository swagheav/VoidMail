# VOID//MAIL - Multi-Provider Temp Mail Console (1secmail / Mail.tm Fallback)
# Styled after VOID//POST
#
# Run:
#     pip install flask requests
#     python VoidMail.py
#
# Then open http://127.0.0.1:5000 in your browser.
#
# Made by heavén swag · DM → https://t.me/he6ca

import random
import string
from flask import Flask, Response, jsonify, request
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)

API_1SEC = "https://www.1secmail.com/api/v1/"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,"
        " like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
}


# ---------------------------------------------------------------------------
# Front-end (HTML / CSS / JS) - matches README screenshots
# ---------------------------------------------------------------------------
PAGE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>VOID//MAIL</title>
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Barlow+Condensed:wght@400;600;700;900&family=Share+Tech+Mono&display=swap" rel="stylesheet">
<style>
:root{
  --bg:#000; --panel:#0a0a0a; --card:#111; --field:#0d0d0d;
  --border:#1f1f1f; --border2:#2a2a2a;
  --red:#b91c1c; --red2:#ef4444; --red3:#fca5a5;
  --dim:#666; --muted:#333; --text:#888; --bright:#ccc; --white:#eee;
  --ok:#22c55e; --warn:#f59e0b;
  --fh:'Bebas Neue',sans-serif;
  --fb:'Barlow Condensed',sans-serif;
  --fm:'Share Tech Mono',monospace;
}
*{margin:0;padding:0;box-sizing:border-box;}
[hidden]{display:none !important;}
html{scroll-behavior:smooth;}
body{background:var(--bg);color:var(--text);font-family:var(--fb);min-height:100vh;overflow-x:hidden;}

body::before{
  content:'';position:fixed;inset:0;pointer-events:none;z-index:999;
  background:repeating-linear-gradient(0deg,transparent,transparent 2px,rgba(0,0,0,.15) 2px,rgba(0,0,0,.15) 4px);
}
body::after{
  content:'';position:fixed;inset:0;pointer-events:none;z-index:998;opacity:.6;
  background-image:url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='0.04'/%3E%3C/svg%3E");
}

.wrap{max-width:900px;margin:0 auto;padding:0 18px 80px;position:relative;z-index:2;}

.topbar{display:flex;justify-content:space-between;align-items:center;padding:14px 0;border-bottom:1px solid var(--border);}
.tbl{font-family:var(--fm);font-size:10px;letter-spacing:4px;color:var(--muted);text-transform:uppercase;}
.tbl span{color:var(--red2);}
.status{display:flex;align-items:center;gap:8px;font-family:var(--fm);font-size:10px;letter-spacing:2px;color:var(--text);}
.dot{width:8px;height:8px;border-radius:50%;background:var(--muted);}
.dot.ok{background:var(--ok);box-shadow:0 0 8px var(--ok);}
.dot.err{background:var(--red2);box-shadow:0 0 8px var(--red2);}
.dot.busy{background:var(--warn);box-shadow:0 0 8px var(--warn);animation:blink 1s steps(2) infinite;}
@keyframes blink{50%{opacity:.25;}}

.masthead{position:relative;overflow:hidden;padding:26px 0 18px;border-bottom:3px solid var(--red);}
.masthead::before{
  content:'VOID//MAIL';position:absolute;font-family:var(--fh);
  font-size:clamp(7rem,16vw,14rem);color:rgba(185,28,28,.05);
  top:50%;left:-8px;transform:translateY(-50%);letter-spacing:-6px;white-space:nowrap;pointer-events:none;
}
.logo{position:relative;font-family:var(--fh);font-size:clamp(3.4rem,11vw,7.5rem);line-height:.9;letter-spacing:4px;color:var(--white);}
.logo .slash{color:var(--red);}
.logo .ver{font-family:var(--fm);font-size:clamp(.8rem,2vw,1.2rem);color:var(--red2);vertical-align:super;letter-spacing:3px;margin-left:8px;}
.sub{position:relative;font-family:var(--fm);font-size:10px;letter-spacing:5px;color:var(--dim);text-transform:uppercase;margin-top:10px;}

.tabs{display:flex;border-bottom:1px solid var(--border);margin-top:18px;}
.tab{
  flex:1;background:transparent;border:none;border-bottom:2px solid transparent;
  padding:12px 6px;font-family:var(--fm);font-size:11px;letter-spacing:3px;
  color:#666;text-transform:uppercase;cursor:pointer;transition:color .2s,border-color .2s,background .2s;
}
.tab:hover{color:#ddd;background:rgba(185,28,28,.05);}
.tab.on{color:var(--red2);border-bottom-color:var(--red);background:rgba(139,0,0,.08);}
.tab .n{color:var(--muted);margin-right:6px;}
.tab.on .n{color:var(--red);}

.panel{background:var(--panel);border:1px solid var(--border);border-top:none;padding:22px 20px;}
.panel-head{display:flex;justify-content:space-between;align-items:flex-end;margin-bottom:18px;gap:12px;flex-wrap:wrap;}
.sec-num{font-family:var(--fm);font-size:10px;color:var(--red2);letter-spacing:2px;}
.sec-title{font-family:var(--fh);font-size:26px;letter-spacing:2px;color:var(--bright);line-height:1;}

label.lbl{display:block;font-family:var(--fm);font-size:10px;letter-spacing:2px;color:var(--text);text-transform:uppercase;margin-bottom:6px;}
input[type=text]{
  width:100%;background:var(--field);border:1px solid var(--border2);border-radius:0;
  color:var(--white);padding:10px 12px;font-family:var(--fb);font-size:16px;outline:none;
  transition:border-color .15s,box-shadow .15s;
}
input:focus{border-color:var(--red2);box-shadow:0 0 0 1px rgba(239,68,68,.25);}
.field{margin-bottom:16px;}
.row{display:grid;grid-template-columns:1fr auto;gap:16px;align-items:end;}
@media (max-width:640px){.row{grid-template-columns:1fr;}}

.btn{
  font-family:var(--fm);font-size:11px;letter-spacing:2px;text-transform:uppercase;
  padding:11px 18px;border:1px solid var(--red);background:transparent;color:var(--red2);
  cursor:pointer;transition:all .15s;display:inline-block;
}
.btn:hover:not(:disabled){background:rgba(185,28,28,.12);color:#fff;}
.btn.primary{background:var(--red);color:#fff;font-weight:700;}
.btn.primary:hover:not(:disabled){background:var(--red2);border-color:var(--red2);}
.btn.ghost{border-color:var(--border2);color:var(--text);}
.btn.ghost:hover:not(:disabled){border-color:var(--text);color:var(--bright);background:transparent;}
.btn.small{padding:7px 12px;font-size:10px;}
.btn:disabled{opacity:.35;cursor:not-allowed;}
.btn-row{display:flex;gap:10px;flex-wrap:wrap;margin-top:6px;}

.msg{font-family:var(--fm);font-size:11px;letter-spacing:.5px;margin-top:14px;min-height:16px;}
.msg.ok{color:var(--ok);} .msg.err{color:var(--red2);}

.inbox-list{list-style:none;margin-top:10px;}
.inbox-item{
  background:var(--card);border:1px solid var(--border2);border-left:3px solid var(--red);
  padding:14px;margin-bottom:10px;cursor:pointer;transition:border-color .15s,background .15s;
  display:flex;justify-content:space-between;align-items:center;gap:12px;
}
.inbox-item:hover{border-color:var(--red2);background:#141414;}
.inbox-info{flex:1;overflow:hidden;}
.inbox-from{font-family:var(--fm);font-size:11px;color:var(--red2);letter-spacing:1px;margin-bottom:4px;}
.inbox-subj{font-size:18px;color:var(--bright);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.inbox-date{font-family:var(--fm);font-size:10px;color:var(--dim);text-align:right;}

.empty-state{text-align:center;padding:40px 20px;font-family:var(--fm);font-size:11px;letter-spacing:2px;color:var(--dim);}

.message-card{background:var(--card);border:1px solid var(--border2);border-top:3px solid var(--red);padding:20px;margin-top:10px;}
.msg-header{border-bottom:1px solid var(--border);padding-bottom:14px;margin-bottom:16px;}
.msg-title{font-family:var(--fh);font-size:24px;color:var(--white);letter-spacing:1px;margin-bottom:8px;}
.msg-meta{font-family:var(--fm);font-size:11px;color:var(--text);line-height:1.6;}
.msg-meta b{color:var(--bright);font-weight:normal;}
.msg-body{font-family:var(--fb);font-size:16px;color:var(--white);line-height:1.5;white-space:pre-wrap;word-break:break-word;background:var(--field);border:1px solid var(--border);padding:16px;margin-top:14px;max-height:400px;overflow-y:auto;}

.log-box{background:#050505;border:1px solid var(--border);height:360px;overflow-y:auto;padding:14px;font-family:var(--fm);font-size:11px;line-height:1.7;}
.log-line{white-space:pre-wrap;word-break:break-word;color:#aaa;}
.log-line.ok{color:var(--ok);}
.log-line.err{color:var(--red2);}
.log-line.warn{color:var(--warn);}
.log-line.dim{color:#555;}

.toast{position:fixed;bottom:24px;left:50%;transform:translate(-50%,20px);opacity:0;pointer-events:none;
  background:#000;border:1px solid var(--red);border-left:3px solid var(--red2);color:var(--bright);
  font-family:var(--fm);font-size:11px;letter-spacing:1.5px;padding:12px 18px;z-index:1001;transition:all .25s;max-width:90vw;}
.toast.show{opacity:1;transform:translate(-50%,0);}

.footer{margin-top:36px;padding-top:18px;border-top:1px solid var(--border);text-align:center;font-family:var(--fm);font-size:10px;letter-spacing:4px;color:var(--muted);}
.footer b{color:var(--red2);font-weight:normal;}
.footer a{color:var(--red2);text-decoration:none;}
.footer a:hover{text-decoration:underline;}
</style>
</head>
<body>
<div class="wrap">

  <div class="topbar">
    <div class="tbl">MULTI-ENGINE<span>::</span>API &nbsp;/&nbsp; TEMP MAIL CONSOLE</div>
    <div class="status"><span id="dot" class="dot"></span><span id="statusText">STANDBY</span></div>
  </div>

  <div class="masthead">
    <div class="logo">VOID<span class="slash">//</span>MAIL<span class="ver">v4.0</span></div>
    <div class="sub">Multi-domain fallback temporary client</div>
  </div>

  <div class="tabs">
    <button class="tab on" data-tab="mailbox"><span class="n">01</span>Mailbox</button>
    <button class="tab" data-tab="inbox"><span class="n">02</span>Inbox <span id="badge" style="color:var(--red2)"></span></button>
    <button class="tab" data-tab="log"><span class="n">03</span>Log</button>
  </div>

  <!-- MAILBOX -->
  <section class="panel" id="pane-mailbox">
    <div class="panel-head">
      <div><div class="sec-num">01 / IDENTITY</div><div class="sec-title">Temporary email address</div></div>
    </div>
    <div class="row">
      <div class="field" style="margin-bottom:0;">
        <label class="lbl" for="emailInput">Active Address</label>
        <input type="text" id="emailInput" readonly placeholder="Generating...">
      </div>
      <div class="btn-row" style="margin-top:0;">
        <button class="btn primary" id="copyBtn">Copy</button>
        <button class="btn ghost" id="genBtn">Generate New</button>
      </div>
    </div>
    <div id="mailMsg" class="msg"></div>
  </section>

  <!-- INBOX -->
  <section class="panel" id="pane-inbox" hidden>
    <div class="panel-head">
      <div><div class="sec-num">02 / MESSAGES</div><div class="sec-title">Incoming inbox</div></div>
      <div class="btn-row" style="margin-top:0;">
        <button class="btn ghost small" id="refreshBtn">Refresh now</button>
      </div>
    </div>

    <div id="inboxContainer">
      <div class="empty-state">No messages received yet. Polling active every 5 seconds...</div>
    </div>

    <div id="messageView" hidden>
      <div class="message-card">
        <div class="msg-header">
          <div class="msg-title" id="msgSubject"></div>
          <div class="msg-meta">
            <div><b>From:</b> <span id="msgFrom"></span></div>
            <div><b>Date:</b> <span id="msgDate"></span></div>
          </div>
        </div>
        <div class="msg-body" id="msgBody"></div>
        <div class="btn-row" style="margin-top:16px;">
          <button class="btn ghost small" id="backBtn">← Back to Inbox</button>
        </div>
      </div>
    </div>
  </section>

  <!-- LOG -->
  <section class="panel" id="pane-log" hidden>
    <div class="panel-head">
      <div><div class="sec-num">03 / OUTPUT</div><div class="sec-title">Activity log</div></div>
      <button class="btn ghost small" id="clearBtn">Clear</button>
    </div>
    <div class="log-box" id="log"></div>
  </section>

  <div class="footer">
    VOID<b>//</b>MAIL &nbsp;·&nbsp; MULTI-ENGINE BACKEND &nbsp;·&nbsp;
    <a href="https://t.me/he6ca" target="_blank" rel="noopener">DM → t.me/he6ca</a>
  </div>
</div>

<div class="toast" id="toast"></div>

<script>
const $ = id => document.getElementById(id);
let currentLogin = '';
let currentDomain = '';
let pollInterval = null;
let seenIds = new Set();

function showTab(name){
  document.querySelectorAll('.tab').forEach(b => b.classList.toggle('on', b.dataset.tab === name));
  ['mailbox','inbox','log'].forEach(n => $('pane-' + n).hidden = (n !== name));
}
document.querySelectorAll('.tab').forEach(b => b.onclick = () => showTab(b.dataset.tab));

function setStatus(kind, text){
  $('dot').className = 'dot ' + kind;
  $('statusText').textContent = text.toUpperCase();
}
function logLine(msg, kind){
  const box = $('log');
  const d = document.createElement('div');
  d.className = 'log-line ' + (kind || '');
  d.textContent = '[' + new Date().toLocaleTimeString() + '] ' + msg;
  box.appendChild(d);
  box.scrollTop = box.scrollHeight;
}
$('clearBtn').onclick = () => {$('log').innerHTML = ''; logLine('Log cleared.', 'dim'); };

function toast(msg){
  const t = $('toast');
  t.textContent = msg;
  t.classList.add('show');
  clearTimeout(toast._t);
  toast._t = setTimeout(() => t.classList.remove('show'), 3200);
}

async function fetchJSON(url){
  const r = await fetch(url);
  return r.json();
}

async function generateEmail(){
  setStatus('busy', 'Generating');
  logLine('Requesting fresh fallback temporary address...', 'dim');
  try{
    const d = await fetchJSON('/api/generate');
    if (d.email){
      currentLogin = d.login;
      currentDomain = d.domain;
      $('emailInput').value = d.email;
      seenIds.clear();
      setStatus('ok', 'Active');
      logLine('Generated email: ' + d.email, 'ok');
      $('mailMsg').className = 'msg ok';$('mailMsg').textContent = 'Ready to receive messages.';
      checkInbox(true);
      startPolling();
    } else {
      throw new Error(d.error || 'Failed to generate mailbox.');
    }
  } catch(e){
    setStatus('err', 'Error');
    logLine('Error generating email: ' + e.message, 'err');
    $('mailMsg').className = 'msg err';$('mailMsg').textContent = 'Error: ' + e.message;
  }
}

$('genBtn').onclick = () => generateEmail();
$('copyBtn').onclick = () => {
  const val = $('emailInput').value;
  if (!val) return;
  navigator.clipboard.writeText(val).then(() => {
    toast('Email copied to clipboard.');
    logLine('Copied email to clipboard.', 'ok');
  }).catch(() => {
    toast('Copy failed.');
    logLine('Copy failed (clipboard permission).', 'err');
  });
};

function startPolling(){
  if (pollInterval) clearInterval(pollInterval);
  pollInterval = setInterval(() => checkInbox(false), 5000);
}

async function checkInbox(manual){
  if (!currentLogin || !currentDomain) return;
  if (manual) logLine('Checking inbox...', 'dim');
  try{
    const messages = await fetchJSON(`/api/messages?login=${encodeURIComponent(currentLogin)}&domain=${encodeURIComponent(currentDomain)}`);
    if (!Array.isArray(messages)) return;

    const container = $('inboxContainer');
    if (messages.length === 0){
      if (manual) container.innerHTML = '<div class="empty-state">Inbox is currently empty.</div>';
      $('badge').textContent = '';
      return;
    }

    messages.forEach(m => {
      if (!seenIds.has(m.id)){
        seenIds.add(m.id);
        logLine('New message received from ' + m.from + ' | Subject: ' + (m.subject || '(no subject)'), 'ok');
      }
    });

    $('badge').textContent = '(' + messages.length + ')';
    container.innerHTML = '';
    messages.forEach(m => {
      const item = document.createElement('div');
      item.className = 'inbox-item';
      item.innerHTML = `
        <div class="inbox-info">
          <div class="inbox-from">${escapeHtml(m.from)}</div>
          <div class="inbox-subj">${escapeHtml(m.subject || '(No Subject)')}</div>
        </div>
        <div class="inbox-date">${escapeHtml(m.date)}</div>
      `;
      item.onclick = () => readMessage(m.id, m.subject, m.from, m.date);
      container.appendChild(item);
    });
  } catch(e){
    if (manual) logLine('Failed to fetch inbox: ' + e.message, 'err');
  }
}

async function readMessage(id, subject, from, date){
  logLine('Fetching message content (ID: ' + id + ')...', 'dim');
  $('msgSubject').textContent = subject || '(No Subject)';
  $('msgFrom').textContent = from;
  $('msgDate').textContent = date;
  $('msgBody').textContent = 'Loading message content...';
  $('inboxContainer').hidden = true;
  $('messageView').hidden = false;

  try{
    const data = await fetchJSON(`/api/read?login=${encodeURIComponent(currentLogin)}&domain=${encodeURIComponent(currentDomain)}&id=${encodeURIComponent(id)}`);
    $('msgBody').textContent = data.textBody || data.htmlBody || 'No text content available.';
    logLine('Loaded message content successfully.', 'ok');
  } catch(e){
    $('msgBody').textContent = 'Failed to load message content.';
    logLine('Failed to load message content: ' + e.message, 'err');
  }
}

$('backBtn').onclick = () => {
  $('messageView').hidden = true;
  $('inboxContainer').hidden = false;
};

$('refreshBtn').onclick = () => checkInbox(true);

function escapeHtml(str){
  return (str || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

generateEmail();
logLine('System ready. Multi-engine temp mail initialized.', 'dim');
</script>
</body>
</html>
"""


# ---------------------------------------------------------------------------
# Backend helpers
# ---------------------------------------------------------------------------
def api_request(action, params=""):
    """Hit the 1secmail API. Returns parsed JSON or None on failure."""
    try:
        url = f"{API_1SEC}?action={action}{params}"
        response = requests.get(url, headers=HEADERS, timeout=10, verify=False)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        print(f"[!] 1secmail API error: {e}")
    return None


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@app.route("/")
def index():
    return Response(PAGE, mimetype="text/html")


@app.route("/api/generate")
def api_generate():
    fallback_domains = [
        "1secmail.com",
        "1secmail.org",
        "1secmail.net",
        "esixt.org",
        "vjuum.com",
        "laafd.com",
    ]

    # Try the live domain list first
    domains_data = api_request("getDomainList")
    if domains_data and isinstance(domains_data, list) and len(domains_data) > 0:
        fallback_domains = domains_data

    domain = random.choice(fallback_domains)
    login = "".join(random.choices(string.ascii_lowercase + string.digits, k=12))
    email = f"{login}@{domain}"
    return jsonify({"email": email, "login": login, "domain": domain})


@app.route("/api/messages")
def api_messages():
    login = request.args.get("login")
    domain = request.args.get("domain")
    if not login or not domain:
        return jsonify([])

    data = api_request("getMessages", f"&login={login}&domain={domain}")
    return jsonify(data if isinstance(data, list) else [])


@app.route("/api/read")
def api_read():
    login = request.args.get("login")
    domain = request.args.get("domain")
    msg_id = request.args.get("id")
    if not login or not domain or not msg_id:
        return jsonify({}), 400

    data = api_request(
        "readMessage", f"&login={login}&domain={domain}&id={msg_id}"
    )
    return jsonify(data if data else {})


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("┌────────────────────────────────────────────┐")
    print("│  VOID//MAIL v4.0                           │")
    print("│  http://127.0.0.1:5000                     │")
    print("│  DM → https://t.me/he6ca                   │")
    print("└────────────────────────────────────────────┘")
    app.run(host="127.0.0.1", port=5000, debug=False)