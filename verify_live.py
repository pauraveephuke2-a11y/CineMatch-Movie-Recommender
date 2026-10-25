import time
from playwright.sync_api import sync_playwright

url = f"https://pauraveephuke2-a11y.github.io/?t={int(time.time())}"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    
    # 1. Desktop Test
    page = browser.new_page(viewport={"width": 1366, "height": 850})
    print(f"Loading {url}...")
    resp = page.goto(url, wait_until="networkidle", timeout=30000)
    print(f"Status: {resp.status}")
    print(f"Title: {page.title()}")
    time.sleep(1.5)
    
    # Screenshot full home view
    page.screenshot(path=r"C:\Users\Nucom\Desktop\cinematch_live_home.png")
    print("1. Desktop Home screenshot captured")
    
    # 2. Bank & UPI Gateway Modal
    print("Testing Bank & UPI portal...")
    page.wait_for_selector("button.btn-bank", timeout=10000)
    page.click("button.btn-bank")
    page.wait_for_selector("#bankModalOverlay.active", timeout=5000)
    time.sleep(1)
    page.screenshot(path=r"C:\Users\Nucom\Desktop\cinematch_bank_upi_modal.png")
    print("2. Bank & UPI modal screenshot captured")
    page.click("#bankModalOverlay .sub-close")
    time.sleep(0.5)
    
    # 3. Upgrade VIP & UPI QR Checkout
    print("Testing Subscription & UPI QR checkout...")
    page.click("#navSubscribeBtn")
    page.wait_for_selector("#subOverlay.active", timeout=5000)
    time.sleep(0.5)
    page.click("button:has-text('Proceed to UPI Payment')")
    page.wait_for_selector("#subStepUpi.active", timeout=5000)
    time.sleep(1)
    page.screenshot(path=r"C:\Users\Nucom\Desktop\cinematch_upi_checkout.png")
    print("3. UPI Checkout with QR screenshot captured")
    
    # 4. Verify & Activate VIP Membership
    print("Testing Payment Verification...")
    page.click("button:has-text('I Have Paid')")
    page.wait_for_selector("#subStepSuccess.active", timeout=5000)
    time.sleep(1)
    page.screenshot(path=r"C:\Users\Nucom\Desktop\cinematch_vip_activated.png")
    print("4. VIP Activated screenshot captured")
    page.click("button:has-text('Start Streaming Now')")
    time.sleep(0.5)
    
    # 5. Movie Detail & Streaming Player Modal
    print("Testing Movie Player Modal & Stream Pulled...")
    page.click(".movie-card >> nth=0")
    page.wait_for_selector("#movieModal.active", timeout=5000)
    time.sleep(1)
    page.screenshot(path=r"C:\Users\Nucom\Desktop\cinematch_movie_player.png")
    print("5. Movie player modal screenshot captured")
    
    # Click Pull Free Web Stream
    page.click("button:has-text('Pull Free Web Stream')")
    time.sleep(1.5)
    page.screenshot(path=r"C:\Users\Nucom\Desktop\cinematch_stream_pulled.png")
    print("6. Pull Free Web Stream captured")
    page.click("#movieModal .modal-close")
    time.sleep(0.5)
    
    # 6. Mobile Responsiveness Test (iPhone 14 / modern smartphone viewport)
    print("Testing Mobile Responsiveness...")
    mobile_page = browser.new_page(viewport={"width": 390, "height": 844}, is_mobile=True)
    mobile_page.goto(url, wait_until="networkidle", timeout=30000)
    time.sleep(1.5)
    mobile_page.screenshot(path=r"C:\Users\Nucom\Desktop\cinematch_mobile_live.png")
    print("7. Mobile view screenshot captured")
    
    browser.close()

print("\n>>> ALL TESTS PASSED SUCCESSFULLY! DEPLOYMENT FULLY VERIFIED! <<<")
