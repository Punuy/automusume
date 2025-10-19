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
        ("back", "assest/buttons/back.png", (0, 255, 0)),
        ("confirm", "assest/buttons/confirm.png", (0, 255, 0)),
        ("cancel", "assest/buttons/cancel.png", (0, 255, 0)),
        ("next", "assest/buttons/next.png", (0, 255, 0)),
        ("reset", "assest/buttons/reset.png", (0, 255, 0)),
        ("plus", "assest/ingame/plus.png", (0, 255, 0)),
        ("race", "assest/buttons/race.png", (0, 255, 0)),
        ("start_career", "assest/buttons/start_career.png", (0, 255, 0)),

        ("rest", "assest/ingame/rest.png", (0, 0, 255)),
        ("training", "assest/ingame/training.png", (0, 0, 255)),
        ("skills", "assest/ingame/skills.png", (0, 0, 255)),
        ("infirmary", "assest/ingame/infirmary.png", (0, 0, 255)),
        ("recreation", "assest/ingame/recreation.png", (0, 0, 255)),
        ("races", "assest/ingame/races.png", (255, 0, 0)),

        ("speed", "assest/ingame/speed-1.png", (0, 0, 255)),
        ("stamina", "assest/ingame/stamina-1.png", (0, 0, 255)),
        ("power", "assest/ingame/power-1.png", (0, 0, 255)),
        ("guts", "assest/ingame/guts-1.png", (0, 0, 255)),
        ("wisdom", "assest/ingame/wit-1.png", (0, 0, 255)),

        ("career", "assest/ingame/career.png", (0, 0, 255)),
        ("normal", "assest/ingame/normal.png", (0, 0, 255)),
        ("good", "assest/ingame/good.png", (0, 0, 255)),
        ("great", "assest/ingame/great.png", (255, 0, 0)),

        ("skills", "assest/ingame/skills.png", (0, 0, 255)),
        ("race", "assest/ingame/race.png", (255, 0, 0)),

        ("change", "assest/ingame/change.png", (0, 255, 0)),
        ("end", "assest/ingame/end.png", (0, 255, 0)),
        ("late", "assest/ingame/late.png", (0, 255, 0)),
        ("pace", "assest/ingame/pace.png", (0, 255, 0)),
        ("front", "assest/ingame/front.png", (0, 255, 0)),
        ("view_results", "assest/ingame/view_results.png", (0, 255, 0))

    ]
    found_any = False
    for name, path, color in menu_templates:
        result = match_template_on_screen(screenshot_bgr, path, threshold=0.75)
        if result:
            (x, y, w, h) = result
            print(f"Debug: Drawing box for {name} at ({x},{y},{w},{h})")
            cv2.rectangle(debug_img, (x, y), (x + w, y + h), color, 3)
            found_any = True
    if found_any:
        cv2.imwrite('debug_career_detect.png', debug_img)
        print("At least one menu detected.")
    else:
        print("No menu detected.")
        cv2.imwrite('debug_career_detect.png', debug_img)
    return

if __name__ == "__main__":
    main()
