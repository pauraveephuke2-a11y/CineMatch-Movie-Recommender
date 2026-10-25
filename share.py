"""
share.py — Launches CineMatch + creates a public shareable link via ngrok
Run:  python share.py
"""
import subprocess, sys, time, webbrowser

print("=" * 55)
print("  CineMatch — Starting server + public tunnel")
print("=" * 55)

# Start Streamlit in background
proc = subprocess.Popen(
    [sys.executable, "-m", "streamlit", "run", "app.py",
     "--server.port", "8501",
     "--server.headless", "true",
     "--browser.gatherUsageStats", "false"],
    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
)
print("\n[1/3] Streamlit server starting on port 8501...")
time.sleep(4)

# Start ngrok tunnel
try:
    from pyngrok import ngrok, conf
    conf.get_default().monitor_thread = False

    tunnel = ngrok.connect(8501, "http")
    public_url = tunnel.public_url

    print(f"[2/3] ngrok tunnel created!")
    print(f"\n{'='*55}")
    print(f"  LOCAL  : http://localhost:8501")
    print(f"  PUBLIC : {public_url}")
    print(f"{'='*55}")
    print(f"\n  Share this link with your friends:")
    print(f"  --> {public_url} <--")
    print(f"\n  Press Ctrl+C to stop the server")
    print(f"{'='*55}\n")

    webbrowser.open("http://localhost:8501")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down...")
        ngrok.kill()
        proc.terminate()

except Exception as e:
    print(f"[!] Could not create public tunnel: {e}")
    print(f"\n  App is running at: http://localhost:8501")
    webbrowser.open("http://localhost:8501")
    try:
        proc.wait()
    except KeyboardInterrupt:
        proc.terminate()
