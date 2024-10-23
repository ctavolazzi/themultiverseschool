import subprocess
import sys
import webbrowser
import os
import time

def run_flask_app():
    subprocess.Popen([sys.executable, 'app/app.py'])
    # Wait for the server to start
    time.sleep(2)
    webbrowser.open('http://127.0.0.1:5000')

if __name__ == '__main__':
    run_flask_app()
