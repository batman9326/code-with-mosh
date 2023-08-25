import yfinance as yf
import datetime

# Ticker symbol
ticker = input("Enter the ticker symbol: ")

# Investment date (YYYY-MM-DD)
#investment_date_str = input("Enter the investment date (YYYY-MM-DD): ")
investment_date_str = "2023-01-01"
investment_date = datetime.datetime.strptime(investment_date_str, "%Y-%m-%d")

# Initial investment amount
#initial_investment = float(input("Enter the initial investment amount: "))
initial_investment = float("10000")

# Current date
current_date = datetime.datetime.today()

# Fetch historical data
data = yf.download(ticker, start=investment_date, end=current_date)

# Calculate profits/loss
investment_price = data['Open'].iloc[0]
current_price = data['Close'].iloc[-1]

investment_value = (initial_investment / investment_price) * current_price
profit_loss = investment_value - initial_investment
profit_loss_percentage = (profit_loss / initial_investment) * 100

# Print results
print(f"Investment Date: {investment_date.date()}")
print(f"Current Date: {current_date.date()}")
print(f"Initial Investment: ${initial_investment:.2f}")
print(f"Initial Price: ${investment_price:.2f}")
print(f"Current Price: ${current_price:.2f}")
print(f"Current Investment Value: ${investment_value:.2f}")
print(f"Profit/Loss: ${profit_loss:.2f}")
print(f"Profit/Loss: ${profit_loss:.2f} ({profit_loss_percentage:.2f}%)")
