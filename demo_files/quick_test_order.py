from order_engine import OrderEngine

engine = OrderEngine(fund=1000)

print("Buying @ 100:", engine.process(True, 100))
print("Selling @ 110:", engine.process(False, 110))
