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

def type_code(code, delay_between_lines=0.005, initial_delay=3, char_delay=0.001):
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
            # --- Option 1: Keep character loop (faster) ---
            for char in line:
                 pyautogui.write(char, interval=0) # Use internal interval if needed, 0 for max speed
                 # No extra time.sleep(char_delay) needed if PAUSE and write interval handle it
            # --- Option 2: Use typewrite (might be slightly cleaner/faster sometimes) ---
            # pyautogui.typewrite(line, interval=char_delay) # interval here is per-character delay

        # Press enter and wait
        pyautogui.press('enter')
        # You might even remove this sleep if pyautogui.PAUSE is very small
        # and the target application is responsive enough
        if delay_between_lines > 0:
             time.sleep(delay_between_lines)

        # Progress update (optional, printing takes time too)
        # Consider printing less often for max speed
        if idx % 10 == 0 or idx == total_lines: # Print every 10 lines or on the last line
            print(f"Typed line {idx}/{total_lines}")
            # print(f"Typed line {idx}/{total_lines}: {line[:50]}{'...' if len(line) > 50 else ''}") # Original print

    print("Finished typing!")
    # Play completion sound
    play_sound('complete')

def play_sound(sound_type):
    """Play a sound notification. sound_type can be 'start' or 'complete'."""
    try:
        if platform.system() == 'Windows':
            frequency = 800 if sound_type == 'start' else 1000
            duration = 300  # milliseconds (shortened duration slightly)
            winsound.Beep(frequency, duration)
        else:
            # On Unix-like systems, use terminal bell (quickest)
             print('\a', end='', flush=True) # '\a' is the bell character
            # os.system('tput bel') # This might be slightly slower
    except Exception as e:
        print(f"Warning: Could not play sound - {e}")


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

    # --- KEY CHANGE FOR SPEED ---
    # Reduce the global pause significantly. Start low (e.g., 0.01) and decrease further if needed.
    # Setting it to 0 makes it rely purely on the other delays/system speed.
    pyautogui.PAUSE = 0.01  # Drastically reduced from 0.1. Try 0.005 or even 0 if needed.

    try:
        # Adjust these timing values for faster speed
        type_code(
            clipboard_content,
            # --- KEY CHANGES FOR SPEED ---
            delay_between_lines=0,  # Make this very small or 0
            initial_delay=5,          # Keep initial delay reasonable
            char_delay=0              # Make this very small or 0 (if using Option 1 loop, this is less relevant now)
        )
    except pyautogui.FailSafeException:
        print("\nTyping aborted by moving mouse to corner")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        # Reset PAUSE on error just in case
        pyautogui.PAUSE = 0.1
    finally:
         # Optional: Reset PAUSE back to default if desired after script finishes
         pyautogui.PAUSE = 0.1
         print("Typing finished or aborted. PyAutoGUI PAUSE reset.")