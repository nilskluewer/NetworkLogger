import os
import time

def check_network():
    response = os.system("ping -n 1 google.com")
    if response == 0:
        return True
    else:
        return False

def log_network_status():
    with open("network_log.txt", "a") as file:
        while True:
            if check_network():
                file.write(time.ctime() + " - Network: UP\n")
            else:
                file.write(time.ctime() + " - Network: DOWN\n")
            time.sleep(60)  # check every minute

if __name__ == "__main__":
    log_network_status()
