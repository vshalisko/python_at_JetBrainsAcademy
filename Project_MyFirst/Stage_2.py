pricedict = {
    "Bubblegum": 202,
    "Toffee": 118,
    "Ice cream": 2250,
    "Milk chocolate": 1680,
    "Doughnut": 1075,
    "Pancake": 80
}
print("Earned ammount:")
earnings = 0
for x, y in pricedict.items():
  earnings += y
  print("{}: ${}".format(x, y))
print("/nIncome: ${}".format(earnings))
