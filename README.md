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

## EXE 파일로 만들기 (설치 없이 실행)

`.exe` 로 만들면 Python 이 없는 PC 에서도 더블클릭만으로 실행됩니다.

### 방법 A. GitHub Actions 로 자동 빌드 (PC 에 설치 불필요)
1. 코드를 GitHub 에 푸시하면 **Windows 가상머신이 자동으로 빌드**합니다.
2. GitHub 레포 → **Actions** 탭 → 최근 실행 → 아래 **Artifacts** 의
   `Calculator-windows-exe` 를 내려받으면 `Calculator.exe` 가 들어 있습니다.
3. 수동 실행: Actions 탭에서 **Build Windows EXE** → **Run workflow** 클릭.

> ⚠️ Windows `.exe` 는 반드시 Windows 에서 빌드해야 합니다. (PyInstaller 는
> 크로스 컴파일을 지원하지 않으므로 Linux/macOS 에서는 만들 수 없습니다.)

### 방법 B. 내 Windows PC 에서 직접 빌드
```cmd
pip install pyinstaller
pyinstaller --onefile --windowed --name 계산기 calculator.py
```
완료되면 `dist\계산기.exe` 가 생성됩니다.

## 기능

- 사칙연산: `+`, `−`, `×`, `÷`
- 백분율(`%`), 소수점, 지우기(`C`), 한 글자 삭제(`←`)
- **키보드 입력 지원**
  - 숫자/`.` , `+ - * /` , `%`
  - `Enter` = 계산, `Backspace` = 삭제, `Esc` = 전체 지우기
- 0으로 나누기 등 오류 상황 안전 처리
