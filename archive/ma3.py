import os
import time
import random
import shutil
import math
import sys
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
    """Draw text with spiral arms emanating from the center of the text"""
    if 0 <= row < len(screen):
        # Calculate the true center of the text
        text_center_x = col + len(text) // 2
        text_center_y = row

        spiral_time = time.time() * 0.15
        arm_length = 90  # Longer arms for more dramatic effect
        num_arms = 4
        spiral_tightness = 4.8

        # Define text bounding box with buffer
        buffer_rows = 1  # Number of rows above and below the text to protect
        buffer_cols = 2  # Number of columns to the left and right of the text to protect

        text_start_row = max(0, row - buffer_rows)
        text_end_row = min(len(screen), row + buffer_rows + 1)
        text_start_col = max(0, col - buffer_cols)
        text_end_col = min(len(screen[0]), col + len(text) + buffer_cols)

        # First draw the spiral arms from the center
        for arm in range(num_arms):
            base_angle = (2 * math.pi * arm / num_arms) + spiral_time

            # Generate spiral points
            for t in range(arm_length):
                t_normalized = t / arm_length
                # Exponential radius growth for more dramatic spiral
                radius = 0.1 + (math.pow(t_normalized, 0.5) * 12.0)
                curve_factor = math.pow(t_normalized, 0.35)
                point_angle = base_angle + ((1 - curve_factor) * spiral_tightness * 2 * math.pi)

                # Calculate position relative to text center
                dx = int(radius * math.cos(point_angle) * 1.6)
                dy = int(radius * math.sin(point_angle) * 0.8)

                glow_row = text_center_y + dy
                glow_col = text_center_x + dx

                if (0 <= glow_row < len(screen)) and (0 <= glow_col < len(screen[0])):

                    # Don't draw over the text bounding box
                    if (text_start_row <= glow_row < text_end_row) and (text_start_col <= glow_col < text_end_col):
                        continue

                    # Enhanced character and intensity progression
                    point_progress = t / arm_length
                    if point_progress < 0.2:
                        glow_char = '✧'
                        intensity = 1.0
                    elif point_progress < 0.4:
                        glow_char = '✦'
                        intensity = 0.9
                    elif point_progress < 0.7:
                        glow_char = '·'
                        intensity = 0.7
                    else:
                        glow_char = '.'
                        intensity = 0.3 + (1 - point_progress) * 0.4

                    # Calculate color based on angle for rainbow effect
                    hue = (time_offset + (point_angle * 180 / math.pi)) % 360
                    r = int((math.sin(math.radians(hue)) + 2.2) * 127.5)
                    g = int((math.sin(math.radians(hue + 120)) + 2.2) * 127.5)
                    b = int((math.sin(math.radians(hue + 240)) + 2.2) * 127.5)

                    # Smooth pulse effect based on distance from center
                    dist_factor = 1 - (t_normalized * 0.5)
                    pulse = 1 + math.sin(spiral_time * 3 + point_progress * 8) * 0.15 * dist_factor

                    # Apply color with distance-based fade
                    arm_color = rgb_to_ansi(
                        min(255, int(r * intensity * pulse * 0.9)),
                        min(255, int(g * intensity * pulse * 0.9)),
                        min(255, int(b * intensity * pulse * 0.9))
                    )

                    screen[glow_row][glow_col] = arm_color + glow_char

        # Draw the text last, making it brightest
        for i, char in enumerate(text):
            if 0 <= col + i < len(screen[0]):
                # Calculate text color based on position and time for rainbow effect
                hue = (time_offset + i * 15) % 360  # Stagger hues for cascading effect
                r = int((math.sin(math.radians(hue)) + 3.0) * 127.5)
                g = int((math.sin(math.radians(hue + 120)) + 3.0) * 127.5)
                b = int((math.sin(math.radians(hue + 240)) + 3.0) * 127.5)

                # More dramatic pulsing effect
                text_pulse = 1.6 + math.sin(time_offset * 0.08 + i * 0.4) * 0.2
                main_color = rgb_to_ansi(
                    min(255, int(r * text_pulse)),
                    min(255, int(g * text_pulse)),
                    min(255, int(b * text_pulse))
                )
                # Add bold style to make text more pronounced
                screen[row][col + i] = "\033[1m" + main_color + char + "\033[22m"

def play(duration=None):
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

    # Prepare message
    message = "Welcome to the Multiverse"
    msg_row = rows // 2
    msg_col = (columns - len(message)) // 2

    # Calculate text bounding box with buffer
    buffer_rows = 1  # Number of rows above and below the text to protect
    buffer_cols = 2  # Number of columns to the left and right of the text to protect

    text_start_row = max(0, msg_row - buffer_rows)
    text_end_row = min(rows, msg_row + buffer_rows + 1)
    text_start_col = max(0, msg_col - buffer_cols)
    text_end_col = min(columns, msg_col + len(message) + buffer_cols)
    text_row = msg_row

    # Initialize drops
    drops = [{'pos': random.randint(-rows, 0), 
              'speed': random.randint(1, 2),
              'trail': random.randint(3, 10)} 
             for _ in range(num_drops)]

    start_time = time.time()
    try:
        while True:
            # Break if duration is specified and exceeded
            if duration is not None and (time.time() - start_time) >= duration:
                break

            # Clear the screen buffer
            screen = [[' ' for _ in range(columns)] for _ in range(rows)]

            # Update and draw matrix rain
            for i, drop in enumerate(drops):
                drop_x = i * 2
                if drop_x >= columns:
                    continue

                drop['pos'] += drop['speed']
                if drop['pos'] - drop['trail'] >= rows:
                    drop['pos'] = random.randint(-5, 0)
                    drop['trail'] = random.randint(3, 10)
                    drop['speed'] = random.randint(1, 2)

                for j in range(drop['trail']):
                    pos = drop['pos'] - j
                    if 0 <= pos < rows:
                        # Skip drawing over the text bounding box
                        if text_start_row <= pos < text_end_row and text_start_col <= drop_x < text_end_col:
                            continue
                        intensity = 1 - (j / drop['trail'])
                        screen[pos][drop_x] = (rgb_to_ansi(200, 255, 200) if intensity > 0.7 
                                              else rgb_to_ansi(0, 150, 0)) + random.choice(chars)

            # Update and draw particles
            while len(particles) < max_particles:
                particles.append(create_particle(columns, rows))

            particles = [p for p in particles if p['life'] > 0]
            for p in particles:
                x, y = int(p['x']), int(p['y'])
                if 0 <= x < columns and 0 <= y < rows:
                    # Skip drawing over the text bounding box
                    if text_start_row <= y < text_end_row and text_start_col <= x < text_end_col:
                        continue
                    brightness = int(255 * p['life'])
                    screen[y][x] = rgb_to_ansi(brightness, brightness, brightness) + p['char']
                p['life'] -= random.uniform(0.02, 0.05)
                p['x'] += p['velocity_x']
                p['y'] += p['velocity_y']

            # Draw glowing rainbow message into the buffer
            time_offset = time.time() * 50
            draw_glowing_text(screen, msg_row, msg_col, message, time_offset)

            # Clear the terminal screen
            os.system('cls' if os.name == 'nt' else 'clear')

            # Print the background
            for row in screen:
                print(''.join(char if char != ' ' else ' ' for char in row))

            # Overlay the rainbow text on top using cursor positioning
            # Move the cursor to the text row and column
            # Note: ANSI escape sequences start counting from 1
            # Generate rainbow text with per-character coloring
            rainbow_text = ""
            for i, char in enumerate(message):
                hue = (time_offset + i * 15) % 360  # Stagger hues for cascading effect
                r = int((math.sin(math.radians(hue)) + 3.0) * 127.5)
                g = int((math.sin(math.radians(hue + 120)) + 3.0) * 127.5)
                b = int((math.sin(math.radians(hue + 240)) + 3.0) * 127.5)
                pulse = 1.6 + math.sin(time_offset * 0.08 + i * 0.4) * 0.2
                color = rgb_to_ansi(
                    min(255, int(r * pulse)),
                    min(255, int(g * pulse)),
                    min(255, int(b * pulse))
                )
                rainbow_text += f"{color}\033[1m{char}\033[22m"

            # Position the cursor and print the rainbow text
            print(f"\033[{msg_row + 1};{msg_col + 1}H{rainbow_text}{Style.RESET_ALL}", end='')

            # Flush the output to ensure it appears immediately
            sys.stdout.flush()

            time.sleep(0.05)
    except KeyboardInterrupt:
        print("\nAnimation stopped by user")
    finally:
        print(Style.RESET_ALL)

if __name__ == "__main__":
    play()
