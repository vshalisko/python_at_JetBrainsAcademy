print("Write how many ml of water the coffee machine has:")
water = int(input())
print("Write how many ml of milk the coffee machine has:")
milk = int(input())
print("Write how many grams of coffee beans the coffee machine has:")
coffee = int(input())
print("Write how many cups of coffee you will need:")
cups = int(input())

water_cups = water // 200
milk_cups = milk // 50
coffee_cups = coffee // 15

min_cups = min([water_cups, milk_cups, coffee_cups])

if (min_cups == cups):
    print("Yes, I can make that amount of coffee")
elif (min_cups < cups):
    print("No, I can make only {} cups of coffee".format(min_cups))
else:
    print("Yes, I can make that amount of coffee (and even {} more than that)".format(min_cups - cups))
