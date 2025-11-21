import os
import sys
import tty
import termios
import shutil
import time

def test_terminal_size():
    print("Normal mode:")
    try:
        sz = os.get_terminal_size()
        print(f"os.get_terminal_size(): {sz}")
    except OSError as e:
        print(f"os.get_terminal_size() failed: {e}")
    
    print(f"shutil.get_terminal_size(): {shutil.get_terminal_size()}")

    print("\nSwitching to raw mode in 2 seconds...")
    time.sleep(2)

    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        
        # We can't easily print in raw mode without \r\n, so we'll write to a file or just format carefully
        # But for this test, let's just try to get the size and print it with \r\n
        
        msg = "\r\nRaw mode:\r\n"
        sys.stdout.write(msg)
        
        try:
            sz = os.get_terminal_size()
            sys.stdout.write(f"os.get_terminal_size(): {sz}\r\n")
        except OSError as e:
            sys.stdout.write(f"os.get_terminal_size() failed: {e}\r\n")
            
        sys.stdout.write(f"shutil.get_terminal_size(): {shutil.get_terminal_size()}\r\n")
        
        sys.stdout.write("Exiting raw mode...\r\n")
        
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

if __name__ == "__main__":
    test_terminal_size()
