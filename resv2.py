import dxcam
import numpy as np
import keyboard
import time
import pyautogui
from PIL import ImageGrab

# 設定座標
target_x = 360
target_y = 915

# 精確顏色值
EXACT_BLUE = np.array([39, 131, 242])   # 精確藍色
EXACT_GREEN = np.array([0, 145, 68])    # 精確綠色

# 允許的顏色誤差範圍（每個分量±5以內）
COLOR_TOLERANCE = 5

# 按鍵狀態管理
key_states = {'x': False, 'z': False}  # 追踪按鍵是否被按住
current_color = None  # 當前檢測到的顏色

def is_color_in_range(color, min_range, max_range):
    return np.all(color >= min_range) and np.all(color <= max_range)

def is_exact_color_match(color, target_color, tolerance=COLOR_TOLERANCE):
    """檢測顏色是否與目標顏色匹配（在容差範圍內）"""
    diff = np.abs(color - target_color)
    return np.all(diff <= tolerance)

def is_green_color(color):
    """檢測是否為精確綠色 RGB(0,145,68)"""
    return is_exact_color_match(color, EXACT_GREEN)

def is_blue_color(color):
    """檢測是否為精確藍色 RGB(39,131,242)"""
    return is_exact_color_match(color, EXACT_BLUE)

def handle_color_detection(pixel_color):
    """處理顏色檢測和按鍵控制"""
    global key_states, current_color
    
    detected_color = None
    
    # 檢測顏色
    if is_green_color(pixel_color):
        detected_color = 'green'
    elif is_blue_color(pixel_color):
        detected_color = 'blue'
    
    # 如果檢測到綠色
    if detected_color == 'green':
        if not key_states['x']:
            keyboard.press('x')
            key_states['x'] = True
            print(f"綠色檢測到! RGB: {pixel_color} -> 開始按住 X")
        
        # 如果之前按住 Z，現在釋放
        if key_states['z']:
            keyboard.release('z')
            key_states['z'] = False
            print("釋放 Z (切換到綠色)")
    
    # 如果檢測到藍色
    elif detected_color == 'blue':
        if not key_states['z']:
            keyboard.press('z')
            key_states['z'] = True
            print(f"藍色檢測到! RGB: {pixel_color} -> 開始按住 Z")
        
        # 如果之前按住 X，現在釋放
        if key_states['x']:
            keyboard.release('x')
            key_states['x'] = False
            print("釋放 X (切換到藍色)")
    
    # 如果沒有檢測到任何目標顏色
    else:
        # 釋放所有按鍵
        if key_states['x']:
            keyboard.release('x')
            key_states['x'] = False
            print("綠色消失 -> 釋放 X")
        
        if key_states['z']:
            keyboard.release('z')
            key_states['z'] = False
            print("藍色消失 -> 釋放 Z")
    
    current_color = detected_color

def cleanup_keys():
    """清理函數：確保所有按鍵都被釋放"""
    global key_states
    for key in key_states:
        if key_states[key]:
            keyboard.release(key)
            key_states[key] = False
            print(f"清理：釋放按鍵 {key.upper()}")

def method1_dxcam():
    """方法1: 使用 DXCam"""
    print("嘗試使用 DXCam...")
    
    try:
        camera = dxcam.create()
        if camera is None:
            return False
            
        success_count = 0
        fail_count = 0
        
        while True:
            if keyboard.is_pressed('esc'):
                break
                
            frame = camera.grab()
            if frame is None:
                fail_count += 1
                if fail_count > 10:
                    print("DXCam 失敗次數過多，切換到其他方法")
                    return False
                time.sleep(0.01)
                continue
            
            success_count += 1
            fail_count = 0
            
            # 檢查座標
            if target_y >= frame.shape[0] or target_x >= frame.shape[1]:
                print(f"座標超出範圍！畫面大小: {frame.shape[1]}x{frame.shape[0]}")
                continue

            pixel_color = frame[target_y, target_x]
            
            # 每500幀顯示一次顏色
            if success_count % 500 == 0:
                print(f"座標 ({target_x}, {target_y}) RGB: {pixel_color}")
            
            # 顏色檢測和按鍵處理
            handle_color_detection(pixel_color)
            
            time.sleep(0.005)
            
    except Exception as e:
        print(f"DXCam 錯誤: {e}")
        return False
    finally:
        cleanup_keys()  # 確保釋放所有按鍵
        if 'camera' in locals():
            camera.stop()
    
    return True

def method2_pil():
    """方法2: 使用 PIL ImageGrab"""
    print("使用 PIL ImageGrab...")
    
    try:
        frame_count = 0
        while True:
            if keyboard.is_pressed('esc'):
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
            if frame_count % 200 == 0:
                print(f"座標 ({target_x}, {target_y}) RGB: {pixel_color}")
            
            # 顏色檢測和按鍵處理
            handle_color_detection(pixel_color)
            
            time.sleep(0.02)  # PIL 比較慢，增加延遲
            
    except Exception as e:
        print(f"PIL 方法錯誤: {e}")
    finally:
        cleanup_keys()  # 確保釋放所有按鍵

def method3_pyautogui():
    """方法3: 使用 PyAutoGUI"""
    print("使用 PyAutoGUI...")
    try:
        frame_count = 0
        while True:
            if keyboard.is_pressed('esc'):
                break

            # 只抓取目標像素附近的小區域以提高效能
            region = (target_x-1, target_y-1, 3, 3)
            screenshot = pyautogui.screenshot(region=region)
            pixel_color = np.array(screenshot.getpixel((1, 1)))  # 中心像素

            frame_count += 1
            if frame_count % 200 == 0:
                print(f"座標 ({target_x}, {target_y}) RGB: {pixel_color}")

            # 直接統一呼叫顏色檢測與按鍵處理
            handle_color_detection(pixel_color)

            time.sleep(0.02)

    except Exception as e:
        print(f"PyAutoGUI 方法錯誤: {e}")
    finally:
        cleanup_keys()  # 確保釋放所有按鍵
# 主程式
if __name__ == "__main__":
    print("顏色檢測程式啟動")
    print("按 ESC 鍵退出")
    print(f"監控座標: ({target_x}, {target_y})")
    print("="*50)
    try:
        # 先嘗試 DXCam
        if not method1_dxcam():
            print("\nDXCam 失敗，嘗試 PIL...")
            try:
                method2_pil()
            except:
                print("\nPIL 失敗，嘗試 PyAutoGUI...")
                method3_pyautogui()
    finally:
        cleanup_keys()  # 確保釋放所有按鍵
        print("程式結束")