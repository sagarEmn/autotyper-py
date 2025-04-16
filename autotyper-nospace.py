import pyautogui
import time
import re
import pyperclip  # For clipboard access

import platform
if platform.system() == 'Windows':
    import winsound
else:
    import os

def remove_indentation(code):
    """
    Removes all indentation from the code while preserving empty lines.
    Returns the processed code as a list of lines.
    """
    lines = code.split('\n')
    processed_lines = []
    for line in lines:
        if not line.strip():
            processed_lines.append('')
        else:
            processed_lines.append(line.lstrip())
    return processed_lines

def type_code(code, delay_between_lines=0.5, initial_delay=3, char_delay=0.1):
    # Play start sound
    play_sound('start')
    
    # Remove indentation
    lines = remove_indentation(code)
    
    # Initial delay countdown
    for i in range(initial_delay, 0, -1):
        print(f"Starting in {i} seconds... Focus on your target window!")
        time.sleep(1)
    print("Starting to type...")
    
    # Type each line
    total_lines = len(lines)
    for idx, line in enumerate(lines, 1):
        if line:  # Only type non-empty lines
            # Type each character with a small delay
            for char in line:
                pyautogui.write(char)
                time.sleep(char_delay)
        
        # Press enter and wait
        pyautogui.press('enter')
        time.sleep(delay_between_lines)
        
        # Progress update
        print(f"Typed line {idx}/{total_lines}: {line[:50]}{'...' if len(line) > 50 else ''}")

    print("Finished typing!")
    # Play completion sound
    play_sound('complete')
    
def play_sound(sound_type):
    """Play a sound notification. sound_type can be 'start' or 'complete'."""
    if platform.system() == 'Windows':
        # On Windows, use winsound
        frequency = 800 if sound_type == 'start' else 1000
        duration = 500  # milliseconds
        winsound.Beep(frequency, duration)
    else:
        # On Unix-like systems, use terminal bell
        os.system('tput bel')

if __name__ == "__main__":
    # Get text from clipboard
    clipboard_content = pyperclip.paste()
    
    if not clipboard_content.strip():
        print("Error: Clipboard is empty! Please copy some text first.")
        exit(1)
    
    # Preview the content
    print("\nContent to be typed (first 150 characters):")
    preview = clipboard_content[:150] + "..." if len(clipboard_content) > 150 else clipboard_content
    print(preview)
    print(f"\nTotal lines to type: {len(clipboard_content.splitlines())}")
    
    # Ask for confirmation
    response = input("\nDo you want to proceed with typing this content? (y/n): ")
    if response.lower() != 'y':
        print("Operation cancelled by user.")
        exit(0)
    
    # Safety feature: move mouse to top-left corner to abort
    print("\nMove your mouse to the top-left corner of the screen to abort.")
    
    # Configure PyAutoGUI
    pyautogui.FAILSAFE = True  # Move mouse to top-left to abort
    pyautogui.PAUSE = 0.1      # Add a small pause between all PyAutoGUI commands
    
    try:
        # You can adjust these timing values as needed
        type_code(
            clipboard_content,
            delay_between_lines=0.005,  # Increased delay between lines
            initial_delay=5,          # Increased initial delay
            char_delay=0.001          # Added delay between characters
        )
    except pyautogui.FailSafeException:
        print("\nTyping aborted by moving mouse to corner")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
       