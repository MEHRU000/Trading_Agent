import os
import sys
import time
import subprocess
import urllib.request

CLOUDFLARED_URL = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe"
CLOUDFLARED_EXE = "cloudflared.exe"

def download_progress(block_num, block_size, total_size):
    downloaded = block_num * block_size
    if total_size > 0:
        percent = min(100, int(downloaded * 100 / total_size))
        # Clear line and print progress
        sys.stdout.write(f"\rDownloading Cloudflare helper: {percent}% completed...")
        sys.stdout.flush()
    else:
        sys.stdout.write(f"\rDownloading Cloudflare helper: {downloaded} bytes...")
        sys.stdout.flush()

def ensure_cloudflared():
    if os.path.exists(CLOUDFLARED_EXE):
        print("[✓] Cloudflare helper binary found locally.")
        return True
    
    print("Cloudflare helper helper binary is missing.")
    print("Downloading from official Cloudflare repository...")
    try:
        urllib.request.urlretrieve(CLOUDFLARED_URL, CLOUDFLARED_EXE, download_progress)
        print("\n[✓] Helper downloaded successfully!")
        return True
    except Exception as e:
        print(f"\n[X] Error downloading Cloudflare helper: {e}")
        print("Please check your internet connection or install cloudflared manually.")
        return False

def run_tunnel():
    print("\nStarting secure tunnel connection to http://127.0.0.1:7999/...")
    
    # Run cloudflared tunnel --url http://127.0.0.1:7999
    # Redirect stderr to stdout because cloudflared logs to stderr
    process = subprocess.Popen(
        [CLOUDFLARED_EXE, "tunnel", "--url", "http://127.0.0.1:7999"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )
    
    tunnel_url = None
    
    # Read output line by line to find the trycloudflare URL
    for line in iter(process.stdout.readline, ""):
        # Debug helper: print line locally if needed
        # print(line.strip())
        if ".trycloudflare.com" in line:
            # Extract the URL from the log line
            # e.g., "|  https://some-subdomain.trycloudflare.com  |"
            parts = line.split()
            for p in parts:
                if "trycloudflare.com" in p:
                    tunnel_url = p.strip()
                    break
            
            if tunnel_url:
                print("\n" + "="*70)
                print("   ★ SUCCESS! AUREON IS NOW LIVE ONLINE ★")
                print("="*70)
                print(f"   Dashboard Link: {tunnel_url}")
                print("="*70)
                print("   Share or open this link on your phone, laptop, or tablet")
                print("   to monitor and manage AUREON from anywhere!")
                print("="*70)
                print("\n   [Keep this window open to maintain the online connection]\n")
                break
                
    # Keep printing the process logs or wait
    try:
        for line in iter(process.stdout.readline, ""):
            # Silence uvicorn proxy logs unless needed, or just let them read in background
            pass
    except KeyboardInterrupt:
        print("\nClosing secure tunnel connection...")
        process.terminate()

if __name__ == "__main__":
    print("==========================================================")
    print("           EXPOSING AUREON TO SINGLE LINK")
    print("==========================================================")
    
    if ensure_cloudflared():
        run_tunnel()
