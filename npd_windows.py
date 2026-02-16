# -*- coding: utf-8 -*-
"""
隐性NPD母亲内在程序模型 — Windows 图形界面

依赖：同目录下的 npd.py（逻辑与数据）。
交互：左侧选择触发情境 → 上方固定显示三条 CoreNeed 与供给升级路径 → 中间为当前 PatternCard，左右翻页查看。
"""

import tkinter as tk
from tkinter import ttk, font as tkfont
from typing import List, Optional

try:
    from npd import (
        TriggerType,
        CoreNeed,
        get_cards_for_trigger,
        get_trigger_description,
        describe_trigger_and_patterns,
    )
    from npd import PatternCard  # type: ignore
except ImportError:
    TriggerType = None
    CoreNeed = None
    get_cards_for_trigger = None
    get_trigger_description = None
    describe_trigger_and_patterns = None
    PatternCard = None


# 界面字体（Windows 下中文）
FONT_UI = ("Microsoft YaHei UI", 10)
FONT_TITLE = ("Microsoft YaHei UI", 11, "bold")
FONT_CARD_TITLE = ("Microsoft YaHei UI", 12, "bold")


def _build_core_need_titles_only() -> str:
    """只展示三条核心需求的标题，不展示表现/描述。"""
    if CoreNeed is None:
        return "【未找到 npd 模块】"
    lines = ["【三条核心需求】", ""]
    for need in CoreNeed:
        lines.append(f"  · {need.name}")
    return "\n".join(lines)


def _card_to_display_text(card: "PatternCard") -> str:
    return (
        f"【{card.pattern.name}】\n\n"
        f"表现：\n{card.description}\n\n"
        f"疗愈提示：\n{card.healing_note}"
    )


class NPDApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("隐性NPD父母 · 内在程序模型")
        self.minsize(800, 560)
        self.geometry("900x600")

        # 当前选中的 trigger 及该 trigger 下的卡片列表、当前索引
        self._current_trigger: Optional[TriggerType] = None
        self._cards: List[PatternCard] = []
        self._card_index: int = 0

        self._setup_fonts()
        self._build_ui()

    def _setup_fonts(self):
        """确保有可用中文字体。"""
        try:
            tkfont.nametofont("TkDefaultFont").configure(family="Microsoft YaHei UI", size=10)
        except Exception:
            pass

    def _build_escalation_diagram(self, parent):
        """在 parent 上绘制供给升级路径图：崇拜 → 恐惧 → 怜悯。"""
        title = tk.Label(parent, text="【供给升级路径】", font=FONT_TITLE)
        title.pack(anchor=tk.W)
        row = tk.Frame(parent)
        row.pack(anchor=tk.W, pady=4)
        # 崇拜（一级）
        box1 = tk.Frame(row, relief=tk.RIDGE, borderwidth=2, padx=12, pady=6)
        box1.pack(side=tk.LEFT)
        tk.Label(box1, text="崇拜", font=FONT_UI).pack()
        tk.Label(box1, text="一级", font=("Microsoft YaHei UI", 9), fg="gray").pack()
        tk.Label(row, text="  →   ", font=FONT_UI).pack(side=tk.LEFT)
        # 恐惧（二级）
        box2 = tk.Frame(row, relief=tk.RIDGE, borderwidth=2, padx=12, pady=6)
        box2.pack(side=tk.LEFT)
        tk.Label(box2, text="恐惧", font=FONT_UI).pack()
        tk.Label(box2, text="二级", font=("Microsoft YaHei UI", 9), fg="gray").pack()
        tk.Label(row, text="  →   ", font=FONT_UI).pack(side=tk.LEFT)
        # 怜悯（三级）
        box3 = tk.Frame(row, relief=tk.RIDGE, borderwidth=2, padx=12, pady=6)
        box3.pack(side=tk.LEFT)
        tk.Label(box3, text="怜悯", font=FONT_UI).pack()
        tk.Label(box3, text="三级", font=("Microsoft YaHei UI", 9), fg="gray").pack()
        hint = tk.Label(parent, text="崇拜不足时升为恐惧（威胁、惩罚）；恐惧失效则转为怜悯（扮演受害者、自怜）", font=("Microsoft YaHei UI", 9), fg="gray")
        hint.pack(anchor=tk.W, pady=(2, 0))

    def _build_ui(self):
        main = ttk.Frame(self, padding=8)
        main.pack(fill=tk.BOTH, expand=True)

        # 左侧：触发情境列表
        left = ttk.LabelFrame(main, text="触发情境", padding=6)
        left.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 8))
        self._trigger_listbox = tk.Listbox(
            left,
            font=FONT_UI,
            height=22,
            width=22,
            selectmode=tk.SINGLE,
            activestyle=tk.DOTBOX,
            highlightthickness=1,
        )
        self._trigger_listbox.pack(fill=tk.BOTH, expand=True)
        self._trigger_listbox.bind("<<ListboxSelect>>", self._on_trigger_select)
        if TriggerType is not None:
            for t in TriggerType:
                self._trigger_listbox.insert(tk.END, t.name)

        # 右侧：上方固定 CoreNeed + Escalation，中间卡片 + 翻页
        right = ttk.Frame(main)
        right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 上方固定：CoreNeed（仅标题）与供给升级路径图
        top_frame = ttk.LabelFrame(right, text="程序核心", padding=6)
        top_frame.pack(fill=tk.X, pady=(0, 8))

        self._core_need_var = tk.StringVar(value=_build_core_need_titles_only())
        core_lbl = tk.Label(
            top_frame,
            textvariable=self._core_need_var,
            font=FONT_UI,
            justify=tk.LEFT,
            anchor=tk.NW,
            wraplength=620,
        )
        core_lbl.pack(anchor=tk.W)

        # 供给升级路径：用图示展示 崇拜 → 恐惧 → 怜悯
        esc_canvas_frame = ttk.Frame(top_frame)
        esc_canvas_frame.pack(fill=tk.X, pady=(10, 0))
        self._build_escalation_diagram(esc_canvas_frame)

        # 中间：当前 PatternCard
        card_frame = ttk.LabelFrame(right, text="行为模式卡片", padding=8)
        card_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 8))

        self._card_text = tk.Text(
            card_frame,
            font=FONT_UI,
            wrap=tk.WORD,
            height=10,
            state=tk.DISABLED,
            padx=8,
            pady=8,
        )
        self._card_text.pack(fill=tk.BOTH, expand=True)

        # 页码与翻页按钮
        nav_frame = ttk.Frame(card_frame)
        nav_frame.pack(fill=tk.X, pady=(8, 0))

        self._page_var = tk.StringVar(value="请先选择左侧的触发情境")
        ttk.Label(nav_frame, textvariable=self._page_var).pack(side=tk.LEFT)

        btn_frame = ttk.Frame(nav_frame)
        btn_frame.pack(side=tk.RIGHT)

        self._btn_prev = ttk.Button(btn_frame, text="← 上一页", command=self._prev_card)
        self._btn_prev.pack(side=tk.LEFT, padx=2)
        self._btn_next = ttk.Button(btn_frame, text="下一页 →", command=self._next_card)
        self._btn_next.pack(side=tk.LEFT, padx=2)

        self._update_card_display()

    def _on_trigger_select(self, event):
        w = event.widget
        sel = w.curselection()
        if not sel or TriggerType is None:
            return
        idx = int(sel[0])
        triggers = list(TriggerType)
        if idx < 0 or idx >= len(triggers):
            return
        self._current_trigger = triggers[idx]
        self._cards = get_cards_for_trigger(self._current_trigger) if get_cards_for_trigger else []
        self._card_index = 0
        self._update_card_display()

    def _prev_card(self):
        if not self._cards:
            return
        self._card_index = (self._card_index - 1) % len(self._cards)
        self._update_card_display()

    def _next_card(self):
        if not self._cards:
            return
        self._card_index = (self._card_index + 1) % len(self._cards)
        self._update_card_display()

    def _update_card_display(self):
        if not self._cards:
            self._page_var.set("请先选择左侧的触发情境")
            self._card_text.config(state=tk.NORMAL)
            self._card_text.delete("1.0", tk.END)
            self._card_text.insert(tk.END, "选择左侧任一触发情境后，此处将显示对应的行为模式卡片，可通过下方按钮翻页。")
            self._card_text.config(state=tk.DISABLED)
            self._btn_prev.state(["disabled"])
            self._btn_next.state(["disabled"])
            return

        n = len(self._cards)
        self._page_var.set(f"第 {self._card_index + 1} / {n} 张")
        self._btn_prev.state(["!disabled"])
        self._btn_next.state(["!disabled"])

        card = self._cards[self._card_index]
        self._card_text.config(state=tk.NORMAL)
        self._card_text.delete("1.0", tk.END)
        self._card_text.insert(tk.END, _card_to_display_text(card))
        self._card_text.see("1.0")
        self._card_text.config(state=tk.DISABLED)
        self._card_text.update_idletasks()


def main():
    if TriggerType is None:
        root = tk.Tk()
        root.title("错误")
        tk.Label(
            root,
            text="请将 npd.py 放在同目录下后再运行 npd_windows.py。",
            font=("Microsoft YaHei UI", 12),
            padx=20,
            pady=20,
        ).pack()
        root.mainloop()
        return
    app = NPDApp()
    app.mainloop()


if __name__ == "__main__":
    main()
