# Facebook Profile Scraper

Async Facebook profile scraper built with **Playwright**, **playwright-stealth** and **BeautifulSoup**.  
The script loads public Facebook profiles, extracts visible information, and generates a clean **HTML report** with profile details and images.

> Facebook heavily restricts automated access. This project uses browser automation and heuristic parsing and may break if Facebook changes its frontend.

---

## ✨ Features

- Async scraping with Playwright
- Stealth mode to reduce bot detection
- Automatic scrolling for dynamic content
- Profile name detection
- Profile picture extraction
- Bio / description extraction (when available)
- Followers / likes / friends heuristic detection
- Clean HTML report generation
- Multiple profiles in a single run

---

## 📸 

<p align="center">
  <img src="example/result_01.png" width="45%">
</p>
---

## ⚙️ Installation

### 1. Clone the repository

```
git clone https://github.com/stoicismo/fb_scrap.git
cd fb_scrap
```

### 2. Install dependencies

```
pip install -r requirements.txt
```

### 3. Install Playwright browsers

```
playwright install
```

---

## 🚀 Usage

Run the scraper:

```
python scraperfb.py
```

You will be prompted to enter Facebook usernames (without `@`).

- Press **Enter** on empty input to finish
- The HTML report will be saved as **get_scraped.html**

---

## 📝 Output

The script generates a standalone HTML file containing:

- Profile name
- Username
- Profile picture
- Bio / description (if found)
- Likes / followers (heuristic)
- Friends count (heuristic)
- Direct link to the profile

The file can be opened locally in any browser.

---

## ⚠️ Disclaimer

This project is intended **for educational and research purposes only**.

- The author is **not responsible** for any misuse
- You are responsible for complying with **Facebook Terms of Service** and local laws
- Do **not** scrape private profiles or protected content

Use responsibly.

---

## 🧠 Notes

- Facebook frequently changes its DOM, scraping logic may break
- The script relies on heuristic parsing and best-effort extraction
- The script uses **headless Chromium** by default

---

## 📜 License

MIT License
