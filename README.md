<div align="center">
  <img src="./modestgames_banner.png" alt="ModestGames Banner" width="100%"/>
  <br><br>
  <img src="./modestgames.png" alt="ModestGames Logo" width="100"/>
  <h1>ModestGames</h1>
  <p><strong>A sophisticated, fully autonomous free-game claiming engine for the Epic Games Store.</strong></p>

  <p>
    <img src="https://img.shields.io/github/license/w3Abhishek/ModestGames?style=flat-square&color=0078f2" alt="License">
    <img src="https://img.shields.io/github/languages/top/w3Abhishek/ModestGames?style=flat-square&color=0078f2" alt="Language">
    <img src="https://img.shields.io/github/actions/workflow/status/w3Abhishek/ModestGames/claim.yml?style=flat-square&color=0078f2" alt="Build Status">
  </p>
</div>

<br>

Welcome to **ModestGames**. Built on top of Python and Playwright, this tool completely automates the process of claiming free weekly games on the Epic Games Store. By leveraging your actual session cookies in a secure, headless Chromium environment, it bypasses complex authentication flows and interacts with the store exactly like a real human.

Set it up once, push it to GitHub Actions, and let it build your library effortlessly in the background.

## ✨ Features

- **Automated Claiming Engine**: Silently fetches, filters, and purchases 100% discounted games every week.
- **Zero-Touch Auth**: Operates exclusively on active session cookies. No usernames, no passwords, and no manual CAPTCHA solving during the automated runs.
- **Auto-Updating Secrets**: Features an elegant local extraction script that instantly connects to your active browser, grabs the session, and uses the `gh` CLI to seamlessly re-encrypt and push your cookies to GitHub Secrets.
- **Email Notifications**: Stay informed with rich notifications on successful claims, and get instant fallback alerts if your session expires or encounters a strict CAPTCHA challenge.
- **State Awareness**: Persists claim history directly to the repository to avoid redundant network requests.

---

## 🚀 Getting Started

### 1. Local Setup
Clone the repository and install the required dependencies.

```bash
git clone https://github.com/w3Abhishek/ModestGames.git
cd ModestGames
pip install -r requirements.txt
playwright install chromium
```

### 2. Connect & Extract Cookies
You'll need to extract your session cookies. We've built a frictionless script to do this by connecting directly to your active browser.

1. Launch Chrome or Edge with remote debugging enabled:
   ```bash
   "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222
   ```
2. Navigate to [store.epicgames.com](https://store.epicgames.com/) in that browser window and log in.
3. Run the extraction script:
   ```bash
   python scripts/export_cookies.py
   ```
*If you have the `gh` CLI installed, the script will automatically upload the encrypted cookies to your GitHub Secrets. Otherwise, it will output a JSON array for manual entry.*

### 3. GitHub Actions Configuration
To run this autonomously, ensure your repository has the following secrets configured (Settings > Secrets and variables > Actions):

| Secret Name | Description |
| :--- | :--- |
| `EPIC_COOKIES` | Your session cookies *(auto-configured by the script if `gh` CLI is present)* |
| `EMAIL_USER` | Sender email address (e.g. your 163 mailbox) |
| `EMAIL_PASSWORD` | SMTP authorization code (163 授权码, **not** your login password) |
| `EMAIL_TO` | Recipient email address for notifications |
| `GH_PAT` | A Personal Access Token (PAT) with `repo` scope (or fine-grained "Actions" read-write) to allow the bot to self-update the `EPIC_COOKIES` secret |

### 4. Autonomous Execution
Once your secrets are set, the workflow will automatically execute:
- **Thursdays at 9:00 AM UTC** (Just before the Epic Games rotation)
- **Thursdays at 5:00 PM UTC** (Safety net post-rotation)
- **Mondays at 9:00 AM UTC** (Weekly fallback check)

---

## 🛠️ Local Testing

If you want to run the engine manually on your local machine, simply copy `config.example.env` to `.env`, populate your variables (pasting your JSON array into `EPIC_COOKIES`), and run:

```bash
python -m claimer
```

---

<div align="center">
  <i>Built with elegance and precision.</i>
</div>
