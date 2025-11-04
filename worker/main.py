import time
from datetime import datetime

def main():
    while True:
        print(f"[{datetime.utcnow()}] 🧠 CryptoCat Worker is alive and ready to collect data...")
        # Placeholder for collectors (Reddit, Twitter, etc.)
        time.sleep(600)  # wait 10 minutes before the next check

if __name__ == "__main__":
    main()
