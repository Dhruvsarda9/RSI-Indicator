# import yfinance as yf
# import pandas as pd
# import os
# import schedule
# import time

# # Function to fetch historical stock data and save it to CSV
# def fetch_stock_data(stock_name):
#     try:        
#         file_name = f"{stock_name}_data.csv"

#         new_data = stock.history(period="1y")
        
#         if os.path.exists(file_name):
#             # Read existing data
#             old_data = pd.read_csv(file_name, index_col='Date', parse_dates=True)
            
#             # Concatenate old and new data, removing duplicates
#             data = pd.concat([old_data, new_data])
#             data = data[~data.index.duplicated(keep='last')]  # Keep the latest entry for each date

#         else:
#             stock = yf.Ticker(stock_name)

#             # Fetch historical data for the past 1 year
#             data = stock.history(period="1y")

#         # deleting unused columns
#         data = data.drop(columns=['Dividends','Volume', 'Stock Splits'], errors='ignore')
       
#         temp_close = list(data['Close'])
        
#         data['Gain'] = get_gain(temp_close)
#         data['Loss'] = get_loss(temp_close)
        
#         # print("gain and loss column inserted")

#         temp_gain = list(data['Gain'])
        
#         data['Average Gain in last 14 days'] = get_avg_14days_gain(temp_gain)

#         # print("avg 14 day gain column inserted")

#         temp_loss = list(data['Loss'])
#         data['Average Loss in last 14 days'] = get_avg_14days_gain(temp_loss)

#         # print("avg 14 day loss column inserted")

#         avg_gain = list(data['Average Gain in last 14 days'])
#         avg_loss = list(data['Average Loss in last 14 days'])
#         data['RS'] = get_rs(avg_gain,avg_loss)

#         rs = list(data['RS'])
#         data['RSI'] = get_RSI(rs)

#         # Save data to CSV
#         data.to_csv(file_name)
#         # print(data)
#         print(f"Historical data for {stock_name} saved to {file_name}")
#     except Exception as e:
#         print(f"An error occurred: {e}")

# #calculate gain
# def get_gain(close):
#     gain = ["#"]
#     for i in range(0,len(close)-1):
#         if(close[i+1] > close[i]):
#             gain.append(close[i+1] - close[i])
#         else:
#             gain.append(0)
#     return gain

# #calculate loss
# def get_loss(close):
#     loss = ["#"]
#     for i in range(len(close)-1):
#         if(close[i+1] < close[i]):
#             loss.append(close[i] - close[i+1])
#         else:
#             loss.append(0)
#     return loss

# #calculate averageof gain in last 14 days
# def get_avg_14days_gain(gain):
#     avg_gain_in_14days = ["#","#","#","#","#","#","#","#","#","#","#","#","#","#"]
#     ls = gain[1:15]
#     average = sum(ls)/len(ls)
#     avg_gain_in_14days.append(average)
#     for i in range(15,len(gain)):
#         temp = ((avg_gain_in_14days[i-1]*13)+gain[i])/14
#         avg_gain_in_14days.append(temp)
#     # print(avg_gain_in_14days)
#     return avg_gain_in_14days

# #calculate average of loss in last 14 days
# def get_avg_14days_loss(loss):
#     avg_loss_in_14days = ["#","#","#","#","#","#","#","#","#","#","#","#","#","#"]
#     ls = loss[1:15]
#     average = sum(ls)/len(ls)
#     avg_loss_in_14days.append(average)
#     for i in range(15,len(loss)):
#         temp = ((avg_loss_in_14days[i-1]*13)+loss[i])/14
#         avg_loss_in_14days.append(temp)
#     # print(avg_gain_in_14days)
#     return avg_loss_in_14days

# #calculate RS 
# def get_rs(avg_gain,avg_loss):
#     rs = ["#","#","#","#","#","#","#","#","#","#","#","#","#","#"]
#     for i in range(14,len(avg_gain)):
#         # print(avg_gain[i] ) 
#         # print(avg_loss[i])
#         rs.append(avg_gain[i]/avg_loss[i])
#     return rs

# #calculate RSI
# def get_RSI(rs):
#     rsi = ["#","#","#","#","#","#","#","#","#","#","#","#","#","#"]
#     for i in range(14,len(rs)):
#         temp = (100 - (100/(1+rs[i])))
#         rsi.append(temp)
#     return rsi 

# # updating the file
# def schedule_task(stock_name):
#     schedule.every().day.at("23:45").do(fetch_stock_data, stock_name=stock_name)

#     while True:
#         schedule.run_pending()
#         time.sleep(1)  # Wait a second between each check

# stock_name = input("Enter the stock symbol (e.g., AAPL for Apple): ").upper()
# stock = stock_name+".NS"
# fetch_stock_data(stock)
# schedule_task(stock)



import yfinance as yf
import pandas as pd
import os
import schedule
import time

# Function to fetch historical stock data and save it to CSV
def fetch_stock_data(stock_name):
    try:        
        file_name = f"{stock_name}_data.csv"
        stock = yf.Ticker(stock_name)
        
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
        print(f"Historical data for {stock_name} saved to {file_name}")
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

# Schedule the task to update stock data daily
def schedule_task(stock_name):
    schedule.every().day.at("16:00").do(fetch_stock_data, stock_name=stock_name)

    while True:
        schedule.run_pending()
        time.sleep(1)  # Wait a second between each check

stock_name = input("Enter the stock symbol (e.g., AAPL for Apple): ").upper()
stock = stock_name + ".NS"
fetch_stock_data(stock)
schedule_task(stock)
