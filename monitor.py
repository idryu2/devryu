"""네이버 카페 새 글 감시 → 핸드폰 알림(텔레그램/SMS).

실행: python monitor.py
한 번만 테스트: python monitor.py --once
"""
import json
import os
import sys
import time
from pathlib import Path

from dotenv import load_dotenv

import cafe
from notifier import build_notifier

STATE_FILE = Path(__file__).parent / "seen_articles.json"
MAX_REMEMBER = 500  # 메모리/파일이 무한정 커지지 않도록 최근 N개만 기억


def load_seen() -> set:
    if STATE_FILE.exists():
        try:
            return set(json.loads(STATE_FILE.read_text()))
        except (ValueError, OSError):
            return set()
    return set()


def save_seen(seen: set) -> None:
    # 가장 큰(최신) id 위주로 최근 MAX_REMEMBER 개만 보관
    trimmed = sorted(seen, reverse=True)[:MAX_REMEMBER]
    STATE_FILE.write_text(json.dumps(trimmed))


def check_once(club_id: str, menu_id: str, notifier, seen: set) -> set:
    articles = cafe.fetch_articles(club_id, menu_id)

    # 최초 실행(기록 없음)이면 현재 글들을 '읽음' 처리만 하고 알림은 보내지 않음
    first_run = len(seen) == 0
    new_ids = [a for a in articles if a["id"] not in seen]

    if first_run:
        for a in articles:
            seen.add(a["id"])
        save_seen(seen)
        print(f"[초기화] 기존 글 {len(articles)}개를 기준점으로 저장했습니다. 이후 새 글만 알립니다.")
        return seen

    # 오래된 글이 먼저 도착하도록 id 오름차순으로 발송
    for a in sorted(new_ids, key=lambda x: x["id"]):
        text = f"📢 새 글 알림\n[{a['title']}]\n작성자: {a['writer']}\n{a['url']}"
        try:
            notifier.send(text)
            print(f"  → 알림 전송: {a['title']}")
        except Exception as e:  # noqa: BLE001
            print(f"  ! 알림 전송 실패: {e}", file=sys.stderr)
            continue  # 실패한 글은 seen 에 넣지 않아 다음 주기에 재시도
        seen.add(a["id"])

    if new_ids:
        save_seen(seen)
    return seen


def main() -> None:
    load_dotenv()
    club_id = os.getenv("NAVER_CLUB_ID", "").strip()
    menu_id = os.getenv("NAVER_MENU_ID", "").strip()
    interval = int(os.getenv("POLL_INTERVAL", "60"))

    if not club_id or not menu_id:
        sys.exit("NAVER_CLUB_ID / NAVER_MENU_ID 를 .env 에 설정하세요. (README.md 참고)")

    notifier = build_notifier()
    seen = load_seen()
    once = "--once" in sys.argv

    print(f"카페 감시 시작 (club={club_id}, menu={menu_id}, 주기={interval}s)")
    while True:
        try:
            seen = check_once(club_id, menu_id, notifier, seen)
        except Exception as e:  # noqa: BLE001
            print(f"[오류] 글 목록 확인 실패: {e}", file=sys.stderr)
        if once:
            break
        time.sleep(interval)


if __name__ == "__main__":
    main()
