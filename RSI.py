import yfinance as yf
import pandas as pd
import os
import schedule
import time
import pywhatkit

# Function to fetch historical stock data and save it to CSV
def fetch_stock_data(stock_name):
    try:        
        file_name = f"{stock_name}_data.csv"
        stock = yf.Ticker(stock_name+".NS")
        
        # Fetch historical data for the past 1 year (including today)
        new_data = stock.history(period="1y")
        
        if os.path.exists(file_name):
            # Read existing data
            old_data = pd.read_csv(file_name, index_col='Date', parse_dates=True)
            
            # Concatenate old and new data, removing duplicates
            data = pd.concat([old_data, new_data])
            data = data[~data.index.duplicated(keep='last')]  # Keep the latest entry for each date
            print("file updated!")        
        else:
            data = new_data
        
        # Delete unused columns
        data = data.drop(columns=['Dividends', 'Volume', 'Stock Splits'], errors='ignore')
        
        temp_close = list(data['Close'])
        
        data['Gain'] = get_gain(temp_close)
        data['Loss'] = get_loss(temp_close)
        
        # Calculate RSI-related columns
        temp_gain = list(data['Gain'])
        data['Average Gain in last 14 days'] = get_avg_14days_gain(temp_gain)

        temp_loss = list(data['Loss'])
        data['Average Loss in last 14 days'] = get_avg_14days_loss(temp_loss)

        avg_gain = list(data['Average Gain in last 14 days'])
        avg_loss = list(data['Average Loss in last 14 days'])
        data['RS'] = get_rs(avg_gain, avg_loss)

        rs = list(data['RS'])
        data['RSI'] = get_RSI(rs)

        # Save the updated data to CSV
        data.to_csv(file_name)

        #generating indication to send the msg
        indication(data)

        print(f"indication generated for {stock_name}")
        print(f'''Historical data for {stock_name} saved to "{file_name}"''')

    except Exception as e:
        print(f"An error occurred: {e}")

# Calculate gain
def get_gain(close):
    gain = ["#"]
    for i in range(len(close) - 1):
        if close[i + 1] > close[i]:
            gain.append(close[i + 1] - close[i])
        else:
            gain.append(0)
    return gain

# Calculate loss
def get_loss(close):
    loss = ["#"]
    for i in range(len(close) - 1):
        if close[i + 1] < close[i]:
            loss.append(close[i] - close[i + 1])
        else:
            loss.append(0)
    return loss

# Calculate average gain in the last 14 days
def get_avg_14days_gain(gain):
    avg_gain_in_14days = ["#"] * 14
    ls = gain[1:15]
    average = sum(ls) / len(ls)
    avg_gain_in_14days.append(average)
    for i in range(15, len(gain)):
        temp = ((avg_gain_in_14days[i - 1] * 13) + gain[i]) / 14
        avg_gain_in_14days.append(temp)
    return avg_gain_in_14days

# Calculate average loss in the last 14 days
def get_avg_14days_loss(loss):
    avg_loss_in_14days = ["#"] * 14
    ls = loss[1:15]
    average = sum(ls) / len(ls)
    avg_loss_in_14days.append(average)
    for i in range(15, len(loss)):
        temp = ((avg_loss_in_14days[i - 1] * 13) + loss[i]) / 14
        avg_loss_in_14days.append(temp)
    return avg_loss_in_14days

# Calculate RS
def get_rs(avg_gain, avg_loss):
    rs = ["#"] * 14
    for i in range(14, len(avg_gain)):
        rs.append(avg_gain[i] / avg_loss[i] if avg_loss[i] != 0 else 0)
    return rs

# Calculate RSI
def get_RSI(rs):
    rsi = ["#"] * 14
    for i in range(14, len(rs)):
        temp = (100 - (100 / (1 + rs[i]))) if rs[i] != 0 else 100
        rsi.append(temp)
    
    return rsi 

# Schedule the task to update stock data daily @ 4 pm
def schedule_task(stock_name):
    schedule.every().day.at("16:00").do(fetch_stock_data, stock_name=stock_name)

    while True:
        schedule.run_pending()
        time.sleep(1)  # Wait a second between each check

# generating indication to send the msg
def indication(data):

    rsi_data = data['RSI'].tolist()    
    close_data = data['Close'].tolist()
    current_RSI = rsi_data[-1]
    closing_price = close_data[-1]
    buy = 35
    sell = 65
    if(current_RSI < buy):
        indicator_msg = f"*{stock_name}*\n *RSI* : {current_RSI:.2f} \n can Buy @ *{closing_price:.2f}*"
        buy = buy - 5
    elif(current_RSI > sell):
        indicator_msg = f"*{stock_name}*\n *RSI* : {current_RSI:.2f} \n can Sell @ *{closing_price:.2f}*"
        sell = sell + 5
    else :
        indicator_msg = f"*{stock_name}*\n *RSI* : {rsi_data[-1]:.2f} \n stock in mid range (can Hold)"

    if(current_RSI > 50):
        buy = 35
    if(current_RSI < 50):
        sell = 65

    pywhatkit.sendwhatmsg_instantly("+918328504861",indicator_msg)


#main
stock_name = input("Enter the stock symbol: ").upper()
fetch_stock_data(stock_name)
schedule_task(stock_name)
