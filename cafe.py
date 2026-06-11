"""네이버 카페 게시판 글 목록을 가져옵니다.

전체공개 카페 게시판은 로그인 없이 아래 공개 JSON 엔드포인트로 조회됩니다.
회원 전용(비공개) 게시판은 별도 로그인/쿠키가 필요하므로 이 방식으로는 동작하지 않습니다.
"""
import requests

API_URL = "https://apis.naver.com/cafe-web/cafe2/ArticleListV2dot1.json"


def fetch_articles(club_id: str, menu_id: str, per_page: int = 20):
    """최신 글 목록을 [{id, title, writer, url}] 형태로 반환합니다."""
    params = {
        "search.clubid": club_id,
        "search.menuid": menu_id,
        "search.queryType": "lastArticle",
        "search.page": 1,
        "search.perPage": per_page,
    }
    headers = {
        # 모바일 카페로 위장해야 공개 데이터가 잘 내려옵니다.
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) "
        "AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148",
        "Referer": f"https://m.cafe.naver.com/ca-fe/web/cafes/{club_id}/menus/{menu_id}",
    }
    resp = requests.get(API_URL, params=params, headers=headers, timeout=15)
    resp.raise_for_status()
    data = resp.json()

    refer = data.get("message", {}).get("result", {}).get("articleList", [])
    articles = []
    for item in refer:
        # 공지글은 건너뜁니다.
        if item.get("type") == "NOTICE" or item.get("noticeType"):
            continue
        article_id = item.get("articleId")
        if article_id is None:
            continue
        articles.append(
            {
                "id": int(article_id),
                "title": item.get("subject", "(제목 없음)").strip(),
                "writer": item.get("writerNickname", item.get("writerId", "")),
                "url": f"https://cafe.naver.com/ca-fe/cafes/{club_id}/articles/{article_id}",
            }
        )
    return articles
