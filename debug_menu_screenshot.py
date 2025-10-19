import pyautogui
import cv2
import numpy as np
import time

def match_template_on_screen(screen_img, template_path, threshold=0.7):
    template = cv2.imread(template_path, cv2.IMREAD_COLOR)
    if template is None:
        print(f"Template not found: {template_path}")
        return None
    res = cv2.matchTemplate(screen_img, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    if max_val >= threshold:
        print(f"Matched {template_path} with confidence {max_val:.2f}")
        return (max_loc[0], max_loc[1], template.shape[1], template.shape[0])  # (x, y, w, h)
    return None

def main():
    # Take screenshot
    screenshot = pyautogui.screenshot()
    screenshot_np = np.array(screenshot)
    screenshot_bgr = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
    debug_img = screenshot_bgr.copy()

    # Detect all menu items at once
    menu_templates = [
        ("career", "assest/menu/careea.png", (0, 255, 0)),
        ("career-1", "assest/menu/careea-1.png", (0, 255, 0)),
        ("home", "assest/menu/home-1.png", (255, 0, 0)),
    ]
    found_any = False
    for name, path, color in menu_templates:
        result = match_template_on_screen(screenshot_bgr, path, threshold=0.6)
        if result:
            (x, y, w, h) = result
            print(f"Debug: Drawing box for {name} at ({x},{y},{w},{h})")
            cv2.rectangle(debug_img, (x, y), (x + w, y + h), color, 3)
            found_any = True
    if found_any:
        cv2.imwrite('debug_menu_detect.png', debug_img)
        print("At least one menu detected.")
    else:
        print("No menu detected.")
        cv2.imwrite('debug_menu_detect.png', debug_img)
    return

if __name__ == "__main__":
    main()
