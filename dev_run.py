import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class ReloadHandler(FileSystemEventHandler):
    def __init__(self):
        self.proc = subprocess.Popen(["python", "main.py"])

    def on_modified(self, event):
        if event.src_path.endswith(".py"):
            self.proc.kill()
            self.proc = subprocess.Popen(["python", "main.py"])


if __name__ == "__main__":
    handler = ReloadHandler()
    observer = Observer()
    observer.schedule(handler, ".", recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
