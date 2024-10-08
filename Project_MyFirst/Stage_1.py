pricedict = {
    "Bubblegum": 2,
    "Toffee": 0.2,
    "Ice cream": 5,
    "Milk chocolate": 4,
    "Doughnut": 2.5,
    "Pancake": 3.2
}
print("Prices:")
for x, y in pricedict.items():
  print("{}: ${}".format(x, y))
