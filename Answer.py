import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests
from PIL import Image, ImageOps

api = "CG-BdZ9akMpLNMWEqqXfFL6kw1R"

key= {
    "accept": "application/json",
    "x-cg-demo-api-key": api
}

def get_historical_data(coin_id, days):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
    params = {
        "vs_currency": "usd",
        "days": days
    }
    response = requests.get(url, headers=key, params=params)
    data = response.json()
    
    try:
        prices = data['prices']
        df = pd.DataFrame(prices, columns=['timestamp', 'price'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        return df
    except KeyError:
        print("erro")
        print("Response data:", data)
        return None

def get_coin_id(coin_name):
    try:
        url = "https://api.coingecko.com/api/v3/coins/list"
        response = requests.get(url, headers=key)
        response.raise_for_status()
        coins = response.json()
        
        if isinstance(coins, list):
            for coin in coins:
                if isinstance(coin, dict) and 'name' in coin:
                    if coin['name'].lower() == coin_name.lower():
                        return coin['id']
        return None
    except requests.exceptions.RequestException as e:
        print("erro")
        print("Error message:", e)
        return None
    except KeyError:
        print("erro")
        return None

def stock_details_app():
    
    st.title('Crypto App')

    coin_name = st.text_input('Bitcoin')

    if coin_name:
        coin_id = get_coin_id(coin_name)
        if coin_id:
            st.write(f"{coin_name}")
            data = get_historical_data(coin_id, 365)
            
            if data is not None:
                st.subheader('Chart')
                plt.figure(figsize=(10, 6))
                plt.plot(data['timestamp'], data['price'])
                plt.title(f'{coin_name} Last Year')
                plt.xlabel('Date')
                plt.ylabel('Price')
                st.pyplot(plt)
                
                st.subheader('Details')
                st.write(f"Maximum Price: {data['price'].max():.2f}")
                st.write(f"Minimum Price: {data['price'].min():.2f}")
                max_date = data.loc[data['price'].idxmax()]['timestamp'].strftime('%Y-%m-%d')
                min_date = data.loc[data['price'].idxmin()]['timestamp'].strftime('%Y-%m-%d')
                st.write(f"Maximum Price: {max_date}")
                st.write(f" Minimum Price: {min_date}")
            else:
                st.error("error.")
   

def get_comparison_data(coin1_id, coin2_id, days):
    data1 = get_historical_data(coin1_id, days)
    data2 = get_historical_data(coin2_id, days)
    return data1, data2

def coin_comparison_app():
    print("hello")

    st.title('Coin Comparison App')

    coin1_name = st.text_input('first cryptocurrency name (e.g., Bitcoin):')
    coin2_name = st.text_input('second cryptocurrency name (e.g., Bitcoin):')
    time_frame = st.selectbox('Select time frame:', ['1 week', '1 month', '1 year', '5 years'])

    if coin1_name and coin2_name:
        coin1_id = get_coin_id(coin1_name)
        coin2_id = get_coin_id(coin2_name)
        if coin1_name and coin2_name:
            st.write(f"Let me do some undercover work on {coin1_name} and {coin2_name}...")
            if time_frame == '1 week':
                days = 7
            elif time_frame == '1 month':
                days = 30
            elif time_frame == '1 year':
                days = 365
            elif time_frame == '5 years':
                days = 1825  

            data1, data2 = get_comparison_data(coin1_id, coin2_id, days)

            if data1 is not None and data2 is not None:
                st.subheader('Chart')
                plt.figure(figsize=(10, 6))
                plt.plot(data1['timestamp'], data1['price'], label=coin1_name)
                plt.plot(data2['timestamp'], data2['price'], label=coin2_name)
                plt.title(f'{coin1_name} vs {coin2_name} Price Comparison')
                plt.xlabel('Date')
                plt.ylabel('Price (USD)')
                plt.legend()
                st.pyplot(plt)

               
                for coin_name, data in zip([coin1_name, coin2_name], [data1, data2]):
                    st.markdown(f"{coin_name}")
                    st.write(f"*Maximum Price:* ${data['price'].max():.2f}")
                    st.write(f"*Minimum Price:* ${data['price'].min():.2f}")
                    max_date = data.loc[data['price'].idxmax()]['timestamp'].strftime('%Y-%m-%d')
                    min_date = data.loc[data['price'].idxmin()]['timestamp'].strftime('%Y-%m-%d')
                    st.write(f"Maximum Price:* {max_date}")
                    st.write(f"Minimum Price:* {min_date}")
                   
            else:
                st.error(" Try again")
        else:
            st.error("not a valid names.")
            
def image():
    print("hello")
    uploaded_file = st.file_uploader("Choose an image of", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)


def main():
    st.sidebar.title("Index")
    app_selection = st.sidebar.radio(
        "Choose an app:",
        ("Stock Details", "Coin Comparison", "Image Identifier")
    )

    if app_selection == "Stock Details":
        stock_details_app()
    elif app_selection == "Coin Comparison":
        coin_comparison_app()
    elif app_selection == "Image Identifier":
        image()

if __name__ == "__main__":
    main()
