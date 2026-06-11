# 네이버 카페 새 글 → 핸드폰 알림

특정 네이버 카페의 특정 게시판에 새 글이 올라오면 **핸드폰으로 알림**을 보내줍니다.
알림 방법은 두 가지 중 선택할 수 있어요.

| 방법 | 비용 | 난이도 | 비고 |
|------|------|--------|------|
| **텔레그램** (추천) | 무료 | 쉬움 | 텔레그램 앱만 깔면 됨 |
| **문자(SMS)** | 유료(건당 과금) | 보통 | 솔라피 가입 + 발신번호 등록 필요 |

> ⚠️ 이 프로그램은 **전체공개 카페 게시판**에서 동작합니다.
> 회원만 볼 수 있는 비공개 게시판은 네이버 로그인 자동화가 따로 필요합니다.

---

## 1. 설치

```bash
pip install -r requirements.txt
cp .env.example .env   # 윈도우는: copy .env.example .env
```

## 2. 감시할 게시판 번호(clubid, menuid) 찾기

1. PC 브라우저에서 감시할 카페 게시판을 엽니다.
2. 게시판의 **글 목록**이 보이는 상태에서 주소(URL)를 봅니다.
   - 옛날 형식: `...?search.clubid=12345678&search.menuid=25...`
   - 새 형식이면 글 하나 누르고 주소의 `cafes/12345678/` 숫자가 **clubid**,
     게시판 목록에서 `menus/25` 숫자가 **menuid** 입니다.
3. 찾은 숫자를 `.env` 의 `NAVER_CLUB_ID`, `NAVER_MENU_ID` 에 넣습니다.

> 헷갈리면 게시판 URL을 저에게 보내주세요. 번호를 찾아드릴게요.

## 3. 알림 방법 설정 (`.env`)

### (A) 텔레그램 — 무료, 추천
1. 텔레그램에서 `@BotFather` 검색 → `/newbot` → 봇 이름 정하면 **토큰** 발급
2. 방금 만든 봇과 대화방을 열고 아무 메시지나 보냄
3. 브라우저에서 `https://api.telegram.org/bot<토큰>/getUpdates` 접속 → `"chat":{"id": ...}` 의 숫자가 **chat_id**
4. `.env` 에 입력:
   ```
   NOTIFY_METHOD=telegram
   TELEGRAM_BOT_TOKEN=발급받은토큰
   TELEGRAM_CHAT_ID=숫자
   ```

### (B) 문자(SMS) — 유료
1. https://solapi.com 가입 → API Key/Secret 발급
2. 발신번호(내 번호) 사전 등록
3. `.env` 에 입력:
   ```
   NOTIFY_METHOD=sms
   SOLAPI_API_KEY=...
   SOLAPI_API_SECRET=...
   SMS_FROM=01012345678   # 등록한 발신번호
   SMS_TO=01012345678     # 알림 받을 내 번호
   ```

## 4. 실행

```bash
# 동작 한 번만 테스트 (새 글 있으면 1회 알림)
python monitor.py --once

# 계속 감시 (기본 60초마다 확인)
python monitor.py
```

- **첫 실행**은 현재 글들을 "기준점"으로만 저장하고 알림은 안 보냅니다.
  그 이후 올라오는 **새 글부터** 알림이 갑니다.
- 24시간 돌리려면 PC를 켜두거나, 라즈베리파이/클라우드 서버에서
  `nohup python monitor.py &` 또는 `systemd`/`pm2` 등으로 상시 실행하세요.

## 파일 구조

| 파일 | 설명 |
|------|------|
| `monitor.py` | 메인 루프(감시 + 새 글 판별 + 알림) |
| `cafe.py` | 네이버 카페 글 목록 가져오기 |
| `notifier.py` | 텔레그램/SMS 발송 |
| `.env` | 내 설정값 (깃에 올라가지 않음) |
| `seen_articles.json` | 이미 알린 글 기록 (자동 생성) |
