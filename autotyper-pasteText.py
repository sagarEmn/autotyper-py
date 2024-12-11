import pyautogui
import time
import re

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

def type_code(code, delay_between_lines=0.5, initial_delay=3, char_delay=0.01):
    """
    Types out the code with specified delays.
    
    Args:
        code (str): The code to type
        delay_between_lines (float): Delay in seconds between each line
        initial_delay (int): Initial delay in seconds before starting to type
        char_delay (float): Delay between each character
    """
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

# Example usage
sample_code = """#include <stdio.h>

int main() {
char recipient[] = "John";
char sender[] = "Jane";
float version = 1.2;
float discount = 10.5;
char status = 'A';
char code[] = "ABCD123";
char location[] = "City XYZ";
int age = 30;
char company[] = "ABC Corporation";
char website[] = "www.example.com";
char phone[] = "+1 123-456-7890";
char jobTitle[] = "Software Engineer";
char department[] = "Engineering";
char subject[] = "Greetings";

    printf("Dear %s, I hope this email finds you well.\n", recipient);
    printf("I wanted to reach out and say hello.\n");
    printf("I hope you are doing well and enjoying your day.\n");
    printf("It's been a while since we last spoke, and I wanted to catch up with you.\n");
    printf("Let's plan to meet up soon and have a great time together!\n\n");
    printf("Subject: %s\n", subject);
    printf("Sender: %s\n", sender);
    printf("Version: %.1f\n", version);
    printf("Discount: %.2f%%\n", discount);
    printf("Status: %c\n", status);
    printf("Code: %s\n", code);
    printf("Location: %s\n", location);
    printf("Age: %d\n", age);
    printf("Company: %s\n", company);
    printf("Website: %s\n", website);
    printf("Phone: %s\n", phone);
    printf("Job Title: %s\n", jobTitle);
    printf("Department: %s\n", department);

    return 0;
}
"""

if __name__ == "__main__":
    # Safety feature: move mouse to top-left corner to abort
    print("Move your mouse to the top-left corner of the screen to abort.")
    
    # Configure PyAutoGUI
    pyautogui.FAILSAFE = True  # Move mouse to top-left to abort
    pyautogui.PAUSE = 0.1      # Add a small pause between all PyAutoGUI commands
    
    try:
        # You can adjust these timing values as needed
        type_code(
            sample_code,
            delay_between_lines=0.5,  # Increased delay between lines
            initial_delay=5,          # Increased initial delay
            char_delay=0.01          # Added delay between characters
        )
    except pyautogui.FailSafeException:
        print("\nTyping aborted by moving mouse to corner")
    except Exception as e:
        print(f"\nAn error occurred: {e}")