"""알림 발송 모듈: 텔레그램(무료) 또는 SMS(솔라피, 유료)."""
import hashlib
import hmac
import os
import uuid
from datetime import datetime, timezone

import requests


class TelegramNotifier:
    """텔레그램 봇으로 메시지를 보냅니다. 무료이고 설정이 가장 쉽습니다."""

    def __init__(self, token: str, chat_id: str):
        if not token or not chat_id:
            raise ValueError("TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID 를 .env 에 설정하세요.")
        self.token = token
        self.chat_id = chat_id

    def send(self, text: str) -> None:
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        resp = requests.post(
            url,
            data={"chat_id": self.chat_id, "text": text, "disable_web_page_preview": False},
            timeout=15,
        )
        resp.raise_for_status()


class SolapiNotifier:
    """솔라피(CoolSMS) 문자 발송. 실제 휴대폰 SMS/LMS 로 도착합니다. (유료)"""

    def __init__(self, api_key: str, api_secret: str, sender: str, to: str):
        if not all([api_key, api_secret, sender, to]):
            raise ValueError("SOLAPI_API_KEY/SECRET, SMS_FROM, SMS_TO 를 .env 에 설정하세요.")
        self.api_key = api_key
        self.api_secret = api_secret
        self.sender = sender.replace("-", "")
        self.to = to.replace("-", "")

    def _auth_header(self) -> str:
        date = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")
        salt = uuid.uuid4().hex
        signature = hmac.new(
            self.api_secret.encode(),
            (date + salt).encode(),
            hashlib.sha256,
        ).hexdigest()
        return (
            f"HMAC-SHA256 apiKey={self.api_key}, date={date}, "
            f"salt={salt}, signature={signature}"
        )

    def send(self, text: str) -> None:
        # 90 bytes 초과 시 자동으로 LMS 로 전송되도록 type 지정
        msg_type = "LMS" if len(text.encode("euc-kr", "ignore")) > 90 else "SMS"
        payload = {
            "message": {
                "to": self.to,
                "from": self.sender,
                "text": text,
                "type": msg_type,
            }
        }
        resp = requests.post(
            "https://api.solapi.com/messages/v4/send",
            json=payload,
            headers={
                "Authorization": self._auth_header(),
                "Content-Type": "application/json",
            },
            timeout=15,
        )
        resp.raise_for_status()


def build_notifier():
    """.env 의 NOTIFY_METHOD 에 따라 알맞은 알림 객체를 생성합니다."""
    method = os.getenv("NOTIFY_METHOD", "telegram").strip().lower()
    if method == "telegram":
        return TelegramNotifier(
            os.getenv("TELEGRAM_BOT_TOKEN", ""),
            os.getenv("TELEGRAM_CHAT_ID", ""),
        )
    if method == "sms":
        return SolapiNotifier(
            os.getenv("SOLAPI_API_KEY", ""),
            os.getenv("SOLAPI_API_SECRET", ""),
            os.getenv("SMS_FROM", ""),
            os.getenv("SMS_TO", ""),
        )
    raise ValueError(f"알 수 없는 NOTIFY_METHOD: {method!r} (telegram 또는 sms 여야 합니다)")
