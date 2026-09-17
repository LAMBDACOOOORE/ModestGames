import os
import smtplib
from email.header import Header
from email.mime.text import MIMEText


def get_config() -> dict:
    return {
        "host": os.getenv("EMAIL_HOST", "smtp.163.com"),
        "port": int(os.getenv("EMAIL_PORT", "465")),
        "user": os.getenv("EMAIL_USER", ""),
        "password": os.getenv("EMAIL_PASSWORD", ""),
        "to": os.getenv("EMAIL_TO", ""),
    }


def send_email(subject: str, body: str) -> bool:
    cfg = get_config()
    if not cfg["user"] or not cfg["password"] or not cfg["to"]:
        print("Email configuration missing. Skipping message:\n", body)
        return False

    msg = MIMEText(body, "html", "utf-8")
    msg["From"] = cfg["user"]
    msg["To"] = cfg["to"]
    msg["Subject"] = Header(subject, "utf-8")

    try:
        server = smtplib.SMTP_SSL(cfg["host"], cfg["port"], timeout=20)
        server.login(cfg["user"], cfg["password"])
        server.sendmail(cfg["user"], [cfg["to"]], msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False


def send_message(text: str):
    body = text.replace("\n", "<br>")
    send_email("Epic Games 免费游戏领取通知", body)


def send_login_prompt(games: list[str]):
    games_text = ", ".join(games) if games else "None"
    text = (
        "🎮 <b>Epic Free Games — Login Required</b><br><br>"
        f"Games to claim: <i>{games_text}</i><br><br>"
        "Cookies expired or captcha needed. Log in to Epic, complete any captcha, "
        "then extract the cookies.<br><br>"
        '👉 <a href="https://store.epicgames.com/free-games">store.epicgames.com/free-games</a><br><br>'
        "After logging in, run locally:<br>"
        "<code>python scripts/export_cookies.py</code><br>"
        "Then update the EPIC_COOKIES secret with the output."
    )
    send_email("Epic Games 免费游戏 — 需要重新登录", text)
