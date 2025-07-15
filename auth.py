from time import sleep
import hashlib
import subprocess
import pyperclip
import http.client
import sys

keyStatus = False  # 0 = licence not valid, 1 = licence is valid
yourkey = ""


def check_hardware_id():
    global yourkey
    global keyStatus
    hardwareid = (
        subprocess.check_output("wmic csproduct get uuid")
        .decode()
        .split("\n")[1]
        .strip()
    )
    get_key = hashlib.md5(hardwareid.encode())
    yourkey = str(get_key.hexdigest())
    # Copy the value of the hardware_id variable to the clipboard
    pyperclip.copy(yourkey)
    print("YOUR KEY: ", yourkey)


def validator():
    global yourkey
    global keyStatus
    try:
        conn = http.client.HTTPSConnection("yourhost.com")
        conn.request("GET", "/view/data/raw")
        response = conn.getresponse()
        if response.status == 200:
            rawmac = response.read().decode("utf-8")
            if yourkey in rawmac:
                keyStatus = True
                return True
            else:
                keyStatus = False
                return False
        else:
            print(f"Request failed with status: {response.status}")
            return False
    except Exception as e:
        print(f"Request failed: {e}")
        return False
    finally:
        conn.close()


def auth_login():
    def_pass = "password"
    if def_pass == "password":
        print("Valid App Password")
        check_hardware_id()
        if validator() == True:
            print("[+] YOUR LICENSE IS OK....")
            return True
        elif validator() == False:
            print("[-] [ERROR] YOUR LICENSE NOT IN OUR DATABASE")
            sleep(4)
            sys.exit()
        else:
            print("Invalid password")
            sys.exit()


if __name__ == "__main__":
    auth_login()
