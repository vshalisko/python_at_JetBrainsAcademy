import json
import requests

def currency_search(cur):
    r = requests.get("http://www.floatrates.com/daily/{}.json".format(cur))
    return r.text

my_currency = str(input()).lower()

exchange_file = currency_search(my_currency)
exhange_dist = json.loads(exchange_file)

currency_cache = dict()

if my_currency != "usd":
    currency_cache["usd"] = exhange_dist["usd"]["rate"]
if my_currency != "eur":
    currency_cache["eur"] = exhange_dist["eur"]["rate"]

while True:
    target = str(input())
    if target == "":
        break
    target = target.lower()
    amount = float(input())
    print("Checking the cache...")
    if target in currency_cache.keys():
        print("Oh! It is in the cache!")
    else:
        print("Sorry, but it is not in the cache!")
        currency_cache[target] = exhange_dist[target]["rate"]
    target_amount = currency_cache[target] * amount
    print("You received {} {}.".format(round(target_amount, 2), target.upper()))
