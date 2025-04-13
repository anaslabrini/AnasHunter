import requests
import random
import time
import base64
from datetime import datetime
import os

def get_stealth_headers():
    return {
        'User-Agent': random.choice([
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'Mozilla/5.0 (X11; Linux x86_64)',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'
        ]),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }

def encode_url(url):
    return base64.b64encode(url.encode()).decode()

def log_result(entry):
    with open("results.txt", "a") as f:
        f.write(entry + "\n")

def stealth_clickjacking_scan(domain):
    protocols = ['https://', 'http://']
    headers = get_stealth_headers()

    for proto in protocols:
        url = proto + domain
        encoded_url = encode_url(url)
        time.sleep(random.uniform(0.5, 1.2))

        print(f"\n[🔍] Sending encrypted scan for: {url} -> Encoded as: {encoded_url}")
        try:
            response = requests.get(url, headers=headers, timeout=5)
            x_frame = response.headers.get('X-Frame-Options')
            csp = response.headers.get('Content-Security-Policy')

            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            vulnerable = False
            result_log = f"\n[*] Time: {now}\n[*] Target: {url}\n[*] Protocol: {proto.upper()}\n[*] Vulnerability: Clickjacking"

            if not x_frame:
                result_log += f"\n[*] Missing Header: X-Frame-Options"
                vulnerable = True
            else:
                result_log += f"\n[*] X-Frame-Options: {x_frame}"

            if not csp:
                result_log += f"\n[*] Missing Header: Content-Security-Policy"
                vulnerable = True
            else:
                if "frame-ancestors" in csp:
                    result_log += f"\n[*] CSP frame-ancestors: OK"
                else:
                    result_log += f"\n[*] CSP Present but without frame-ancestors"
                    vulnerable = True

            if vulnerable:
                result_log += "\n[+] Result: VULNERABLE to Clickjacking!"
            else:
                result_log += "\n[-] Result: Site is Protected."

            print(result_log)
            log_result(result_log)

        except Exception as e:
            error_log = f"\n[-] Error accessing {url}: {e}"
            print(error_log)
            log_result(error_log)

if __name__ == "__main__":
    os.system("clear")
    print("""
    \033[91m 
 ██████╗██╗     ██╗ ██████╗██╗  ██╗         ██╗ █████╗  ██████╗██╗  ██╗██╗███╗   ██╗ ██████╗ 
██╔════╝██║     ██║██╔════╝██║ ██╔╝         ██║██╔══██╗██╔════╝██║ ██╔╝██║████╗  ██║██╔════╝ 
██║     ██║     ██║██║     █████╔╝          ██║███████║██║     █████╔╝ ██║██╔██╗ ██║██║  ███╗				Anass Labrini
██║     ██║     ██║██║     ██╔═██╗     ██   ██║██╔══██║██║     ██╔═██╗ ██║██║╚██╗██║██║   ██║
╚██████╗███████╗██║╚██████╗██║  ██╗    ╚█████╔╝██║  ██║╚██████╗██║  ██╗██║██║ ╚████║╚██████╔╝
 ╚═════╝╚══════╝╚═╝ ╚═════╝╚═╝  ╚═╝     ╚════╝ ╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝ ╚═════╝ 
                                                                                        
                                                  \033[0m
        """)
    domain = input(" Enter the target URL without http/https (example: test.com): ").strip()
    print("\n[*] Launch Incognito Clickjacking Scan...\n")
    stealth_clickjacking_scan(domain)

