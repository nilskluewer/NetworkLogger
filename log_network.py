import os
import time
import subprocess
import re

NETWORK_INTERFACE = "Ethernet"  # replace with your network interface name

def get_router_ip():
    try:
        result = subprocess.check_output("ipconfig", shell=True)
        default_gateways = re.findall(r"Default Gateway . . . . . . . . . : (\d+\.\d+\.\d+\.\d+)", result.decode())
        for gateway in default_gateways:
            if gateway != '0.0.0.0':
                return gateway
    except Exception as e:
        return str(e)

ROUTER_IP = get_router_ip()  # automatically set your router's IP

def check_network(target="google.com"):
    response = os.system(f"ping -n 1 {target}")
    return response == 0

def check_nic_status():
    try:
        output = subprocess.check_output(f"netsh interface show interface \"{NETWORK_INTERFACE}\"", shell=True)
        return "connected" in output.decode().lower()
    except Exception as e:
        return str(e)

def check_dns_resolution():
    try:
        output = subprocess.check_output("nslookup google.com", shell=True)
        return "Non-existent domain" not in output.decode()
    except Exception as e:
        return str(e)

def check_traceroute():
    try:
        output = subprocess.check_output("tracert 8.8.8.8", shell=True)
        return output.decode()
    except Exception as e:
        return str(e)

def log_network_status():
    with open("network_log.txt", "a") as file:
        while True:
            if check_network():
                file.write(time.ctime() + " - Network: UP\n")
            else:
                file.write(time.ctime() + " - Network: DOWN\n")
                
                # Additional checks when network is down
                file.write("Checking router connection...\n")
                if check_network(ROUTER_IP):
                    file.write("Router is reachable.\n")
                else:
                    file.write("Cannot reach router.\n")
                
                file.write("Checking NIC status...\n")
                nic_status = check_nic_status()
                if nic_status is True:
                    file.write("NIC is running.\n")
                else:
                    file.write(f"NIC status check error: {nic_status}\n")
                
                file.write("Checking DNS resolution...\n")
                if check_dns_resolution():
                    file.write("DNS resolution is working.\n")
                else:
                    file.write("DNS resolution failed.\n")
                
                file.write("Running traceroute...\n")
                file.write(check_traceroute() + "\n")
                
            time.sleep(5)  # check every 5 seconds

if __name__ == "__main__":
    log_network_status()
