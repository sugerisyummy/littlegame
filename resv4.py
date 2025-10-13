import numpy as np
import keyboard
import time
import pyautogui
from PIL import ImageGrab
import sys
import atexit

# 設定座標
target_x = 360
target_y = 890

# 精確顏色值
EXACT_BLUE = np.array([39, 131, 242])    # 精確藍色 (Z)
EXACT_GREEN = np.array([0, 145, 68])     # 精確綠色 (X)
EXACT_ORANGE = np.array([255, 106, 41])  # 精確橘色 (Z)
EXACT_PURPLE = np.array([80, 46, 188])   # 精確紫色 (X)

# 允許的顏色誤差範圍
COLOR_TOLERANCE = 5

# 按鍵狀態管理
key_states = {'x': False, 'z': False}
current_color = None

def is_exact_color_match(color, target_color, tolerance=COLOR_TOLERANCE):
    """檢測顏色是否與目標顏色匹配（在容差範圍內）"""
    diff = np.abs(color - target_color)
    return np.all(diff <= tolerance)

def is_green_color(color):
    """檢測是否為精確綠色 RGB(0,145,68) -> X"""
    return is_exact_color_match(color, EXACT_GREEN)

def is_blue_color(color):
    """檢測是否為精確藍色 RGB(39,131,242) -> Z"""
    return is_exact_color_match(color, EXACT_BLUE)

def is_orange_color(color):
    """檢測是否為精確橘色 RGB(255,106,41) -> Z"""
    return is_exact_color_match(color, EXACT_ORANGE)

def is_purple_color(color):
    """檢測是否為精確紫色 RGB(80,46,188) -> X"""
    return is_exact_color_match(color, EXACT_PURPLE)

def cleanup_keys():
    """清理函數：確保所有按鍵都被釋放"""
    global key_states
    try:
        for key in key_states:
            if key_states[key]:
                keyboard.release(key)
                key_states[key] = False
                print(f"清理：釋放按鍵 {key.upper()}")
    except:
        pass

def handle_color_detection(pixel_color):
    """處理顏色檢測和按鍵控制"""
    global key_states, current_color
    
    detected_color = None
    
    # 檢測所有顏色
    if is_green_color(pixel_color):
        detected_color = 'green'
    elif is_purple_color(pixel_color):
        detected_color = 'purple'
    elif is_blue_color(pixel_color):
        detected_color = 'blue'
    elif is_orange_color(pixel_color):
        detected_color = 'orange'
    
    # 處理 X 按鍵 (綠色或紫色)
    should_press_x = detected_color in ['green', 'purple']
    if should_press_x:
        if not key_states['x']:
            keyboard.press('x')
            key_states['x'] = True
            color_name = "綠色" if detected_color == 'green' else "紫色"
            print(f"{color_name}檢測到! RGB: {pixel_color} -> 開始按住 X")
        
        # 釋放 Z 如果正在按
        if key_states['z']:
            keyboard.release('z')
            key_states['z'] = False
            print("釋放 Z (切換到 X)")
    
    # 處理 Z 按鍵 (藍色或橘色)
    should_press_z = detected_color in ['blue', 'orange']
    if should_press_z:
        if not key_states['z']:
            keyboard.press('z')
            key_states['z'] = True
            color_name = "藍色" if detected_color == 'blue' else "橘色"
            print(f"{color_name}檢測到! RGB: {pixel_color} -> 開始按住 Z")
        
        # 釋放 X 如果正在按
        if key_states['x']:
            keyboard.release('x')
            key_states['x'] = False
            print("釋放 X (切換到 Z)")
    
    # 如果沒有檢測到任何目標顏色
    if not should_press_x and not should_press_z:
        # 釋放所有按鍵
        if key_states['x']:
            keyboard.release('x')
            key_states['x'] = False
            print("目標顏色消失 -> 釋放 X")
        
        if key_states['z']:
            keyboard.release('z')
            key_states['z'] = False
            print("目標顏色消失 -> 釋放 Z")
    
    current_color = detected_color

def method_pil():
    """使用 PIL ImageGrab（最穩定的方法）"""
    print("使用 PIL ImageGrab...")
    
    try:
        frame_count = 0
        while True:
            if keyboard.is_pressed('esc'):
                print("按下 ESC，正在退出...")
                break
            
            # 使用 PIL 截圖
            screenshot = ImageGrab.grab()
            screenshot_np = np.array(screenshot)
            
            # 檢查座標
            if target_y >= screenshot_np.shape[0] or target_x >= screenshot_np.shape[1]:
                print(f"座標超出範圍！螢幕大小: {screenshot_np.shape[1]}x{screenshot_np.shape[0]}")
                time.sleep(1)
                continue
            
            pixel_color = screenshot_np[target_y, target_x]
            
            frame_count += 1
            if frame_count % 300 == 0:
                print(f"座標 ({target_x}, {target_y}) RGB: {pixel_color}")
            
            # 顏色檢測和按鍵處理
            handle_color_detection(pixel_color)
            
            time.sleep(0.01)  # 適中的延遲
            
    except KeyboardInterrupt:
        print("\n程式被中斷")
    except Exception as e:
        print(f"PIL 方法錯誤: {e}")
    finally:
        cleanup_keys()

def method_pyautogui():
    """使用 PyAutoGUI（備用方法）"""
    print("使用 PyAutoGUI...")
    
    try:
        frame_count = 0
        while True:
            if keyboard.is_pressed('esc'):
                print("按下 ESC，正在退出...")
                break
            
            # 只抓取目標像素
            pixel_color = np.array(pyautogui.pixel(target_x, target_y))
            
            frame_count += 1
            if frame_count % 300 == 0:
                print(f"座標 ({target_x}, {target_y}) RGB: {pixel_color}")
            
            # 顏色檢測和按鍵處理
            handle_color_detection(pixel_color)
            
            time.sleep(0.01)
            
    except KeyboardInterrupt:
        print("\n程式被中斷")
    except Exception as e:
        print(f"PyAutoGUI 方法錯誤: {e}")
    finally:
        cleanup_keys()

# 註冊清理函數
atexit.register(cleanup_keys)

# 主程式
if __name__ == "__main__":
    print("穩定版顏色檢測程式啟動")
    print("按 ESC 鍵退出")
    print(f"監控座標: ({target_x}, {target_y})")
    print("\n顏色映射:")
    print("🟢 綠色 RGB(0,145,68) -> 按住 X")
    print("🟣 紫色 RGB(80,46,188) -> 按住 X") 
    print("🔵 藍色 RGB(39,131,242) -> 按住 Z")
    print("🟠 橘色 RGB(255,106,41) -> 按住 Z")
    print("="*50)
    
    try:
        # 優先使用 PIL（避免 DXCam 的 comtypes 問題）
        print("嘗試 PIL 方法...")
        method_pil()
        
    except Exception as e:
        print(f"PIL 失敗: {e}")
        print("嘗試 PyAutoGUI 方法...")
        try:
            method_pyautogui()
        except Exception as e2:
            print(f"PyAutoGUI 也失敗: {e2}")
    
    finally:
        cleanup_keys()
        print("程式安全結束")