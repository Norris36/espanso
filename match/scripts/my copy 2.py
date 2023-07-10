import subprocess
import time
#start_time = time.now().timestamp()
def wifi_control():
    # Turn off the WiFi
    subprocess.run('netsh interface set interface "Wi-Fi" admin=disable', shell=True)
    
    # Wait for 5 seconds
    time.sleep(5)
    
    # Turn on the WiFi
    subprocess.run('netsh interface set interface "Wi-Fi" admin=enable', shell=True)


print("wifi will turn on in four seconds")

wifi_control()

