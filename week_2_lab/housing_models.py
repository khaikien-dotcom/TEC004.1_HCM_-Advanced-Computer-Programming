class Property:
    def __init__(self, prop_id, address, price_bil_vnd, sqm):
        # Validation
        if prop_id > 0 and price_bil_vnd > 0 and sqm > 0:
            self.prop_id = prop_id
            self.address = address
            self.price_bil_vnd = price_bil_vnd
            self.sqm = sqm

            print(f"--- System: [ID: {prop_id}] at [{address}] successfully constructed ---")
        else:
            print(f"--- Error: Invalid data for ID [{prop_id}] at [{address}]. Values must be positive. ---")

    # Step 2
    def display_metrics(self):
        price_per_sqm = self.price_bil_vnd / self.sqm

        print(f"ID: {self.prop_id} | Listing: {self.address} | "
              f"Price: {price_per_sqm:.3f} Billion VND / sqm")

    def is_affordable(self, budget):
        return self.price_bil_vnd <= budget

    # Step 4
    def update_price(self, new_price):
        self.price_bil_vnd = new_price

        print(f"--- System: ID [{self.prop_id}] price updated to [{new_price}]B VND ---")

    # Step 5
    def is_larger_than(self, other_property):
        return self.sqm > other_property.sqm


# ---------------- STEP 1 TEST ----------------

print("\nSTEP 1 TEST")

property_a = Property(101, "12A Cau Giay St", 4.5, 65)
property_b = Property(102, "Unknown Alley", -1.0, 0)


# ---------------- STEP 2 TEST ----------------

print("\nSTEP 2 TEST")

property_a.display_metrics()

print("Affordable under 5.0B?:", property_a.is_affordable(5.0))


# ---------------- STEP 3 TEST ----------------

print("\nSTEP 3 TEST")

mock_database = [
    Property(103, "88 Tay Ho Rd", 12.0, 120),
    Property(104, "5 Nguyen Trai", 3.2, 50),
    Property(101, "12A Cau Giay St", 4.5, 65)
]

for property_item in mock_database:
    property_item.display_metrics()


# ---------------- STEP 4 TEST ----------------

print("\nSTEP 4 TEST")

for property_item in mock_database:
    increased_price = property_item.price_bil_vnd * 1.10
    property_item.update_price(increased_price)

print("\nUpdated Metrics:")
mock_database[0].display_metrics()


# ---------------- STEP 5 TEST ----------------

print("\nSTEP 5 TEST")

tay_ho_property = mock_database[0]
nguyen_trai_property = mock_database[1]

result = tay_ho_property.is_larger_than(nguyen_trai_property)

print(f"Is ID {tay_ho_property.prop_id} larger than "
      f"ID {nguyen_trai_property.prop_id}? {result}")


# ---------------- STEP 6 TEST ----------------

print("\nSTEP 6 TEST")

sample_property = mock_database[0]

# type()
print(type(sample_property))

# dir()
print(dir(sample_property))

# __dict__
print(sample_property.__dict__)