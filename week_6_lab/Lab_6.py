import requests
from bs4 import BeautifulSoup
import json
import csv
from housing_models import Property

# ==========================================
# Step 1: The Request Handshake
# ==========================================
print("\n=== STEP 1: The Request Handshake ===")

url = "https://alonhadat.com.vn/can-ban-nha-dat/ha-noi.html"

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

try:
    response = requests.get(url, headers=headers, timeout=10)
    if response.status_code == 200:
        print("--- Connection Successful: Data Received ---")
    else:
        print(f"--- Connection Failed: Status Code {response.status_code} ---")
except Exception as e:
    print(f"--- Connection Error: {e} ---")


# ==========================================
# Step 2: Target Identification and Extraction
# ==========================================
print("\n=== STEP 2: Target Identification ===")

soup = BeautifulSoup(response.text, 'html.parser')
listings = soup.find_all('div', class_='property-item')

if not listings:
    print("(Live scraping blocked or structure changed. Activating Fallback HTML...)")
    mock_html = """
    <div class="property-item">
        <span class="address">Thanh Xuân, Hà Nội</span>
        <span class="price">Giá: 5.5 Tỷ VND</span>
        <span class="sqm">Diện tích: 75 m2</span>
    </div>
    <div class="property-item">
        <span class="address">Cầu Giấy, Hà Nội</span>
        <span class="price">12.0 Billion VND</span>
        <span class="sqm">120m2</span>
    </div>
    <div class="property-item">
        <span class="address">Hà Đông, Hà Nội</span>
        <span class="price">Price on Request</span>
        <span class="sqm">80 m2</span>
    </div>
    """
    soup = BeautifulSoup(mock_html, 'html.parser')
    listings = soup.find_all('div', class_='property-item')

print("\n--- Raw Data (First 3 listings) ---")
extracted_data = []


for i, item in enumerate(listings[:3]):
    address_tag = item.find(class_='address')
    price_tag = item.find(class_='price')
    sqm_tag = item.find(class_='sqm')
    
    raw_address = address_tag.text if address_tag else "Unknown"
    raw_price = price_tag.text if price_tag else "Unknown"
    raw_sqm = sqm_tag.text if sqm_tag else "Unknown"
    
    extracted_data.append({"address": raw_address, "price": raw_price, "sqm": raw_sqm})
    print(f"Listing {i+1}: {raw_address} | {raw_price} | {raw_sqm}")


# ==========================================
# Step 3: Data Cleaning and Type Conversion
# ==========================================
print("\n=== STEP 3: Data Cleaning ===")

def clean_data(raw_price, raw_sqm):
    try:
        c_price = raw_price.replace("Giá:", "").replace("Tỷ VND", "").replace("Billion VND", "").strip()
        price = float(c_price)
        
        c_sqm = raw_sqm.replace("Diện tích:", "").replace("m2", "").strip()
        sqm = int(c_sqm)
        
        return price, sqm
    except ValueError:
        return None, None


# ==========================================
# Step 4: Automated Object Creation with ID Tracking
# ==========================================
print("\n=== STEP 4: Automated Object Creation ===")

scraped_results = []
prop_id = 5001

for data in extracted_data:
    raw_p = data['price']
    raw_s = data['sqm']
    
    price, sqm = clean_data(raw_p, raw_s)
    print(f"Raw: [{raw_p}] & [{raw_s}]  -->  Cleaned: [{price}] & [{sqm}]")
    
    if price is not None and sqm is not None:
        new_prop = Property(prop_id, data['address'], price, sqm)
        scraped_results.append(new_prop)
        prop_id += 1

print(f"\n--- Total successfully created objects: {len(scraped_results)} ---")


# ==========================================
# Step 5: Data Persistence (JSON/CSV Output)
# ==========================================
print("\n=== STEP 5: Data Persistence ===")


json_data = [prop.__dict__ for prop in scraped_results]
with open("scraped_data.json", "w", encoding="utf-8") as f:
    json.dump(json_data, f, indent=4, ensure_ascii=False)


with open("scraped_data.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(['id', 'address', 'price', 'sqm'])  # Header
    for prop in scraped_results:
        writer.writerow([prop.prop_id, prop.address, prop.price_bil_vnd, prop.sqm])

print("--- System: Data successfully saved to 'scraped_data.json' and 'scraped_data.csv' ---")