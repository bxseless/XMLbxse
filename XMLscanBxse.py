import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# ASCII art
print("""
▒██   ██▒ ███▄ ▄███▓ ██▓     ▄▄▄▄   ▒██   ██▒  ██████ ▓█████ 
▒▒ █ █ ▒░▓██▒▀█▀ ██▒▓██▒    ▓█████▄ ▒▒ █ █ ▒░▒██    ▒ ▓█   ▀ 
░░  █   ░▓██    ▓██░▒██░    ▒██▒ ▄██░░  █   ░░ ▓██▄   ▒███   
 ░ █ █ ▒ ▒██    ▒██ ▒██░    ▒██░█▀   ░ █ █ ▒   ▒   ██▒▒▓█  ▄ 
▒██▒ ▒██▒▒██▒   ░██▒░██████▒░▓█  ▀█▓▒██▒ ▒██▒▒██████▒▒░▒████▒
▒▒ ░ ░▓ ░░ ▒░   ░  ░░ ▒░▓  ░░▒▓███▀▒▒▒ ░ ░▓ ░▒ ▒▓▒ ▒ ░░░ ▒░ ░
░░   ░▒ ░░  ░      ░░ ░ ▒  ░▒░▒   ░ ░░   ░▒ ░░ ░▒  ░ ░ ░ ░  ░
 ░    ░  ░      ░     ░ ░    ░    ░  ░    ░  ░  ░  ░     ░   
 ░    ░         ░       ░  ░ ░       ░    ░        ░     ░  ░
""")

# Function to test for XML injection vulnerability
def test_xml_injection(url, payload):
    try:
        headers = {'Content-Type': 'application/xml'}
        response = requests.post(url, data=payload, headers=headers)
        if "error" in response.text.lower():
            print(f"[+] XML Injection vulnerability found at: {url}")
            print(f"Payload: {payload}")
            print(f"Response: {response.text[:200]}...")
        else:
            print(f"[-] No XML Injection vulnerability found at: {url}")
    except Exception as e:
        print(f"[-] Error testing {url}: {e}")

# Function to find forms and test for XML injection
def find_forms(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        forms = soup.find_all('form')
        for form in forms:
            action = form.get('action')
            if action:
                action = urljoin(url, action)
                method = form.get('method', 'get').lower()
                inputs = form.find_all('input')
                payloads = [
                    '<?xml version="1.0"?><root><name>test</name></root>',
                    '<?xml version="1.0"?><root><name>&lt;script&gt;alert("XML Injection")&lt;/script&gt;</name></root>'
                ]
                for payload in payloads:
                    data = {input.get('name'): payload for input in inputs if input.get('name')}
                    if method == 'post':
                        response = requests.post(action, data=data)
                    else:
                        response = requests.get(action, params=data)
                    if "error" in response.text.lower():
                        print(f"[+] XML Injection vulnerability found at: {action}")
                        print(f"Payload: {payload}")
                        print(f"Response: {response.text[:200]}...")
                    else:
                        print(f"[-] No XML Injection vulnerability found at: {action}")
    except Exception as e:
        print(f"[-] Error finding forms at {url}: {e}")

# Main function
def main():
    url = input("Enter the URL to test for XML Injection vulnerabilities: ")
    test_xml_injection(url, '<?xml version="1.0"?><root><name>test</name></root>')
    find_forms(url)

if __name__ == "__main__":
    main()
