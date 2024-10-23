import os
import time
import random
import shutil
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

def play(duration=5):
    """
    Display a Matrix-style animation in the terminal with falling characters
    Args:
        duration (int): How long to run the animation in seconds
    """
    try:
        columns, rows = shutil.get_terminal_size()
    except:
        columns, rows = 80, 24  # Default fallback

    # Make animation two rows shorter than terminal height
    rows = max(3, rows - 2)  # Ensure at least 3 rows minimum
    
    # Matrix characters - using more authentic katakana and Matrix-style symbols
    chars = "ｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄﾅﾆﾇﾈﾉﾊﾋﾌﾍﾎﾏﾐﾑﾒﾓﾔﾕﾖﾗﾘﾙﾚﾛﾜﾝ1234567890"
    
    # Initialize the screen matrix with proper size check
    # Ensure we don't exceed terminal width when spacing columns
    num_drops = max(1, columns // 2)  # At least 1 drop, but no more than half the columns
    
    screen = [[' ' for _ in range(columns)] for _ in range(rows)]
    
    # Track the position and trail length of each drop
    drops = [{'pos': random.randint(-rows, 0), 
              'speed': random.randint(1, 2),
              'trail': random.randint(3, 10)} 
             for _ in range(num_drops)]

    # Prepare the welcome message
    message = "Welcome to the Multiverse"
    msg_row = rows // 2
    msg_col = (columns - len(message)) // 2

    start_time = time.time()
    while (time.time() - start_time) < duration:
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # Reset screen buffer each frame
        screen = [[' ' for _ in range(columns)] for _ in range(rows)]
        
        # Update and draw matrix rain
        for i, drop in enumerate(drops):
            if i*2 >= columns: continue
            
            drop['pos'] += drop['speed']
            if drop['pos'] - drop['trail'] >= rows:
                drop['pos'] = random.randint(-5, 0)
                drop['trail'] = random.randint(3, 10)
                drop['speed'] = random.randint(1, 2)
            
            for j in range(drop['trail']):
                pos = drop['pos'] - j
                if 0 <= pos < rows:
                    # Skip drawing matrix characters where the message will be
                    if pos == msg_row and msg_col <= i*2 < msg_col + len(message):
                        continue
                    intensity = 1 - (j / drop['trail'])
                    screen[pos][i*2] = (Fore.WHITE + Style.BRIGHT if intensity > 0.7 
                                      else Fore.GREEN) + random.choice(chars)

        # Draw the message
        if 0 <= msg_row < rows:
            for i, char in enumerate(message):
                if 0 <= msg_col + i < columns:
                    screen[msg_row][msg_col + i] = Style.BRIGHT + Fore.WHITE + char

        # Draw the screen
        for row in screen:
            print(''.join(char if char != ' ' else ' ' for char in row))

        time.sleep(0.05)

if __name__ == "__main__":
    play(duration=10)  # Run for 10 seconds by default when run directly
