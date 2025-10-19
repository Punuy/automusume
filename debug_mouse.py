import pyautogui
import time

def debug_mouse_pointing():
    print("Move your mouse to the desired position. Press Ctrl+C to exit.")
    try:
        while True:
            x, y = pyautogui.position()
            print(f"Current mouse position: ({x}, {y})", end='\r')
            time.sleep(0.05)
    except KeyboardInterrupt:
        print(f"\nClicked at: ({x}, {y})")
        pyautogui.click(x, y)
        print("Mouse clicked for debug.")

if __name__ == "__main__":
    debug_mouse_pointing()
