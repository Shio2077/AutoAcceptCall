from PIL import ImageGrab
import numpy as np
import cv2
import sys, time, ctypes
import win32api
import os
import mss

THRESHOLD = 0.9
SCREEN_MAGNI = 1

try: 
    ctypes.windll.user32.SetProcessDPIAware()
    print("DPI Aware has been set")
except Exception:
    pass


def resource_path(rel_path: str) -> str:
    # Support PyInstaller onefile extraction via sys._MEIPASS
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, rel_path)

def load_res():
    call_path = resource_path(os.path.join('img', 'call.png'))
    video_path = resource_path(os.path.join('img', 'video.png'))
    call_pic = cv2.imread(call_path)
    video_pic = cv2.imread(video_path)
    if call_pic is None or video_pic is None:
        raise FileNotFoundError(f"img not found: {call_path}, {video_path}")
    return call_pic, video_pic

def find_on_monitor(img_bgr, template_bgr, threshold=THRESHOLD):
    img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    tpl_gray = cv2.cvtColor(template_bgr, cv2.COLOR_BGR2GRAY)

    # simple match
    res = cv2.matchTemplate(img_gray, tpl_gray, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)
    return max_val, max_loc
    
def click_at(x, y):
    ctypes.windll.user32.SetCursorPos(int(x), int(y))
    ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0)
    time.sleep(0.1)
    ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0)

def main_loop():
    call_pic, video_pic = load_res()
    with mss.mss() as sct:
        mon = sct.monitors[1]
        # Main loop
        while True:
            sct_img = sct.grab(mon)
            # mss return BGRA image
            img = np.array(sct_img)[:, :, :3]

            max_call_conf, max_call_loc = find_on_monitor(img, call_pic)
            max_video_conf, max_video_loc = find_on_monitor(img, video_pic)
            print("match call pic confidence: ", max_call_conf)
            print("match video pic confidence: ", max_video_conf)
            if max_call_conf > THRESHOLD:
                global_x = mon['left'] + max_call_loc[0] + call_pic.shape[1] // 2
                global_y = mon['top'] + max_call_loc[1] + call_pic.shape[0] // 2
                print(f"Clicking at global coords: {global_x}, {global_y}")
                click_at(global_x, global_y)
                time.sleep(3)
            if max_video_conf > THRESHOLD:
                global_x = mon['left'] + max_video_loc[0] + video_pic.shape[1] // 2
                global_y = mon['top'] + max_video_loc[1] + video_pic.shape[0] // 2
                print(f"Clicking at global coords: {global_x}, {global_y}")
                click_at(global_x, global_y)
                time.sleep(0.5)
            time.sleep(0.5)


if __name__ == "__main__":
    print("Hello")
    main_loop()