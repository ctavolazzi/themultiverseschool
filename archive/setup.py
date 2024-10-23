import os
import sys
import time
import random
import shutil
import math
import json
import hashlib
import subprocess
from getpass import getpass
from colorama import Fore, Style, init
import webbrowser
import threading

# Initialize colorama
init(autoreset=True)

def install_requirements():
    """Install required packages from requirements.txt"""
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        return True
    except Exception as e:
        print(f"Error installing requirements: {e}")
        return False

def hash_password(password):
    """Create a SHA-256 hash of the password"""
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    """Load users from users.json or create new file if it doesn't exist"""
    if os.path.exists('users.json'):
        with open('users.json', 'r') as f:
            return json.load(f)
    return {}

def save_users(users):
    """Save users to users.json"""
    with open('users.json', 'w') as f:
        json.dump(users, f, indent=4)

def create_user():
    """Create a new user"""
    users = load_users()
    
    while True:
        username = input(Fore.CYAN + "\nEnter username: " + Style.RESET_ALL).strip()
        if not username:
            print(Fore.RED + "Username cannot be empty" + Style.RESET_ALL)
            continue
        if username in users:
            print(Fore.RED + "Username already exists" + Style.RESET_ALL)
            continue
        break

    while True:
        password = getpass(Fore.CYAN + "Enter password: " + Style.RESET_ALL)
        if not password:
            print(Fore.RED + "Password cannot be empty" + Style.RESET_ALL)
            continue
        confirm_password = getpass(Fore.CYAN + "Confirm password: " + Style.RESET_ALL)
        if password != confirm_password:
            print(Fore.RED + "Passwords don't match" + Style.RESET_ALL)
            continue
        break

    users[username] = {
        'password': hash_password(password),
        'created_at': time.strftime('%Y-%m-%d %H:%M:%S')
    }
    save_users(users)
    return username

def login():
    """Login existing user"""
    users = load_users()
    
    if not users:
        print(Fore.RED + "\nNo users exist. Please create a new user." + Style.RESET_ALL)
        return create_user()

    while True:
        username = input(Fore.CYAN + "\nEnter username: " + Style.RESET_ALL).strip()
        if username not in users:
            print(Fore.RED + "Username not found" + Style.RESET_ALL)
            continue
        
        password = getpass(Fore.CYAN + "Enter password: " + Style.RESET_ALL)
        if users[username]['password'] != hash_password(password):
            print(Fore.RED + "Incorrect password" + Style.RESET_ALL)
            continue
        
        return username

def create_flask_app():
    """Create the Flask application file"""
    flask_code = '''from flask import Flask, render_template, request, redirect, url_for, flash, session
import json
import hashlib
import webbrowser
import threading
import time
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

def open_browser():
    """Start the browser after a short delay"""
    time.sleep(1.5)
    webbrowser.open('http://127.0.0.1:5000/')

def load_users():
    with open('users.json', 'r') as f:
        return json.load(f)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
@login_required
def index():
    users = load_users()
    user_data = users[session['username']]
    return render_template('dashboard.html', 
                         username=session['username'],
                         created_at=user_data['created_at'])

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        users = load_users()
        username = request.form['username']
        password = request.form['password']
        
        if username in users and users[username]['password'] == hash_password(password):
            session['username'] = username
            return redirect(url_for('index'))
        flash('Invalid username or password')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    threading.Thread(target=open_browser).start()
    app.run(debug=True)
'''
    
    # Create templates directory and static/css directory
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)

    # Create CSS file
    css_content = '''
:root {
    --neon-purple: #b026ff;
    --dark-purple: #2a0134;
    --cyber-blue: #0ff;
    --cyber-pink: #ff00ff;
}

body {
    background: linear-gradient(45deg, var(--dark-purple), #000);
    color: #fff;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    margin: 0;
    padding: 0;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

.container {
    background: rgba(0, 0, 0, 0.8);
    border: 2px solid var(--neon-purple);
    border-radius: 10px;
    padding: 2rem;
    box-shadow: 0 0 20px var(--neon-purple);
    max-width: 600px;
    width: 90%;
    margin: 20px;
}

h1 {
    color: var(--cyber-blue);
    text-align: center;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-bottom: 2rem;
    text-shadow: 0 0 10px var(--cyber-blue);
}

.form-group {
    margin-bottom: 1.5rem;
}

input[type="text"],
input[type="password"] {
    width: 100%;
    padding: 10px;
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid var(--neon-purple);
    border-radius: 5px;
    color: #fff;
    font-size: 1rem;
    transition: all 0.3s ease;
}

input[type="text"]:focus,
input[type="password"]:focus {
    outline: none;
    box-shadow: 0 0 10px var(--cyber-pink);
}

button {
    background: var(--neon-purple);
    color: #fff;
    border: none;
    padding: 12px 24px;
    border-radius: 5px;
    cursor: pointer;
    font-size: 1rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    transition: all 0.3s ease;
    width: 100%;
}

button:hover {
    background: var(--cyber-pink);
    box-shadow: 0 0 15px var(--cyber-pink);
}

.error-message {
    color: var(--cyber-pink);
    text-align: center;
    margin-bottom: 1rem;
}

.dashboard-info {
    margin-bottom: 2rem;
    padding: 1rem;
    border: 1px solid var(--cyber-blue);
    border-radius: 5px;
    background: rgba(0, 255, 255, 0.1);
}

.next-steps {
    margin-top: 2rem;
    padding: 1rem;
    border: 1px solid var(--cyber-pink);
    border-radius: 5px;
    background: rgba(255, 0, 255, 0.1);
}

.highlight {
    color: var(--cyber-blue);
    font-weight: bold;
}

.logout-btn {
    margin-top: 2rem;
    background: rgba(255, 0, 0, 0.5);
}

.logout-btn:hover {
    background: red;
}
'''

    # Create login template
    login_template = '''<!DOCTYPE html>
<html>
<head>
    <title>Login - Multiverse Portal</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
    <div class="container">
        <h1>Enter the Multiverse</h1>
        {% with messages = get_flashed_messages() %}
            {% if messages %}
                {% for message in messages %}
                    <div class="error-message">{{ message }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        <form method="POST">
            <div class="form-group">
                <input type="text" name="username" placeholder="Username" required>
            </div>
            <div class="form-group">
                <input type="password" name="password" placeholder="Password" required>
            </div>
            <button type="submit">Access Portal</button>
        </form>
    </div>
</body>
</html>
'''

    # Create dashboard template
    dashboard_template = '''<!DOCTYPE html>
<html>
<head>
    <title>Multiverse Dashboard</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
    <div class="container">
        <h1>Welcome to Your Multiverse</h1>
        
        <div class="dashboard-info">
            <h2>Profile Information</h2>
            <p>Username: <span class="highlight">{{ username }}</span></p>
            <p>Account Created: <span class="highlight">{{ created_at }}</span></p>
        </div>

        <div class="next-steps">
            <h2>Next Steps</h2>
            <p>Congratulations on accessing the Multiverse! Here's what to do next:</p>
            <ol>
                <li>Close this server (Ctrl+C in the terminal)</li>
                <li>Run the next script by typing:<br>
                <span class="highlight">python run-me-second.py</span></li>
                <li>Follow along with the curriculum to build your own multiverse!</li>
            </ol>
        </div>

        <a href="{{ url_for('logout') }}">
            <button class="logout-btn">Logout</button>
        </a>
    </div>
</body>
</html>
'''

    # Write all the files
    with open('run-me-first.py', 'w') as f:
        f.write(flask_code)
    
    with open('templates/login.html', 'w') as f:
        f.write(login_template)
        
    with open('templates/dashboard.html', 'w') as f:
        f.write(dashboard_template)
        
    with open('static/css/style.css', 'w') as f:
        f.write(css_content)

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
    """Draw text with rainbow glow effect and spiral arms"""
    if 0 <= row < len(screen):
        # Calculate the true center of the text
        text_center_x = col + len(text) // 2
        text_center_y = row

        # Draw spiral arms first (behind everything else)
        spiral_time = time.time() * 0.15
        arm_length = 40  # Shorter arms to be less intrusive
        num_arms = 4
        spiral_tightness = 4.8

        # Draw the spiral arms from the center
        for arm in range(num_arms):
            base_angle = (2 * math.pi * arm / num_arms) + spiral_time
            
            for t in range(arm_length):
                t_normalized = t / arm_length
                radius = 0.1 + (math.pow(t_normalized, 0.5) * 8.0)  # Reduced radius
                curve_factor = math.pow(t_normalized, 0.35)
                point_angle = base_angle + ((1 - curve_factor) * spiral_tightness * 2 * math.pi)

                dx = int(radius * math.cos(point_angle) * 1.6)
                dy = int(radius * math.sin(point_angle) * 0.8)

                glow_row = text_center_y + dy
                glow_col = text_center_x + dx

                if (0 <= glow_row < len(screen)) and (0 <= glow_col < len(screen[0])):
                    # Don't draw over the text area
                    if (row - 1 <= glow_row <= row + 1 and 
                        col - 1 <= glow_col <= col + len(text) + 1):
                        continue

                    # Enhanced character and intensity progression
                    point_progress = t / arm_length
                    if point_progress < 0.2:
                        glow_char = '✧'
                        intensity = 0.7
                    elif point_progress < 0.4:
                        glow_char = '✦'
                        intensity = 0.6
                    elif point_progress < 0.7:
                        glow_char = '·'
                        intensity = 0.4
                    else:
                        glow_char = '.'
                        intensity = 0.2

                    # Calculate color based on angle for rainbow effect
                    hue = (time_offset + (point_angle * 180 / math.pi)) % 360
                    r = int((math.sin(math.radians(hue)) + 2.2) * 127.5)
                    g = int((math.sin(math.radians(hue + 120)) + 2.2) * 127.5)
                    b = int((math.sin(math.radians(hue + 240)) + 2.2) * 127.5)

                    # Apply color with distance-based fade
                    arm_color = rgb_to_ansi(
                        min(255, int(r * intensity)),
                        min(255, int(g * intensity)),
                        min(255, int(b * intensity))
                    )

                    if screen[glow_row][glow_col] == ' ':  # Only draw if space is empty
                        screen[glow_row][glow_col] = arm_color + glow_char

        # Draw the original cross glow and text (on top of spirals)
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
                
                # Draw main character with increased brightness and boldness
                text_pulse = 1.2 + math.sin(time_offset * 0.08 + i * 0.4) * 0.2
                main_color = rgb_to_ansi(
                    min(255, int(r * text_pulse)),
                    min(255, int(g * text_pulse)),
                    min(255, int(b * text_pulse))
                )
                # Add bold style to make text more pronounced
                screen[row][col + i] = "\033[1m" + main_color + char + "\033[22m"

def play(duration=10):
    try:
        columns, rows = shutil.get_terminal_size()
    except:
        columns, rows = 80, 24  # Default fallback

    # Make animation four rows shorter to ensure plenty of space for footer
    rows = max(3, rows - 4)
    
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

    # Update message and positioning
    message = "Welcome to the Multiverse"
    msg_row = rows // 2  # Center vertically
    msg_col = (columns - len(message)) // 2  # Center horizontally

    start_time = time.time()
    while (time.time() - start_time) < duration:
        # Clear the terminal screen
        os.system('cls' if os.name == 'nt' else 'clear')

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
                    # Ensure matrix rain doesn't overwrite the message area
                    if not (msg_row - 1 <= pos <= msg_row + 1 and 
                            msg_col <= drop_x < msg_col + len(message)):
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
                # Ensure particles don't overwrite the message area
                if not (msg_row - 1 <= y <= msg_row + 1 and 
                        msg_col <= x < msg_col + len(message)):
                    brightness = int(255 * p['life'])
                    screen[y][x] = rgb_to_ansi(brightness, brightness, brightness) + p['char']
            p['life'] -= random.uniform(0.02, 0.05)
            p['x'] += p['velocity_x']
            p['y'] += p['velocity_y']

        # Draw glowing rainbow message
        time_offset = time.time() * 10  # Adjusted for smoother color transitions
        draw_glowing_text(screen, msg_row, msg_col, message, time_offset)

        # Draw the screen
        for row_content in screen:
            print(''.join(char if char != ' ' else ' ' for char in row_content))

        # Add footer with exit instructions
        footer_text = "Press Ctrl+C to exit - then run the next file"
        footer_col = (columns - len(footer_text)) // 2
        print('\n\n' + ' ' * footer_col + rgb_to_ansi(150, 150, 150) + footer_text)

        sys.stdout.flush()
        time.sleep(0.05)

def create_second_script():
    """Create the second script file"""
    second_script = '''from flask import Flask, render_template
import webbrowser
import threading
import time

app = Flask(__name__)

def open_browser():
    """Start the browser after a short delay"""
    time.sleep(1.5)
    webbrowser.open('http://127.0.0.1:5000/')

@app.route('/')
def index():
    return "Welcome to your new project! Start building your multiverse here!"

if __name__ == '__main__':
    threading.Thread(target=open_browser).start()
    app.run(debug=True)
'''
    
    with open('run-me-second.py', 'w') as f:
        f.write(second_script)

def main():
    # Clear screen
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print(Fore.GREEN + "\nWelcome to the Multiverse Setup!" + Style.RESET_ALL)
    
    # Install requirements
    print("\nInstalling requirements...")
    if not install_requirements():
        print(Fore.RED + "Failed to install requirements. Please try again." + Style.RESET_ALL)
        return

    # User authentication
    while True:
        print("\n1. Create new user")
        print("2. Login")
        print("3. Exit")
        
        choice = input(Fore.CYAN + "\nEnter your choice (1-3): " + Style.RESET_ALL)
        
        if choice == '1':
            username = create_user()
            break
        elif choice == '2':
            username = login()
            break
        elif choice == '3':
            print(Fore.YELLOW + "\nSetup cancelled. Goodbye!" + Style.RESET_ALL)
            return
        else:
            print(Fore.RED + "Invalid choice. Please try again." + Style.RESET_ALL)

    # Create Flask application and second script
    create_flask_app()
    create_second_script()
    
    # Play welcome animation
    try:
        play(duration=10)
    except KeyboardInterrupt:
        # Clear the screen
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n\n")
        print(Fore.GREEN + "Next step:" + Style.RESET_ALL)
        print(Fore.CYAN + "    python run-me-first.py" + Style.RESET_ALL)
        print("\n")
    finally:
        print(Style.RESET_ALL)

if __name__ == "__main__":
    main()
