import time, pyautogui, keyboard

print("3 秒後開始（切到目標視窗）。按 ESC 可退出。")
time.sleep(3)

while True:
    if keyboard.is_pressed('esc'):
        print("收到 ESC，已退出。")
        break
    pyautogui.typewrite('p') 
    pyautogui.press('enter')
    time.sleep(1.2)  