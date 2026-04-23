from src.clients.ecb import fetch_series

data = fetch_series(dataset="EXR", key="D.USD.EUR.SP00.A", start_date="2018-01-01")

print(len(data))
print(data[:5])
