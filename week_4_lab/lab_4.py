from specialized_housing import market_dashboard
from specialized_housing import Apartment, Villa, Penthouse
# =============== LAB 4: Functional Programming — Data Pipelines ================
print("\n" + "-"*10 + "LAB 4: Functional Programming — Data Pipelines" + "-"*10)
print("="*50)
print("PART 1: THE FILTERING & MAPPING PIPELINE")
print("="*50)

# ---------------------------- Step 1: Multi-Condition Filtering ----------------------------
print("\n--- Step 1: 'Best Value' Properties ---")

# Sử dụng filter() và lambda để lọc các property có price < 10.0 VÀ sqm > 60
best_value_properties = list(filter(lambda p: p.price < 10.0 and p.sqm > 60, market_dashboard))

# In kết quả sử dụng display_listing() theo yêu cầu
if not best_value_properties:
    print("No properties match the 'Best Value' criteria (Price < 10.0B AND SQM > 60).")
else:
    for prop in best_value_properties:
        prop.display_listing()

# ---------------------------- Step 2: Complex Mapping (The Analysis List) ----------------------------
print("\n--- Step 2: Price Analysis Mapping ---")

# Sử dụng map() và lambda để trích xuất dữ liệu và tính toán Price / SQM
# Ép kiểu list để có thể duyệt qua và in ra màn hình
analysis_list = list(map(
    lambda p: f"[ID: {p.prop_id}] at [{p.address}] | Unit Price: {p.price / p.sqm:.5f}B per sqm", 
    market_dashboard
))

# In các chuỗi kết quả
for analysis in analysis_list:
    print(analysis)

from functools import reduce

# =============== PART 2: AGGREGATION & SORTING ===============
print("\n" + "="*50)
print("PART 2: AGGREGATION & SORTING")
print("="*50)

# ---------------------------- Step 3: Advanced Reduce (Finding the Market Leader) ----------------------------
print("\n--- Step 3: Finding the Market Leader (Most Expensive Property) ---")

# Sử dụng reduce() và lambda để so sánh giá của 2 đối tượng, trả về đối tượng có giá cao hơn
market_leader = reduce(lambda a, b: a if a.price > b.price else b, market_dashboard)

print("Most Expensive Property Found:")
market_leader.display_listing()

# ---------------------------- Step 4: Custom Sorting with Lambdas ----------------------------
print("\n--- Step 4: Properties Sorted by Size (Descending) ---")

# Tạo list sorted_by_size sử dụng sorted(), sắp xếp theo thuộc tính sqm giảm dần (reverse=True)
sorted_by_size = sorted(market_dashboard, key=lambda p: p.sqm, reverse=True)

# Lặp qua danh sách đã sắp xếp và in ra ID, address, và sqm
for p in sorted_by_size:
    print(f"ID: {p.prop_id} | Address: {p.address} | SQM: {p.sqm}")

# ---------------------------- Step 4: Custom Sorting with Lambdas ----------------------------
print("\n--- Step 4: Properties Sorted by Size (Descending) ---")

# 1. & 2. Tạo list sorted_by_size sử dụng sorted() và lambda, sắp xếp theo sqm giảm dần (reverse=True)
sorted_by_size = sorted(market_dashboard, key=lambda p: p.sqm, reverse=True)

# 3. Lặp qua danh sách đã sắp xếp và in ra ID, address, và sqm
for p in sorted_by_size:
    print(f"ID: {p.prop_id} | Address: {p.address} | SQM: {p.sqm}")

# =============== PART 3: CLOSURES, COMPREHENSIONS, & DECORATORS ===============
print("\n" + "="*50)
print("PART 3: CLOSURES, COMPREHENSIONS, & DECORATORS")
print("="*50)

# ---------------------------- Step 5: Currency Converter Factory (Closures) ----------------------------
print("\n--- Step 5: Currency Converter Factory ---")

# 1. Khởi tạo Closure để tạo ra các hàm chuyển đổi tiền tệ
def make_currency_converter(exchange_rate):
    def convert(price_in_billions):
        # Do thuộc tính price đang lưu ở dạng Tỷ VNĐ (vd: 15.5), 
        # ta cần nhân với 1,000,000,000 để ra số tiền gốc trước khi chia cho tỷ giá.
        actual_vnd = price_in_billions * 1_000_000_000
        return actual_vnd / exchange_rate
    return convert

# 2. Tạo 2 hàm chuyển đổi cụ thể: to_usd và to_euro
to_usd = make_currency_converter(25000)
to_euro = make_currency_converter(27000)

# Lấy thử một đối tượng Penthouse trong market_dashboard (ID 401, giá 15.5B)
sample_penthouse = next(p for p in market_dashboard if isinstance(p, Penthouse))

# Thực hiện chuyển đổi giá
usd_price = to_usd(sample_penthouse.price)
euro_price = to_euro(sample_penthouse.price)

print(f"Penthouse ID {sample_penthouse.prop_id} - Original Price: {sample_penthouse.price}B VND")
print(f"Equivalent in USD: ${usd_price:,.2f}")
print(f"Equivalent in EURO: €{euro_price:,.2f}")


# ---------------------------- Step 6: Dynamic Tax Simulation (Comprehensions) ----------------------------
print("\n--- Step 6: Dynamic Tax Simulation ---")

# Sử dụng List Comprehension để duyệt, lọc dữ liệu (chỉ lấy Apartment, Penthouse) và tạo ra dictionary
projected_market = [
    {"ID": p.prop_id, "Taxed_Price": p.price * 1.1} 
    for p in market_dashboard 
    if isinstance(p, (Apartment, Penthouse))
]

# In ra từng dictionary trong list để hoàn thiện Deliverable 4.6
for item in projected_market:
    print(item)

# ---------------------------- Step 7: The Audit Tracker (General Decorators) ----------------------------
print("\n--- Step 7: The Audit Tracker ---")

# 1, 2 & 3. Khởi tạo decorator audit_log
def audit_log(func):
    # Sử dụng *args và **kwargs để decorator có thể bọc bất kỳ hàm nào, dù có bao nhiêu tham số
    def wrapper(*args, **kwargs):
        # In log trước khi chạy hàm, sử dụng func.__name__ để lấy tên hàm linh hoạt
        print(f"[LOG] Executing: {func.__name__}...")
        
        # Thực thi hàm gốc và lưu lại kết quả
        result = func(*args, **kwargs)
        
        # In log sau khi hàm chạy xong
        print(f"[LOG] {func.__name__} complete.")
        
        return result
    return wrapper

# 4 & 5. Áp dụng decorator @audit_log vào hàm update_listing_status
@audit_log
def update_listing_status(prop_id, status):
    print(f"Property {prop_id} status updated to: {status}")

# Chạy thử hàm với các ID và status khác nhau để lấy kết quả cho Deliverable 4.7
update_listing_status(401, "SOLD")
print("-" * 30)
update_listing_status(202, "UNDER CONTRACT")