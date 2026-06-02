# 계산기 (Calculator)

Windows에서 바로 실행할 수 있는 GUI 계산기입니다. Python 표준 라이브러리인
`tkinter`만 사용하므로 **별도 패키지 설치가 필요 없습니다.**

## 실행 방법

### 방법 1. 더블클릭 (가장 간단)
`계산기_실행.bat` 파일을 더블클릭하세요.

### 방법 2. 명령 프롬프트
```cmd
python calculator.py
```

> Python이 없다면 [python.org](https://www.python.org/downloads/)에서
> 설치하세요. 설치 시 **"Add Python to PATH"** 옵션을 꼭 체크하세요.
> (tkinter는 Windows용 Python 설치 파일에 기본 포함되어 있습니다.)

## 기능

- 사칙연산: `+`, `−`, `×`, `÷`
- 백분율(`%`), 소수점, 지우기(`C`), 한 글자 삭제(`←`)
- **키보드 입력 지원**
  - 숫자/`.` , `+ - * /` , `%`
  - `Enter` = 계산, `Backspace` = 삭제, `Esc` = 전체 지우기
- 0으로 나누기 등 오류 상황 안전 처리
