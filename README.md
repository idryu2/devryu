# 네이버 카페 새 글 → 핸드폰 알림

특정 네이버 카페에 **(원하면 제목 키워드에 맞는)** 새 글이 올라오면 **핸드폰으로 알림**을 보내줍니다.
알림 방법은 두 가지 중 선택할 수 있어요.

| 방법 | 비용 | 난이도 | 비고 |
|------|------|--------|------|
| **텔레그램** (추천) | 무료 | 쉬움 | 텔레그램 앱만 깔면 됨 |
| **문자(SMS)** | 유료(건당 과금) | 보통 | 솔라피 가입 + 발신번호 등록 필요 |

> 전체공개 카페면 설정 없이 바로 동작합니다.
> 회원만 볼 수 있는 비공개 카페는 `.env` 의 `NAVER_COOKIE` 에 로그인 쿠키를 넣으면 됩니다.

이 프로젝트는 보내주신 URL
`cafe.naver.com/.../cafes/20486145/menus/0?q=카리20&ta=SUBJECT` 기준으로
**카페 20486145 의 전체글 중 제목에 `카리20` 이 들어간 새 글**을 감시하도록 미리 맞춰져 있습니다.

---

## 1. 설치

```bash
pip install -r requirements.txt
cp .env.example .env   # 윈도우는: copy .env.example .env
```

## 2. 설정 (`.env`)

`.env.example` 을 복사한 `.env` 에 이미 카페 값이 채워져 있습니다.

| 항목 | 의미 | 기본값 |
|------|------|--------|
| `NAVER_CLUB_ID` | 카페 고유 번호 | `20486145` |
| `NAVER_MENU_ID` | 게시판 번호(`0`=전체글) | `0` |
| `NAVER_KEYWORD` | 제목 키워드(쉼표로 여러 개, 비우면 모든 새 글) | `카리20` |
| `NAVER_COOKIE` | 비공개 카페일 때만 로그인 쿠키 | (비움) |
| `POLL_INTERVAL` | 확인 주기(초) | `60` |

> 다른 카페/게시판을 보고 싶으면 그 게시판 URL을 저에게 보내주세요. 번호를 찾아드릴게요.

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

## 4. 실행 / 점검

```bash
# (1) 글이 제대로 받아지는지 먼저 확인 (✅ 표시가 키워드 매칭된 글)
python monitor.py --dump

# (2) 알림(텔레그램/SMS) 연결 테스트 — 핸드폰으로 테스트 메시지 1건
python monitor.py --test

# (3) 한 번만 확인 (새 글 있으면 1회 알림)
python monitor.py --once

# (4) 계속 감시 (기본 60초마다)
python monitor.py
```

권장 순서: **`--dump` → `--test` → `--once` → 상시 실행**.
`--dump` 에 글이 안 나오면 비공개 카페일 수 있으니 `NAVER_COOKIE` 를 채워주세요.

- **첫 실행**은 현재 글들을 "기준점"으로만 저장하고 알림은 안 보냅니다.
  그 이후 올라오는 **새 글부터** 알림이 갑니다.
- 24시간 돌리려면 PC를 켜두거나, 라즈베리파이/클라우드 서버에서
  `nohup python monitor.py &` 또는 `systemd`/`pm2` 등으로 상시 실행하세요.

## 5. (선택) PC 없이 24시간 자동 운영 — GitHub Actions

PC를 안 켜놔도 GitHub가 **5분마다 자동으로** 확인해서 알림을 보내줍니다. 서버 0대, 공개 저장소면 무료.

> 📁 워크플로 파일: `.github/workflows/cafe-alert.yml` (이미 포함됨)

설정은 딱 3가지:

**① 저장소를 공개로 전환** (공개면 Actions 무료)
- GitHub 저장소 → `Settings` → `General` → 맨 아래 `Danger Zone` → `Change visibility` → **Public**

**② 알림 비밀값 등록** (코드에 토큰을 안 넣고 안전하게)
- 저장소 → `Settings` → `Secrets and variables` → `Actions` → `New repository secret`
- 아래 2개(비공개 카페면 3개) 등록:
  | 이름 | 값 |
  |------|------|
  | `TELEGRAM_BOT_TOKEN` | BotFather 토큰 |
  | `TELEGRAM_CHAT_ID` | getUpdates 로 확인한 숫자 |
  | `NAVER_COOKIE` | (비공개 카페일 때만) 로그인 쿠키 |

**③ 기본 브랜치에 올리기** ⚠️ 중요
- GitHub 스케줄(cron)은 **기본 브랜치(main/master)** 에 있는 워크플로만 자동 실행됩니다.
- 따라서 이 브랜치를 기본 브랜치로 **병합(merge)** 해야 5분마다 자동으로 돌아갑니다.
- 감시 대상(카페/키워드)을 바꾸려면 `cafe-alert.yml` 위쪽 `NAVER_CLUB_ID/MENU_ID/KEYWORD` 값만 고치면 됩니다.

설정 후 `Actions` 탭에서 워크플로 선택 → `Run workflow` 로 **수동 1회 실행**해 동작을 바로 확인할 수 있어요.
(첫 실행은 기준점만 잡고, 그 다음 실행부터 새 글 알림이 갑니다.)

## 파일 구조

| 파일 | 설명 |
|------|------|
| `monitor.py` | 메인 루프(감시 + 키워드/새 글 판별 + 알림) |
| `cafe.py` | 네이버 카페 글 목록 가져오기 |
| `notifier.py` | 텔레그램/SMS 발송 |
| `.env` | 내 설정값 (깃에 올라가지 않음) |
| `seen_articles.json` | 이미 알린 글 기록 (자동 생성) |
