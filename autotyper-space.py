import pyautogui
import pyperclip
import time

def type_clipboard_content():
    # Safety delay to give you time to focus the correct window
    print("You have 5 seconds to focus the window where you want to type...")
    time.sleep(5)
    
    # Get clipboard content
    text = pyperclip.paste()
    
    # Disable pyautogui's fail-safe (optional, but recommended to keep it on)
    pyautogui.FAILSAFE = True
    
    # Set typing interval (adjust if needed)
    pyautogui.PAUSE = 0.01
    
    # Type out the text character by character to maintain formatting
    for char in text:
        if char == '\n':
            pyautogui.press('enter')
        elif char == '\t':
            pyautogui.press('tab')
        elif char == ' ':
            pyautogui.press('space')
        else:
            pyautogui.write(char)

if __name__ == "__main__":
    # Instructions
    print("Make sure you have the text copied to your clipboard.")
    print("WARNING: Keep your mouse in the top-left corner of the screen to abort typing.")
    input("Press Enter to start typing (or Ctrl+C to cancel)...")
    
    try:
        type_clipboard_content()
        print("\nTyping completed successfully!")
    except Exception as e:
        print(f"\nAn error occurred: {e}")