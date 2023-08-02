

def calculate_buying_price(floor_price, floor):
    # Assuming floor ranges from -2 to 7 (-2 for LG, -1 for UG, and 0-5 for 1st to 6th floors)
    if floor == -2:
        sqft_price = floor_price['LG']
    elif floor == -1:
        sqft_price = floor_price['UG']
    else:
        sqft_price = floor_price[floor]
    return sqft_price

def main():
    try:
        floor_prices = {
            'LG': 13000,
            'UG': 15000,
            0: 12000, #1st floor
            1: 11000, #2nd floor
            2: 11000,
            3: 15000,
            4: 11000
        }

        floor = int(input("Enter the floor you want to buy (-2 for LG, -1 for UG, 0-5 for 1st to 6th floors): "))
        sqft_to_buy = float(input("Enter the square feet you want to buy: "))
        estimated_rent = float(input("Enter the estimated rent for that floor (per month): "))

        sqft_price = calculate_buying_price(floor_prices, floor)
        buying_price = sqft_to_buy * sqft_price
        rent = sqft_to_buy * estimated_rent

        print(f"\nBuying price for floor {floor}: ${buying_price:.2f}")
        print(f"Estimated rent for floor {floor}: ${rent:.2f}")

    except ValueError:
        print("Invalid input. Please enter valid numeric values for floor, square feet, and rent rate.")

if __name__ == "__main__":
    main()
