import pyautogui
import cv2
import numpy as np
from PIL import Image
import time

# Utility: match template on screen, return top-left position if found, else None
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

# Utility: click at a position (center of template)
def click_template(screen_img, template_path, threshold=0.7):
    pos = match_template_on_screen(screen_img, template_path, threshold)
    if pos is not None:
        template = cv2.imread(template_path, cv2.IMREAD_COLOR)
        h, w = template.shape[:2]
        center_x = pos[0] + w // 2
        center_y = pos[1] + h // 2
        pyautogui.moveTo(center_x, center_y, duration=0.2)
        pyautogui.click()
        print(f"Clicked {template_path} at ({center_x}, {center_y})")
        return True
    return False
# Step 1: Detect the game screen (not just window)
def find_game_screen():
    # Take a screenshot of the primary screen
    screenshot = pyautogui.screenshot()
    screenshot.save('screenshot_debug.png')  # Save for debug
    screenshot_np = np.array(screenshot)
    screenshot_bgr = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
    # You can use a unique image from the game to match here
    # For now, just return the screenshot for further processing
    return screenshot_bgr

def main():
    print("Searching for Umamusume game screen...")
    screen = find_game_screen()
    # Detect and click logic with loop: if career detected, click; else click home and retry
    menu_templates = [
        ("career", "assest/menu/careea.png"),
        ("home", "assest/menu/home-1.png"),
    ]
    max_attempts = 5
    for attempt in range(max_attempts):
        screen = find_game_screen()
        result = match_template_on_screen(screen, menu_templates[0][1], threshold=0.7)  # career
        if result:
            (x, y, w, h) = result
            print(f"Career detected at ({x},{y},{w},{h}), clicking career...")
            center_x = x + w // 2
            center_y = y + h // 2
            pyautogui.moveTo(center_x, center_y, duration=0.2)
            pyautogui.click()
            time.sleep(1)
            # After clicking career, click next and ensure screen changes (retry up to 5 times if not)
            next_path = "assest/buttons/next.png"
            confirm_path = "assest/buttons/confirm.png"
            for attempt in range(5):
                screen = find_game_screen()
                result = match_template_on_screen(screen, next_path, threshold=0.7)
                if result:
                    (x, y, w, h) = result
                    print(f"Next detected at ({x},{y},{w},{h}), clicking next...")
                    center_x = x + w // 2
                    center_y = y + h // 2
                    pyautogui.moveTo(center_x, center_y, duration=0.2)
                    pyautogui.click()
                    time.sleep(1)
                    # After clicking next, if still detected, click again (up to 5 times)
                    for retry in range(5):
                        screen_retry = find_game_screen()
                        result_retry = match_template_on_screen(screen_retry, next_path, threshold=0.7)
                        if not result_retry:
                            print("Next button gone, proceeding to confirm.")
                            break
                        else:
                            print(f"Next still detected after click, retrying ({retry+1}/5)...")
                            pyautogui.moveTo(center_x, center_y, duration=0.2)
                            pyautogui.click()
                            time.sleep(1)
                    else:
                        print("Next button still present after 5 retries.")
                    break
                else:
                    print("Next not detected, retrying...")
                    time.sleep(0.5)
            else:
                print("Max attempts reached. Next not detected.")

            # Now look for confirm only after next is gone
            for attempt in range(5):
                screen = find_game_screen()
                result = match_template_on_screen(screen, confirm_path, threshold=0.7)
                if result:
                    (x, y, w, h) = result
                    print(f"Confirm detected at ({x},{y},{w},{h}), clicking confirm...")
                    center_x = x + w // 2
                    center_y = y + h // 2
                    pyautogui.moveTo(center_x, center_y, duration=0.2)
                    pyautogui.click()
                    time.sleep(1)
                    break
                else:
                    print("Confirm not detected, retrying...")
                    time.sleep(0.5)
            else:
                print("Max attempts reached. Confirm not detected.")
            # Check if next is still present after click, retry up to 5 times
            for retry in range(5):
                screen_retry = find_game_screen()
                result_retry = match_template_on_screen(screen_retry, next_path, threshold=0.7)
                if not result_retry:
                    print("Next button gone, proceeding.")
                    break
                else:
                    print(f"Next still detected after click, retrying ({retry+1}/5)...")
                    pyautogui.moveTo(center_x, center_y, duration=0.2)
                    pyautogui.click()
                    time.sleep(1)
            else:
                print("Next button still present after 5 retries.")
            break
        else:
            print("Career not detected. Checking for home...")
            result = match_template_on_screen(screen, menu_templates[1][1], threshold=0.7)  # home
            if result:
                (x, y, w, h) = result
                print(f"Home detected at ({x},{y},{w},{h}), clicking home...")
                center_x = x + w // 2
                center_y = y + h // 2
                pyautogui.moveTo(center_x, center_y, duration=0.2)
                pyautogui.click()
                time.sleep(1)
            else:
                print("Neither career nor home detected. Stopping.")
                break
    else:
        print("Max attempts reached. Career not detected.")

if __name__ == "__main__":
    main()
