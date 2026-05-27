import housing_models
#=============== Part 1: Expanding the Hierarchy ===================
#----------------------- Step 1 ------------------------
class Property:
    def __init__(self, prop_id: int, address: str, price: float, sqm: float):
        self.prop_id = prop_id
        self.address = address
        self.price = price
        self.sqm = sqm
        
    def display_listing(self):
        print(f"ID: {self.prop_id} | {self.address} | {self.price}B VND | {self.sqm} sqm")

class Apartment(Property):
    def __init__(self, prop_id: int, address: str, price: float, sqm: float, floor_level: int):
        super().__init__(prop_id, address, price, sqm)
        self.floor_level = floor_level

    def get_actual_area(self) -> float:
        return self.sqm * 1.05

    def display_listing(self):
        actual_area = self.get_actual_area()
        # Đã thêm dấu gạch đứng | sau phần giá tiền để đúng format đề bài
        print(
            f"[APT] ID: {self.prop_id} | "
            f"Floor {self.floor_level} | "
            f"{self.address} | "
            f"{self.price}B VND | "
            f"Area: {actual_area:.1f} sqm"
        )

#---------------------------- Step 2 --------------------------
class Villa(Property):
    def __init__(self, prop_id: int, address: str, price: float, sqm: float, has_pool: bool):
        super().__init__(prop_id, address, price, sqm)
        self.has_pool = has_pool

    def calculate_maintenance(self) -> float:
        return self.price * 0.0005

    def display_listing(self):
        maintenance_fee = self.calculate_maintenance()
        pool_status = "Yes" if self.has_pool else "No"
        print(
            f"[VILLA] ID: {self.prop_id} | "
            f"{self.address} | "
            f"Price: {self.price}B VND | "
            f"Pool: {pool_status} | "
            f"Maint. Fee: {maintenance_fee:.5f}B VND"
        )

    #-------------------------- STEP 6 -------------------------
    def add_pool(self):
        self.has_pool = True
        print(f"\n>>> [RENOVATION] A luxury pool has been built at Villa ID: {self.prop_id}! <<<")

#---------------------------- Step 3 ----------------------------
class Penthouse(Property):
    def __init__(self, prop_id: int, address: str, price: float, sqm: float, has_private_elevator: bool):
        super().__init__(prop_id, address, price, sqm)
        self.has_private_elevator = has_private_elevator

    def get_taxed_price(self) -> float:
        return self.price * 1.10

    def display_listing(self):
        total_price = self.get_taxed_price()
        elevator_status = "Yes" if self.has_private_elevator else "No"
        print(
            f"[PENTHOUSE] ID: {self.prop_id} | "
            f"Private Elevator: {elevator_status} | "
            f"{self.address} | "
            f"Total Price (w/ Tax): {total_price:.2f}B VND"
        )


#============== Part 2: Polymorphism & Advanced Reporting ===============
#---------------------------- Step 4 ----------------------------
def generate_market_report(listings):
    print("\n--- MARKET DASHBOARD REPORT ---")
    total_value = 0
    for item in listings:
        item.display_listing()
        total_value += item.price
    print("-" * 40)
    print(f"TOTAL MARKET VALUE: {total_value:.2f}B VND")
    print("-" * 40)

#---------------------------- Step 5 ----------------------------
def villa_inspection(listings):
    print("\n--- POOL INSPECTION LOG ---")
    for item in listings:
        if isinstance(item, Villa):
            print(f"--- Inspection Required for Pool at Property {item.prop_id} ---")
        else:
            print(f"--- Property {item.prop_id} does not require pool inspection ---")


#----- Chạy kiểm thử mẫu -----
if __name__ == "__main__":
    # Test lẻ Step 1, 2, 3
    apt = Apartment(201 ,"Ocean Park, Gia Lam", 3.1, 55, 15)
    apt.display_listing()

    villa = Villa(301, "Vinhomes Riverside", 35.0, 300, True)
    villa.display_listing()

    penthouse = Penthouse(401, "Keangnam Landmark 72", 15.5, 250, True)
    penthouse.display_listing()

    # Step 4 & 5: Khởi tạo list dashboard hoàn chỉnh
    market_dashboard = [
        Apartment(201, "Ocean Park, Gia Lam", 3.1, 55, 15),
        Apartment(202, "Vinhomes Smart City", 2.8, 45, 10),
        Villa(301, "Vinhomes Riverside", 35.0, 300, True),
        Villa(302, "Ciputra Tay Ho", 42.5, 450, False), # Đây là villa chưa có pool trong list
        Penthouse(401, "Keangnam Landmark 72", 15.5, 250, True),
        Penthouse(402, "Lotte Center Hanoi", 18.2, 280, True)
    ]

    generate_market_report(market_dashboard)
    villa_inspection(market_dashboard)

    #---------------------------- Step 6 (Sửa đổi logic tại đây) ----------------------------
    print("\n--- BEFORE RENOVATION ---")
    # Thay vì tạo object mới, ta lấy trực tiếp phần tử Villa index số 3 ra để hiển thị và nâng cấp
    market_dashboard[3].display_listing()

    # Tiến hành gọi hàm xây hồ bơi ngay trên phần tử của list
    market_dashboard[3].add_pool()

    print("\n--- AFTER RENOVATION ---")
    market_dashboard[3].display_listing()
