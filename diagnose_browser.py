"""
diagnose_browser.py
Tests the live GitHub Pages website in real headless Chromium via Playwright.
"""
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    url = "https://pauraveephuke2-a11y.github.io/"
    print(f"Navigating to: {url}")
    response = page.goto(url, wait_until="networkidle")

    print(f"Status Code: {response.status}")
    print(f"Page Title:  {page.title()}")
    content = page.content()
    print(f"Content Length: {len(content)}")
    if "404" in page.title() or "There's isn't a GitHub Pages site here" in content or "404" in content[:500]:
        print("[!] PAGE SHOWS 404!")
        print("First 300 chars of body:", page.inner_text("body")[:300])
    else:
        print("[SUCCESS] Page loaded successfully!")
        print("Hero Heading:", page.inner_text("h1"))

    # Also test /index.html
    url_index = "https://pauraveephuke2-a11y.github.io/index.html"
    print(f"\nNavigating to: {url_index}")
    resp2 = page.goto(url_index, wait_until="networkidle")
    print(f"Status Code: {resp2.status}")
    print(f"Page Title:  {page.title()}")

    browser.close()
