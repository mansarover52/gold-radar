import yfinance as yf
import datetime
import math

ticker = yf.Ticker("GOLDBEES.NS")
hist = ticker.history(period="1mo")
closes = hist['Close'].tolist()[-20:]

if len(closes) < 20:
    exit()

currentPrice = closes[-1]
prev2Price = closes[-3]
twoDayDrop = ((currentPrice - prev2Price) / prev2Price) * 100

period = 5
gains, losses = 0, 0
for i in range(len(closes) - period, len(closes)):
    diff = closes[i] - closes[i - 1]
    if diff >= 0:
        gains += diff
    else:
        losses -= diff

avgGain = gains / period
avgLoss = losses / period
rsi5 = 100 if avgLoss == 0 else 100 - (100 / (1 + (avgGain / avgLoss)))

sma20 = sum(closes) / 20
variance = sum([math.pow(x - sma20, 2) for x in closes]) / 20
lowerBand = sma20 - (1.8 * math.sqrt(variance))

dayOfMonth = datetime.datetime.now().day

isStrongBuy = (rsi5 < 28 and currentPrice <= lowerBand * 1.008) or (twoDayDrop <= -1.8 and rsi5 < 35)
isAccumulate = (rsi5 < 38 or currentPrice < sma20) or (dayOfMonth >= 28 and currentPrice <= sma20 * 1.01)

if isStrongBuy:
    signal_text = "BUY"
elif isAccumulate:
    signal_text = "ACCUM"
else:
    signal_text = "WAIT"

with open("gold.txt", "w") as f:
    f.write(str(round(currentPrice, 2)))

with open("signal.txt", "w") as f:
    f.write(signal_text)
