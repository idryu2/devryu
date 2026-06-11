"""네이버 카페 새 글 감시 → 핸드폰 알림(텔레그램/SMS).

실행:
  python monitor.py            # 계속 감시
  python monitor.py --once     # 한 번만 확인
  python monitor.py --test     # 알림(텔레그램/SMS) 연결 테스트 메시지 1건 발송
  python monitor.py --dump     # 지금 받아지는 글 목록을 화면에 출력(진단용)
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


def match_keywords(title: str, keywords: list) -> bool:
    """키워드가 없으면 모든 글 통과. 있으면 제목에 하나라도 포함되면 통과."""
    if not keywords:
        return True
    low = title.lower()
    return any(k.lower() in low for k in keywords)


def check_once(club_id, menu_id, keywords, cookie, notifier, seen) -> set:
    articles = cafe.fetch_articles(club_id, menu_id, cookie=cookie)
    # 키워드(제목)에 맞는 글만 대상으로 삼습니다.
    articles = [a for a in articles if match_keywords(a["title"], keywords)]

    # 최초 실행(기록 없음)이면 현재 글들을 '읽음' 처리만 하고 알림은 보내지 않음
    first_run = len(seen) == 0
    new_ids = [a for a in articles if a["id"] not in seen]

    if first_run:
        for a in articles:
            seen.add(a["id"])
        save_seen(seen)
        print(f"[초기화] 조건에 맞는 기존 글 {len(articles)}개를 기준점으로 저장했습니다. 이후 새 글만 알립니다.")
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
    menu_id = os.getenv("NAVER_MENU_ID", "0").strip() or "0"
    cookie = os.getenv("NAVER_COOKIE", "").strip()
    keywords = [k.strip() for k in os.getenv("NAVER_KEYWORD", "").split(",") if k.strip()]
    interval = int(os.getenv("POLL_INTERVAL", "60"))

    if not club_id:
        sys.exit("NAVER_CLUB_ID 를 .env 에 설정하세요. (README.md 참고)")

    # 진단용: 지금 받아지는 글 목록을 그대로 출력
    if "--dump" in sys.argv:
        items = cafe.fetch_articles(club_id, menu_id, cookie=cookie)
        print(f"받아온 글 {len(items)}개 (키워드 필터 적용 전):")
        for a in items:
            hit = "✅" if match_keywords(a["title"], keywords) else "  "
            print(f"  {hit} [{a['id']}] {a['title']} - {a['writer']}")
        return

    notifier = build_notifier()

    # 알림 연결만 테스트
    if "--test" in sys.argv:
        notifier.send("✅ 알림 연결 테스트 성공! 이제 새 글이 올라오면 여기로 알림이 옵니다.")
        print("테스트 메시지를 발송했습니다. 핸드폰을 확인하세요.")
        return

    seen = load_seen()
    once = "--once" in sys.argv

    kw = ", ".join(keywords) if keywords else "(전체)"
    print(f"카페 감시 시작 (club={club_id}, menu={menu_id}, 키워드={kw}, 주기={interval}s)")
    while True:
        try:
            seen = check_once(club_id, menu_id, keywords, cookie, notifier, seen)
        except Exception as e:  # noqa: BLE001
            print(f"[오류] 글 목록 확인 실패: {e}", file=sys.stderr)
        if once:
            break
        time.sleep(interval)


if __name__ == "__main__":
    main()
