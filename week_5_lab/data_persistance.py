import json
from specialized_housing import Apartment, Villa, Penthouse, market_dashboard

# ================= PART 1: SYSTEM LOGGING & MAINTENANCE =================

def log_action(message):
    """
    Mở file system.log ở chế độ append ('a') và ghi lại hành động hệ thống,
    tự động thêm dấu xuống dòng (\n).
    """
    with open("system.log", "a", encoding="utf-8") as log_file:
        log_file.write(message + "\n")


# ================= PART 2: JSON ENGINEERING =================

def export_to_json(listings, filename):
    """
    Sử dụng List Comprehension để chuyển đổi danh sách đối tượng 
    thành danh sách các dictionary và lưu thành file JSON.
    """
    listings_dict_list = [
        {**obj.__dict__, "type": obj.__class__.__name__} 
        for obj in listings
    ]
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(listings_dict_list, f, indent=4, ensure_ascii=False)
        
    print(f"✔️ [SUCCESS] Đã xuất {len(listings_dict_list)} dữ liệu bất động sản ra file '{filename}'")
    
    # Ghi nhật ký hệ thống
    log_action(f"Successfully exported {len(listings_dict_list)} properties to {filename}")


def import_from_json(filename):
    """
    Đọc file JSON, chuyển đổi các dictionary thành các đối tượng tương ứng 
    (Apartment, Villa, Penthouse) dựa vào key 'type'.
    """
    with open(filename, 'r', encoding='utf-8') as f:
        data_list = json.load(f)
    
    rehydrated_listings = []
    
    for item in data_list:
        # Tách trường 'type' ra khỏi thuộc tính đối tượng để không lỗi tham số khởi tạo
        prop_type = item.pop("type", None)
        
        if prop_type == "Apartment":
            obj = Apartment(**item)
        elif prop_type == "Villa":
            obj = Villa(**item)
        elif prop_type == "Penthouse":
            obj = Penthouse(**item)
        else:
            print(f"⚠️ [WARNING] Không tìm thấy loại Class phù hợp cho: {prop_type}")
            continue
            
        rehydrated_listings.append(obj)
    
    # In ra kiểu dữ liệu type() để kiểm chứng cấu trúc đối tượng
    print("\n--- PROVING DATA REHYDRATION (Object Types) ---")
    for obj in rehydrated_listings:
        print(f"Property ID: {obj.prop_id} -> Object Type: {type(obj)}")
        
    return rehydrated_listings


def export_to_csv(listings, filename):
    """
    Giả định xuất dữ liệu ra file CSV và ghi nhật ký hệ thống.
    """
    # (Đoạn code xử lý ghi file CSV của bạn tại đây nếu có)
    log_action(f"All properties successfully exported to {filename}")


# ================= PART 3: INTERACTIVE DATA ENTRY & VALIDATION =================

def interactive_data_entry(listings):
    print("\n--- STEP 4: INTERACTIVE DATA ENTRY & VALIDATION ---")
    
    # Tự động tính unique prop_id tiếp theo bằng cách lấy max id hiện tại + 1
    if listings:
        next_id = max(obj.prop_id for obj in listings) + 1
    else:
        next_id = 101

    while True:
        print(f"\n[Adding New Property | Assigned ID: {next_id}]")
        address = input("Enter address (or type 'exit' to stop): ").strip()
        
        if address.lower() == 'exit':
            print("Exiting data entry mode.")
            break
            
        # Sử dụng try/except để kiểm tra dữ liệu nhập vào
        try:
            price_input = input("Enter price (in billion VND): ")
            price_bil_vnd = float(price_input)
            
            sqm_input = input("Enter area (in sqm): ")
            sqm = float(sqm_input)
            
        except ValueError:
            print("\n❌ [ERROR] Invalid input! Price and Area must be numbers. Please try again.")
            continue

        print("Select property type: 1. Apartment | 2. Villa | 3. Penthouse")
        choice = input("Your choice (1-3): ").strip()
        
        if choice == "1":
            try:
                floor = int(input("Enter floor level: "))
                new_prop = Apartment(next_id, address, price_bil_vnd, sqm, floor)
            except ValueError:
                print("\n❌ [ERROR] Floor level must be an integer. Restarting entry.")
                continue
        elif choice == "2":
            has_pool_input = input("Does it have a pool? (y/n): ").strip().lower()
            has_pool = has_pool_input == 'y'
            new_prop = Villa(next_id, address, price_bil_vnd, sqm, has_pool)
        elif choice == "3":
            has_elev_input = input("Does it have a private elevator? (y/n): ").strip().lower()
            has_private_elevator = has_elev_input == 'y'
            new_prop = Penthouse(next_id, address, price_bil_vnd, sqm, has_private_elevator)
        else:
            print("\n❌ [ERROR] Invalid choice. Restarting entry.")
            continue

        listings.append(new_prop)
        print(f"✔️ [SUCCESS] Property ID {next_id} added to market_dashboard!")
        next_id += 1


# ================= PART 4: DATA INTEGRITY CHECK =================

def verify_integrity(original_list, imported_list):
    """
    So sánh độ dài và kiểm tra từng cặp prop_id giữa list gốc và list import 
    để xác minh tính toàn vẹn của dữ liệu.
    """
    print("\n--- STEP 6: DATA INTEGRITY CHECK ---")
    
    if len(original_list) != len(imported_list):
        print("❌ [FAILED] Integrity Check: Lists have different lengths!")
        return False
        
    for orig_item, imp_item in zip(original_list, imported_list):
        if orig_item.prop_id != imp_item.prop_id:
            print(f"❌ [FAILED] Integrity Check: ID mismatch found! ({orig_item.prop_id} != {imp_item.prop_id})")
            return False
        
    print("✅ Data Integrity Verified: All lists are identical in count and IDs.")
    return True


# ================= PART 5: MAIN EXECUTION FLOW =================

if __name__ == "__main__":
    # 1. Khởi tạo và ghi nhận nhật ký hệ thống
    log_action("System initialized.")
    
    # 2. Chạy vòng lặp cho phép người dùng nhập thêm dữ liệu từ Terminal
    interactive_data_entry(market_dashboard)
    
    # 3. Xuất dữ liệu đã cập nhật trong market_dashboard ra file JSON
    export_to_json(market_dashboard, "listings.json")
    
    # 4. Nạp và khôi phục (rehydrate) lại đối tượng từ file JSON vừa xuất
    imported_listings = import_from_json("listings.json")
    
    # 5. Kiểm tra tính toàn vẹn giữa danh sách hiện tại và danh sách khôi phục từ file
    verify_integrity(market_dashboard, imported_listings)
