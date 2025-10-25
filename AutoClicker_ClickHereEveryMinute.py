# -*- coding: utf-8 -*-
"""
AutoClicker_ClickHereEveryMinute.py — 每 1 分鐘在指定座標自動點一下滑鼠（Windows）

特色
- 免安裝套件（純 ctypes / 標準庫）。
- 預設 60 秒點擊一次左鍵，會先抓「目前游標位置」當成目標點。
- 點擊時會「瞬移到目標點→點一下→再回到原位置」，盡量不干擾操作。
- 主控台快捷鍵：
  - c : 重新以「目前游標位置」為目標點
  - p : 暫停/繼續
  - q : 結束
  
  - + / - : 間隔每次 ±5 秒
- 可用參數：--interval / -i 設定秒數（預設 60）、--button 設 left/right/middle（預設 left）。

注意
- 這是系統層「真正的點擊」，會影響目前前景視窗。
- 若你想要「背景點擊不切到前景」且對特定視窗送坐標點擊，需改為對該視窗 PostMessage/SendMessage，
  但許多遊戲/程式不接受此法；此檔先提供最通用且穩定的 SendInput 版本。
"""

import time
import argparse
import ctypes
from ctypes import wintypes
import sys
import msvcrt  # Windows console 熱鍵讀取

# 解析參數
parser = argparse.ArgumentParser(description="每隔一段時間在指定螢幕座標自動點擊。")
parser.add_argument("-i", "--interval", type=float, default=60.0, help="點擊間隔秒數（預設 60）")
parser.add_argument("--button", choices=["left", "right", "middle"], default="left", help="滑鼠按鍵（預設 left）")
args = parser.parse_args()

INTERVAL = max(0.5, float(args.interval))  # 最短 0.5s 保護
BUTTON = args.button

# Win32 結構與常數
user32 = ctypes.windll.user32

class POINT(ctypes.Structure):
    _fields_ = [("x", wintypes.LONG),
                ("y", wintypes.LONG)]

# SendInput 定義
PUL = ctypes.POINTER(ctypes.c_ulong)

class MOUSEINPUT(ctypes.Structure):
    _fields_ = [
        ("dx", wintypes.LONG),
        ("dy", wintypes.LONG),
        ("mouseData", wintypes.DWORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", PUL)
    ]

class INPUT(ctypes.Structure):
    class _INPUT_UNION(ctypes.Union):
        _fields_ = [("mi", MOUSEINPUT)]
    _anonymous_ = ("u",)
    _fields_ = [("type", wintypes.DWORD),
                ("u", _INPUT_UNION)]

INPUT_MOUSE = 0

# 滑鼠事件旗標
MOUSEEVENTF_MOVE        = 0x0001
MOUSEEVENTF_LEFTDOWN    = 0x0002
MOUSEEVENTF_LEFTUP      = 0x0004
MOUSEEVENTF_RIGHTDOWN   = 0x0008
MOUSEEVENTF_RIGHTUP     = 0x0010
MOUSEEVENTF_MIDDLEDOWN  = 0x0020
MOUSEEVENTF_MIDDLEUP    = 0x0040
MOUSEEVENTF_ABSOLUTE    = 0x8000

def get_cursor_pos():
    pt = POINT()
    user32.GetCursorPos(ctypes.byref(pt))
    return pt.x, pt.y

def set_cursor_pos(x, y):
    user32.SetCursorPos(int(x), int(y))

def send_mouse_click(button="left"):
    if button == "left":
        down_flag, up_flag = MOUSEEVENTF_LEFTDOWN, MOUSEEVENTF_LEFTUP
    elif button == "right":
        down_flag, up_flag = MOUSEEVENTF_RIGHTDOWN, MOUSEEVENTF_RIGHTUP
    else:
        down_flag, up_flag = MOUSEEVENTF_MIDDLEDOWN, MOUSEEVENTF_MIDDLEUP

    inp_down = INPUT(type=INPUT_MOUSE, mi=MOUSEINPUT(0, 0, 0, down_flag, 0, None))
    inp_up   = INPUT(type=INPUT_MOUSE, mi=MOUSEINPUT(0, 0, 0, up_flag,   0, None))
    user32.SendInput(1, ctypes.byref(inp_down), ctypes.sizeof(INPUT))
    user32.SendInput(1, ctypes.byref(inp_up),   ctypes.sizeof(INPUT))

def click_at(x, y, button="left", restore_cursor=True):
    oldx, oldy = get_cursor_pos()
    set_cursor_pos(x, y)
    time.sleep(0.01)  # 小延遲避免 miss
    send_mouse_click(button=button)
    if restore_cursor:
        set_cursor_pos(oldx, oldy)

def banner():
    print(">>> AutoClicker — 每隔固定時間在指定位置自動點擊（Windows）")
    print(f"    間隔：{INTERVAL:.1f} 秒，按鍵：{BUTTON}")
    print("    操作：c=重設目標  p=暫停/繼續  +=+5秒  -=-5秒  q=離開")
    print("    3 秒後會以【目前游標位置】作為目標...")
    for i in (3,2,1):
        sys.stdout.write(f"      請把游標移到要點的地方… {i}\r")
        sys.stdout.flush()
        time.sleep(1)
    print()

def main():
    global INTERVAL
    banner()
    target = get_cursor_pos()
    print(f"目標座標已設定為：{target}")

    paused = False
    next_time = time.monotonic() + INTERVAL

    while True:
        # 處理鍵盤指令（非阻塞）
        if msvcrt.kbhit():
            ch = msvcrt.getwch()
            if ch in ("q", "Q"):
                print("收到離開指令，結束。")
                break
            elif ch in ("c", "C"):
                target = get_cursor_pos()
                print(f"重新設定目標座標：{target}")
            elif ch in ("p", "P"):
                paused = not paused
                state = "暫停" if paused else "繼續"
                print(f"{state}。")
                if not paused:
                    next_time = time.monotonic() + INTERVAL
            elif ch == "+":
                INTERVAL = min(3600.0, INTERVAL + 5.0)
                print(f"間隔改為 {INTERVAL:.1f} 秒")
            elif ch == "-":
                INTERVAL = max(0.5, INTERVAL - 5.0)
                print(f"間隔改為 {INTERVAL:.1f} 秒")

        now = time.monotonic()
        if not paused and now >= next_time:
            x, y = target
            click_at(x, y, button=BUTTON, restore_cursor=True)
            print(f"[{time.strftime('%H:%M:%S')}] 已點擊 {BUTTON} 於 {target}")
            next_time += INTERVAL

        # 小睡一下避免佔滿 CPU
        time.sleep(0.02)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n已結束。")
