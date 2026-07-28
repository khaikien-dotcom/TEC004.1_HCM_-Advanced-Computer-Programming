import time
from concurrent.futures import ThreadPoolExecutor
import requests

# 1. Five real estate target URLs
URLS = [
    "https://www.realtor.com",
    "https://www.redfin.com",
    "https://www.trulia.com",
    "https://www.homes.com",
    "https://www.century21.com",
]

# Browser User-Agent header to prevent real estate servers from dropping requests
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
}

def scrape_page(url):
    """Fetches the HTML of a page and returns response metrics."""
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        return {"url": url, "status": r.status_code, "size": len(r.text)}
    except requests.RequestException as e:
        return {"url": url, "status": "Error", "size": 0, "error": str(e)}

if __name__ == "__main__":
    print("=== Pipeline Benchmark: Sequential vs Threaded ===\n")

# 2. Standard For-Loop Execution (Sequential)
    start_seq = time.perf_counter()

    seq_results = []
    for url in URLS:
        seq_results.append(scrape_page(url))

    end_seq = time.perf_counter()
    duration_seq = end_seq - start_seq

    print("Sequential Results:")
    for res in seq_results:
        print(f"  [{res['status']}] {res['url']} -> {res['size']} bytes")
    print(f"\n-> Sequential For-Loop took: {duration_seq:.2f} seconds\n")

    
# 3. ThreadPoolExecutor Execution (Simultaneous / Concurrent)
    
    start_thread = time.perf_counter()

    with ThreadPoolExecutor(max_workers=5) as executor:
        # Executes scrape_page on all 5 URLs simultaneously
        threaded_results = list(executor.map(scrape_page, URLS))

    end_thread = time.perf_counter()
    duration_thread = end_thread - start_thread

    print("Threaded Results (executor.map):")
    for res in threaded_results:
        print(f"  [{res['status']}] {res['url']} -> {res['size']} bytes")
    print(f"\n-> Threaded Executor took:  {duration_thread:.2f} seconds\n")

# 4. Time Difference & Proof
    time_difference = duration_seq - duration_thread
    speedup = duration_seq / duration_thread if duration_thread > 0 else 1.0

    print("=== Proof & Performance Summary ===")
    print(f"Time Saved:     {time_difference:.2f} seconds")
    print(f"Speedup Factor: {speedup:.2f}x faster using ThreadPoolExecutor")