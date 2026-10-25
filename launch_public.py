import subprocess
import time
import re
import sys
import os
import urllib.parse

# Set UTF-8 encoding for standard output if supported
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

print("=" * 60)
print("[*] CineMatch - Launching Streamlit & Cloudflare Public Tunnel")
print("=" * 60)

# 1. Kill any existing streamlit or cloudflared instances to ensure clean start
subprocess.run(["powershell", "-Command", "Stop-Process -Name streamlit,cloudflared -ErrorAction SilentlyContinue"], capture_output=True)

# 2. Start Streamlit
streamlit_cmd = [
    sys.executable, "-m", "streamlit", "run", "app.py",
    "--server.port", "8501",
    "--server.headless", "true"
]
print("[1/3] Starting Streamlit server on http://localhost:8501...")
st_proc = subprocess.Popen(streamlit_cmd, cwd=os.getcwd(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(3)

# 3. Start Cloudflare Tunnel
cloudflared_path = r"C:\Program Files (x86)\cloudflared\cloudflared.exe"
print("[2/3] Starting Cloudflare Quick Tunnel (Zero-password, works on iPhone & Android)...")
cf_proc = subprocess.Popen(
    [cloudflared_path, "tunnel", "--url", "http://localhost:8501"],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    bufsize=1,
    encoding="utf-8",
    errors="replace"
)

public_url = None
start_time = time.time()
while time.time() - start_time < 35:
    line = cf_proc.stdout.readline()
    if not line:
        continue
    match = re.search(r"https://[a-zA-Z0-9-]+\.trycloudflare\.com", line)
    if match:
        public_url = match.group(0)
        break

if public_url:
    print(f"\n[3/3] SUCCESS! CineMatch is LIVE worldwide!")
    print("=" * 60)
    print(f"Local Browser:  http://localhost:8501")
    print(f"Public Web Link: {public_url}")
    print("=" * 60)
    
    wa_msg = f"Hey! Check out CineMatch - an awesome movie recommendation app:\n\n{public_url}\n\nFind your next favorite film in seconds!"
    encoded = urllib.parse.quote(wa_msg)
    wa_url = f"https://wa.me/?text={encoded}"
    print(f"\nWhatsApp Direct Link:\n{wa_url}\n")
    
    with open("active_url.txt", "w", encoding="utf-8") as f:
        f.write(public_url)

    # Update app.py SHARE_URL so in-app WhatsApp buttons use the live tunnel
    try:
        with open("app.py", "r", encoding="utf-8") as f:
            content = f.read()
        content = re.sub(r'SHARE_URL = ".*?"', f'SHARE_URL = "{public_url}"', content)
        with open("app.py", "w", encoding="utf-8") as f:
            f.write(content)
    except Exception as e:
        pass

    try:
        while True:
            time.sleep(2)
    except KeyboardInterrupt:
        cf_proc.terminate()
        st_proc.terminate()
else:
    print("\n[!] Could not capture public Cloudflare URL.")
