import sys
import subprocess
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class ChangeHandler(FileSystemEventHandler):
    def __init__(self, command):
        super().__init__()
        self.command = command
        self.process = subprocess.Popen(self.command)

    def on_modified(self, event):
        # Restart the application when a file is modified
        if "__pycache__" in event.src_path:
            return
        print(f'{event.src_path} has been modified; restarting application...')
        self.process.terminate()
        time.sleep(0.5)  # Wait for the process to terminate
        self.process = subprocess.Popen(self.command)

    def on_created(self, event):
        self.on_modified(event)

if __name__ == "__main__":
    command = [sys.executable, "FACSPyUI.py"]
    
    # Create an event handler and observer
    event_handler = ChangeHandler(command)
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=True)  # Watch the current directory

    print("Starting watchdog to monitor file changes...")
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
