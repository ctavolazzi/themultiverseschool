import os
import time
import random
import shutil
import math
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

def rgb_to_ansi(r, g, b):
    """Convert RGB values to ANSI color code"""
    return f"\033[38;2;{r};{g};{b}m"

def create_particle(columns, rows):
    """Create a sparkle particle"""
    return {
        'x': random.randint(0, columns - 1),
        'y': random.randint(0, rows - 1),
        'life': random.uniform(0.3, 1.5),
        'char': random.choice('.*·+✧✦⋆'),  # Simplified particle characters
        'velocity_x': random.uniform(-0.8, 0.8),
        'velocity_y': random.uniform(-0.8, 0.8)
    }

def draw_glowing_text(screen, row, col, text, time_offset):
    """Draw text with rainbow glow effect"""
    if 0 <= row < len(screen):
        # Glow positions (simple cross pattern)
        glow_positions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        for i, char in enumerate(text):
            if 0 <= col + i < len(screen[0]):
                # Calculate rainbow color
                hue = (time_offset + i * 20) % 360
                r = int((math.sin(math.radians(hue)) + 1) * 127.5)
                g = int((math.sin(math.radians(hue + 120)) + 1) * 127.5)
                b = int((math.sin(math.radians(hue + 240)) + 1) * 127.5)
                
                # Draw glow
                for dy, dx in glow_positions:
                    glow_row, glow_col = row + dy, col + i + dx
                    if (0 <= glow_row < len(screen) and 
                        0 <= glow_col < len(screen[0]) and 
                        screen[glow_row][glow_col] == ' '):
                        glow_color = rgb_to_ansi(r//2, g//2, b//2)
                        screen[glow_row][glow_col] = glow_color + '·'
                
                # Draw main character
                screen[row][col + i] = rgb_to_ansi(r, g, b) + char

def play(duration=5):
    try:
        columns, rows = shutil.get_terminal_size()
    except:
        columns, rows = 80, 24  # Default fallback

    # Make animation two rows shorter than terminal height
    rows = max(3, rows - 2)
    
    # Matrix characters
    chars = "ｱｲｳｴｵｶｷｸｹｺｻｼｽｾｿﾀﾁﾂﾃﾄﾅﾆﾇﾈﾉﾊﾋﾌﾍﾎﾏﾐﾑﾒﾓﾔﾕﾖﾗﾘﾙﾚﾛﾜﾝ1234567890"
    
    # Initialize effects
    num_drops = max(1, columns // 2)
    particles = []
    max_particles = 25
    
    screen = [[' ' for _ in range(columns)] for _ in range(rows)]
    
    # Initialize drops
    drops = [{'pos': random.randint(-rows, 0), 
              'speed': random.randint(1, 2),
              'trail': random.randint(3, 10)} 
             for _ in range(num_drops)]

    # Prepare message
    message = "Welcome to the Multiverse"
    msg_row = rows // 2
    msg_col = (columns - len(message)) // 2

    start_time = time.time()
    while (time.time() - start_time) < duration:
        os.system('cls' if os.name == 'nt' else 'clear')
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
                    if pos == msg_row and msg_col <= i*2 < msg_col + len(message):
                        continue
                    intensity = 1 - (j / drop['trail'])
                    screen[pos][i*2] = (rgb_to_ansi(200, 255, 200) if intensity > 0.7 
                                      else rgb_to_ansi(0, 150, 0)) + random.choice(chars)

        # Update and draw particles
        while len(particles) < max_particles:
            particles.append(create_particle(columns, rows))
        
        particles = [p for p in particles if p['life'] > 0]
        for p in particles:
            x, y = int(p['x']), int(p['y'])
            if 0 <= x < columns and 0 <= y < rows:
                brightness = int(255 * p['life'])
                screen[y][x] = rgb_to_ansi(brightness, brightness, brightness) + p['char']
            p['life'] -= random.uniform(0.02, 0.05)
            p['x'] += p['velocity_x']
            p['y'] += p['velocity_y']

        # Draw glowing rainbow message
        if 0 <= msg_row < rows:
            time_offset = time.time() * 50
            draw_glowing_text(screen, msg_row, msg_col, message, time_offset)

        # Draw the screen
        for row in screen:
            print(''.join(char if char != ' ' else ' ' for char in row))

        time.sleep(0.05)

if __name__ == "__main__":
    try:
        play(duration=10)
    except KeyboardInterrupt:
        print("\nAnimation stopped by user")
    finally:
        print(Style.RESET_ALL)
