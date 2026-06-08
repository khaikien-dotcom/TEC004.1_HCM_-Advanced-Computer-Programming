import json
import csv
from specialized_housing import market_dashboard, Apartment, Villa, Penthouse

# =====================================================================
# PART 3: SYSTEM LOGGING & MAINTENANCE (TÍCH HỢP CHO STEP 5)
# =====================================================================

def log_action(message):
    """
    Step 5: Ghi lại các vết hành động của hệ thống vào file nhật ký system.log.
    Sử dụng chế độ append mode ('a') để ghi nối tiếp nội dung, không làm mất log cũ.
    """
    with open("system.log", "a", encoding="utf-8") as log_file:
        log_file.write(message + "\n")


# =====================================================================
# PART 1: JSON ENGINEERING
# =====================================================================

def export_to_json(listings, filename):
    """Step 1: Xuất danh sách object ra cấu trúc JSON thông qua __dict__"""
    processed_listings = [
        {**item.__dict__, "type": type(item).__name__}
        for item in listings
    ]
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(processed_listings, file, indent=4, ensure_ascii=False)
    print(f"[SUCCESS] Step 1: Đã xuất {len(processed_listings)} bất động sản ra '{filename}'!")
    
    # Yêu cầu số 4: Gọi hàm log_action ở cuối bước xuất JSON
    log_action(f"[JSON EXPORT] Successfully exported {len(processed_listings)} objects to '{filename}'")


def import_from_json(filename):
    """Step 2: Đọc file JSON và khôi phục (rehydrate) lại thành các Object ban đầu"""
    with open(filename, "r", encoding="utf-8") as file:
        raw_data = json.load(file)
        
    rehydrated_listings = []
    for data in raw_data:
        class_type = data.get("type")
        if class_type == "Apartment":
            obj = Apartment(data["prop_id"], data["address"], data["price"], data["sqm"], data["floor_level"])
        elif class_type == "Villa":
            obj = Villa(data["prop_id"], data["address"], data["price"], data["sqm"], data["has_pool"])
        elif class_type == "Penthouse":
            obj = Penthouse(data["prop_id"], data["address"], data["price"], data["sqm"], data["has_private_elevator"])
        else:
            continue
        rehydrated_listings.append(obj)
    return rehydrated_listings


# =====================================================================
# PART 2: TABULAR DATA SYSTEMS
# =====================================================================

def export_to_csv(listings, filename):
    """Step 3: Xuất dữ liệu ra file bảng tính CSV (Cột đầu là prop_id)"""
    header = ['id', 'address', 'price', 'sqm', 'type']
    
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(header)
        
        for item in listings:
            row = [
                item.prop_id,
                item.address,
                item.price,
                item.sqm,
                type(item).__name__
            ]
            writer.writerow(row)
            
    print(f"[SUCCESS] Step 3: Đã xuất dữ liệu bảng tính ra file '{filename}' thành công!")
    
    # Yêu cầu số 4: Gọi hàm log_action ở cuối bước xuất CSV
    log_action(f"[CSV EXPORT] Successfully exported market data table to '{filename}'")


def interactive_data_entry(listings):
    """Step 4: Cho phép nhập liệu tương tác từ terminal và chống crash bằng try/except"""
    print("\n" + "="*20 + " CỬA SỔ NHẬP DỮ LIỆU BẤT ĐỘNG SẢN " + "="*20)
    
    while True:
        print("\n[HỆ THỐNG] Vui lòng nhập thông tin (hoặc gõ 'exit' ở mục Địa chỉ để thoát):")
        address = input("1. Nhập địa chỉ bất động sản: ").strip()
        if address.lower() == 'exit':
            print("[HỆ THỐNG] Đã thoát chương trình nhập liệu tương tác.")
            break
            
        try:
            price = float(input("2. Nhập giá bán (tỷ VND): "))
            sqm = float(input("3. Nhập diện tích sử dụng (sqm): "))
            if price <= 0 or sqm <= 0:
                print("[LỖI DỮ LIỆU] Các giá trị phải lớn hơn 0! Vui lòng nhập lại.")
                continue
        except ValueError:
            print("\n>>> [LỖI NGOẠI LỆ] Cảnh báo: Bạn đã nhập sai định dạng số!")
            # Tiện ích bổ sung: log lại cả hành vi nhập lỗi của người dùng vào hệ thống log
            log_action("[WARNING] System caught a ValueError during manual data entry.")
            continue

        print("4. Chọn phân loại bất động sản (1: Apartment | 2: Villa | 3: Penthouse)")
        choice = input("Lựa chọn của bạn (1-3): ").strip()
        next_id = max([item.prop_id for item in listings]) + 1
        
        if choice == "1":
            try:
                floor = int(input(" -> Nhập số tầng: "))
                new_property = Apartment(next_id, address, price, sqm, floor)
            except ValueError:
                print("[LỖI] Số tầng phải là số nguyên!")
                continue
        elif choice == "2":
            has_pool_input = input(" -> Villa có hồ bơi không? (y/n): ").strip().lower()
            has_pool = True if has_pool_input == 'y' else False
            new_property = Villa(next_id, address, price, sqm, has_pool)
        elif choice == "3":
            has_el_input = input(" -> Penthouse có thang máy riêng không? (y/n): ").strip().lower()
            has_elevator = True if has_el_input == 'y' else False
            new_property = Penthouse(next_id, address, price, sqm, has_elevator)
        else:
            print("[LỖI PHÂN LOẠI] Lựa chọn không hợp lệ!")
            continue
            
        listings.append(new_property)
        print(f"[THÀNH CÔNG] Đã tự động cấp ID {next_id} và thêm vào dashboard!")
        
        # Ghi log sự kiện thêm bất động sản mới thành công
        log_action(f"[DATA INSERTION] Successfully added new property ID {next_id} ({type(new_property).__name__}) to memory")


# =====================================================================
# KHỐI LỆNH THỰC THI (MAIN)
# =====================================================================
if __name__ == "__main__":
    print("--- BẮT ĐẦU CHẠY PIPELINE KIỂM THỬ TUẦN 5 ---")
    
    # 1. Chạy xuất JSON -> Tự động kích hoạt ghi log lần 1
    export_to_json(market_dashboard, "listings.json")
    
    # 2. Chạy xuất CSV -> Tự động kích hoạt ghi log lần 2
    export_to_csv(market_dashboard, "market_report.csv")
    
    # 3. Chạy chương trình nhập liệu tương tác (Có thể gõ 'exit' luôn nếu chỉ muốn test log xuất file)
    interactive_data_entry(market_dashboard)
    
    print("\n--- HOÀN THÀNH TOÀN BỘ TIẾN TRÌNH STEP 5 ---")