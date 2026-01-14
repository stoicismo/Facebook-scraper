import asyncio
from playwright.async_api import async_playwright
from playwright_stealth import Stealth
from bs4 import BeautifulSoup
from datetime import datetime
import re

BASE_URL = "https://www.facebook.com"
ENDPOINT_PATTERN = "/{}"
OUTPUT_FILE = "get_scraped.html"

html_content = f"""
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <title>scraped by exposedid - {datetime.now().strftime('%d/%m/%Y %H:%M')}</title>
    <style>
        body {{ font-family: Arial, sans-serif; background: #f0f2f5; margin: 40px; }}
        .profile {{ background: white; border-radius: 10px; padding: 20px; margin: 30px auto; max-width: 900px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }}
        .name {{ font-size: 28px; font-weight: bold; color: #1c1e21; margin-bottom: 10px; }}
        .info {{ margin: 10px 0; }}
        .profile-pic {{ width: 150px; height: 150px; border-radius: 50%; object-fit: cover; border: 4px solid #1877f2; }}
        hr {{ margin: 20px 0; border: 0; border-top: 1px solid #ddd; }}
    </style>
</head>
<body>
    <h1>Scraped Profiles - {datetime.now().strftime('%d/%m/%Y %H:%M')}</h1>
"""

async def scrape_profile(username):
    global html_content

    async with Stealth().use_async(async_playwright()) as p:
        browser = await p.chromium.launch(headless=True)  # holy 
        page = await browser.new_page()

        url = BASE_URL + ENDPOINT_PATTERN.format(username)

        try:
            print(f"loading {url}...")
            await page.goto(url, wait_until="networkidle", timeout=90000)

            for _ in range(12):
                await page.evaluate("window.scrollBy(0, 1500)")
                await asyncio.sleep(3)

            await asyncio.sleep(10)  # js

            content = await page.content()
            soup = BeautifulSoup(content, "html.parser")

            name_tag = soup.find("h1") or soup.find("span", {"dir": "auto"})
            if name_tag:
                name = name_tag.get_text(strip=True)
                name = re.sub(r'Verified account$', '', name).strip()
            else:
                name = "Name not found"

            profile_pic_url = "https://via.placeholder.com/150?text=No+Foto"
            img_tag = soup.find("image")
            if img_tag and img_tag.get("xlink:href"):
                profile_pic_url = img_tag["xlink:href"]

            elif soup.find("img", alt=re.compile(re.escape(name), re.I)):
                img = soup.find("img", alt=re.compile(re.escape(name), re.I))
                if img.get("src"):
                    profile_pic_url = img["src"]

            else:
                for img in soup.find_all("img"):
                    src = img.get("src", "")
                    if src and ("profile" in src or "fbcdn" in src) and "width=" in str(img) or "height=" in str(img):
                        if any(size in str(img) for size in ["150", "160", "170", "180"]):
                            profile_pic_url = src
                            break

            about = "no bio found"
            for span in soup.find_all("span", {"dir": "auto"}):
                text = span.get_text(strip=True)
                if 30 < len(text) < 400:
                    if any(kw in text.lower() for kw in ["pagina ufficiale", "arma dei carabinieri", "possiamoaiutarvi", "benvenuti", "sono", "vivo a"]):
                        about = text
                        break

            likes_followers = "Non visibile"
            friends = "Non visibile"
            full_text = soup.get_text(separator=" ", strip=True).lower()

            patterns = [
                r'(\d{1,3}(?:\.\d{3})*(?:,\d+)?)\s*(followers?|following|like|likes|pp)',
                r'(\d[\d\.KMB]+)\s*(followers?|seguaci|mi piace|likes)',
            ]
            for pattern in patterns:
                match = re.search(pattern, full_text, re.IGNORECASE)
                if match:
                    likes_followers = match.group(0).strip()
                    break

            friends_match = re.search(r'(\d{1,3}(?:\.\d{3})*(?:,\d+)?)\s*amici', full_text, re.IGNORECASE)
            if friends_match:
                friends = friends_match.group(0).strip()

            html_content += f"""
            <div class="profile">
                <div style="display: flex; align-items: center; gap: 20px;">
                    <img src="{profile_pic_url}" alt="Foto profilo" class="profile-pic" onerror="this.src='https://via.placeholder.com/150?text=No+Foto'">
                    <div>
                        <div class="name">{name}</div>
                        <div class="info"><strong>Username:</strong> @{username}</div>
                    </div>
                </div>
                <hr>
                <div class="info"><strong>Bio/d:</strong><br>{about}</div>
                <div class="info"><strong>likes / Follower:</strong> {likes_followers}</div>
                <div class="info"><strong>friends:</strong> {friends}</div>
                <div class="info"><a href="{url}" target="_blank">open fb →</a></div>
            </div>
            """
            print(f"yes! {username} success")

        except Exception as e:
            error_msg = str(e)[:200]
            html_content += f"""
            <div class="profile" style="border-left: 5px solid red;">
                <strong>@{username}</strong> — Error: {error_msg}
                <br><a href="{url}" target="_blank">try manually</a>
            </div>
            """
            print(f"Error {username}: {e}")

        finally:
            await browser.close()

print("scraper by exposedid, username (no @):\n")

async def main():
    while True:
        username = input("Username: ").strip()
        if not username:
            break
        if username.startswith("@"):
            username = username[1:]
        await scrape_profile(username)

    global html_content
    html_content += "</body></html>"
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"\ncomplete, saved in: {OUTPUT_FILE}")

asyncio.run(main())
