import os
import time
import subprocess
import re
import json
import speedtest

st = speedtest.Speedtest()
NETWORK_INTERFACE = "Ethernet"  # replace with your network interface name


def run_speedtest():
    try:
        st.download()
        st.upload()
        speedtest_result = st.results.dict()
        download_speed = speedtest_result['download'] / (1024 * 1024)  # convert to Mbps
        upload_speed = speedtest_result['upload'] / (1024 * 1024)  # convert to Mbps
        ping = speedtest_result['ping']
        return download_speed, upload_speed, ping
    except Exception as e:
        print(f"Speedtest failed: {e}")
        return None, None, None



def get_router_ip():
    try:
        result = subprocess.check_output("ipconfig", shell=True)
        default_gateways = re.findall(r"Default Gateway . . . . . . . . . : (\d+\.\d+\.\d+\.\d+)", result.decode())
        for gateway in default_gateways:
            if gateway != '0.0.0.0':
                return gateway
    except Exception as e:
        print(f"Could not get router IP: {e}")
        return None

ROUTER_IP = get_router_ip()  # automatically set your router's IP


def check_network(target="google.com"):
    response = os.system(f"ping -n 1 {target}")
    return response == 0


def log_network_status():
    with open("network_log.txt", "a") as file:
        while True:
            if not check_network():
                file.write(time.ctime() + " - Network: DOWN\n")

                # Additional checks when network is down
                file.write("Checking router connection...\n")
                if check_network(ROUTER_IP):
                    file.write("Router is reachable.\n")
                else:
                    file.write("Cannot reach router.\n")

            time.sleep(5)  # check every 5 seconds





if __name__ == "__main__":
    log_network_status()
