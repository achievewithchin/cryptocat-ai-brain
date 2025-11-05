# worker/worker.py
import time
from datetime import datetime

def main():
    while True:
        print(f"🐱 CryptoCat Worker is alive and purring... {datetime.utcnow().isoformat()}")
        time.sleep(60)

if __name__ == "__main__":
    main()
