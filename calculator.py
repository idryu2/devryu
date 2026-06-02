"""
Windows 계산기 (Calculator)

Python 표준 라이브러리 tkinter 만으로 동작하는 GUI 계산기입니다.
별도의 패키지 설치 없이 Windows / macOS / Linux 어디서나 실행됩니다.

실행 방법:
    python calculator.py
"""

import tkinter as tk
from tkinter import font as tkfont


class Calculator(tk.Tk):
    """간단하고 깔끔한 사칙연산 계산기."""

    # 색상 테마
    BG = "#1e1e2e"
    DISPLAY_BG = "#11111b"
    DISPLAY_FG = "#cdd6f4"
    NUM_BG = "#313244"
    NUM_FG = "#cdd6f4"
    OP_BG = "#fab387"
    OP_FG = "#11111b"
    EQ_BG = "#a6e3a1"
    EQ_FG = "#11111b"
    CLR_BG = "#f38ba8"
    CLR_FG = "#11111b"

    def __init__(self):
        super().__init__()
        self.title("계산기")
        self.configure(bg=self.BG)
        self.resizable(False, False)

        # 입력 수식과 마지막 결과 표시 여부
        self.expression = ""
        self.just_evaluated = False

        self._build_display()
        self._build_buttons()
        self._bind_keys()

    # ----- UI 구성 -----
    def _build_display(self):
        self.display_var = tk.StringVar(value="0")
        display_font = tkfont.Font(family="Segoe UI", size=28, weight="bold")
        display = tk.Label(
            self,
            textvariable=self.display_var,
            anchor="e",
            bg=self.DISPLAY_BG,
            fg=self.DISPLAY_FG,
            font=display_font,
            padx=16,
            pady=24,
        )
        display.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=8, pady=(8, 4))

    def _build_buttons(self):
        # (라벨, 행, 열, 종류, [colspan])
        buttons = [
            ("C", 1, 0, "clr"), ("←", 1, 1, "clr"), ("%", 1, 2, "op"), ("÷", 1, 3, "op"),
            ("7", 2, 0, "num"), ("8", 2, 1, "num"), ("9", 2, 2, "num"), ("×", 2, 3, "op"),
            ("4", 3, 0, "num"), ("5", 3, 1, "num"), ("6", 3, 2, "num"), ("−", 3, 3, "op"),
            ("1", 4, 0, "num"), ("2", 4, 1, "num"), ("3", 4, 2, "num"), ("+", 4, 3, "op"),
            ("0", 5, 0, "num", 2), (".", 5, 2, "num"), ("=", 5, 3, "eq"),
        ]

        btn_font = tkfont.Font(family="Segoe UI", size=18)
        colors = {
            "num": (self.NUM_BG, self.NUM_FG),
            "op": (self.OP_BG, self.OP_FG),
            "eq": (self.EQ_BG, self.EQ_FG),
            "clr": (self.CLR_BG, self.CLR_FG),
        }

        for spec in buttons:
            label, row, col, kind = spec[:4]
            colspan = spec[4] if len(spec) > 4 else 1
            bg, fg = colors[kind]
            btn = tk.Button(
                self,
                text=label,
                font=btn_font,
                bg=bg,
                fg=fg,
                activebackground=bg,
                activeforeground=fg,
                bd=0,
                relief="flat",
                width=4,
                height=1,
                command=lambda l=label: self.on_press(l),
            )
            btn.grid(
                row=row,
                column=col,
                columnspan=colspan,
                sticky="nsew",
                padx=4,
                pady=4,
            )

        # 그리드 크기 균등 분배
        for c in range(4):
            self.grid_columnconfigure(c, weight=1, minsize=70)
        for r in range(1, 6):
            self.grid_rowconfigure(r, weight=1, minsize=64)

    def _bind_keys(self):
        for key in "0123456789.+-*/%":
            self.bind(key, lambda e, k=key: self.on_press(self._map_key(k)))
        self.bind("<Return>", lambda e: self.on_press("="))
        self.bind("<KP_Enter>", lambda e: self.on_press("="))
        self.bind("<BackSpace>", lambda e: self.on_press("←"))
        self.bind("<Escape>", lambda e: self.on_press("C"))

    @staticmethod
    def _map_key(key):
        """키보드 입력을 버튼 라벨로 변환."""
        return {"*": "×", "/": "÷", "-": "−"}.get(key, key)

    # ----- 동작 -----
    def on_press(self, label):
        if label == "C":
            self.expression = ""
        elif label == "←":
            self.expression = self.expression[:-1]
        elif label == "=":
            self._evaluate()
            return
        else:
            # 결과 표시 직후 숫자를 누르면 새로 시작
            if self.just_evaluated and label not in "+-×÷−%":
                self.expression = ""
            self.just_evaluated = False
            self.expression += label

        self._update_display()

    def _evaluate(self):
        if not self.expression:
            return
        # 화면 기호를 파이썬 연산자로 변환
        expr = (
            self.expression.replace("×", "*")
            .replace("÷", "/")
            .replace("−", "-")
            .replace("%", "/100")
        )
        try:
            result = eval(expr, {"__builtins__": {}}, {})  # noqa: S307 (입력은 숫자/연산자로 제한)
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            self.expression = str(result)
            self.just_evaluated = True
        except ZeroDivisionError:
            self.expression = ""
            self.display_var.set("0으로 나눌 수 없음")
            return
        except Exception:
            self.expression = ""
            self.display_var.set("오류")
            return
        self._update_display()

    def _update_display(self):
        self.display_var.set(self.expression if self.expression else "0")


if __name__ == "__main__":
    Calculator().mainloop()
