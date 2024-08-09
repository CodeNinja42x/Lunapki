import schedule
import time
import subprocess

def job():
    subprocess.run(["/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/venv/bin/python", "/Users/gorkemberkeyuksel/Documents/GitHub/Lunapki/crypto_trading_bot/Bot/main_script.py"])

# Schedule jobs
schedule.every().hour.at(":00").do(job)
schedule.every().day.at("00:00").do(job)

# Start the scheduler
while True:
    schedule.run_pending()
    time.sleep(1)
