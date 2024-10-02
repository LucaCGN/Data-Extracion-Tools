import os
import asyncio
import websockets
import json
import pandas as pd
from datetime import datetime

# Define project root and output directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
output_dir = os.path.join(project_root, 'data', 'html_feed')

# Binance WebSocket URL for the BTCUSDT ticker
ws_url = "wss://stream.binance.com:9443/ws/btcusdt@trade"

async def listen_to_binance():
    os.makedirs(output_dir, exist_ok=True)
    file_name = "binance_btcusdt_feed.csv"
    save_path = os.path.join(output_dir, file_name)
    
    data_list = []

    async with websockets.connect(ws_url) as websocket:
        print(f"Connected to {ws_url}")
        
        # Run for 5 seconds
        end_time = datetime.now().timestamp() + 5
        
        # Listen for incoming messages
        try:
            while datetime.now().timestamp() < end_time:
                message = await websocket.recv()
                data = json.loads(message)
                
                # Extract relevant information (price and timestamp)
                price = float(data.get('p'))
                timestamp = pd.to_datetime(data.get('T'), unit='ms')
                
                if price and timestamp:
                    data_list.append({'Price': price, 'Timestamp': timestamp})
                    
        except websockets.ConnectionClosed as e:
            print("Connection closed:", e)
        except Exception as e:
            print("Error occurred:", e)

    # Convert the data to a pandas DataFrame
    df = pd.DataFrame(data_list)
    
    # Save DataFrame to CSV
    df.to_csv(save_path, index=False)
    print(f"Data saved to {save_path}")

# Entry point
if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(listen_to_binance())
