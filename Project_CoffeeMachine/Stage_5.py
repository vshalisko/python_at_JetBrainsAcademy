machine_state = {
                 'water': 400, 
                 'milk': 540, 
                 'beans': 120, 
                 'disposables': 9, 
                 'money': 550
                }

coffee_types = {
                1:{'type':'espresso','water':250,'milk':0,'beans':16,'money':4},
                2:{'type':'latte','water':350,'milk':75,'beans':20,'money':7},
                3:{'type':'cappuccino','water':200,'milk':100,'beans':12,'money':6}
               }

def output_state (state):
    print("""
The coffee machine has:
{} ml of water
{} ml of milk
{} g of coffee beans
{} disposable cups
${} of money""".format(state.get('water'),
                       state.get('milk'),
                       state.get('beans'),
                       state.get('disposables'),
                       state.get('money')))
    return 1
def supply_test (state, coffee_type):
    water_cups = state.get('water') // coffee_type['water']
    beans_cups = state.get('beans') // coffee_type['beans']
    if (coffee_type['milk'] == 0):
        required_supplies = ['water','beans','disposables']
        available_supplies = [water_cups, beans_cups, state.get('disposables')]
    else:
        milk_cups = state.get('milk') // coffee_type['milk']
        required_supplies = ['water','milk','beans','disposables']
        available_supplies = [water_cups, milk_cups, beans_cups, state.get('disposables')]
    min_cups = min(available_supplies)
    if (min_cups >= 1):
        return('ok')
    else:
        limiting_supply_index = available_supplies.index(min(available_supplies))
        return(required_supplies[limiting_supply_index])

while 1:
    print("\nWrite action (buy, fill, take, remaining, exit):")
    action = str(input())
    if (action == 'take'):
        print("I gave you ${}".format(machine_state.get('money')))
        machine_state.update({'money':0})
    elif (action == 'remaining'):
        output_state(machine_state)
    elif (action == 'fill'):
        print("Write how many ml of water you want to add:")
        add_water = int(input())
        print("Write how many ml of milk you want to add: :")
        add_milk = int(input())
        print("Write how many grams of coffee beans you want to add:")
        add_beans = int(input())
        print("Write how many disposable cups you want to add:")
        add_disposables = int(input())
        machine_state.update({'water':machine_state.get('water') + add_water,
                          'milk':machine_state.get('milk') + add_milk,
                          'beans':machine_state.get('beans') + add_beans,
                          'disposables':machine_state.get('disposables') + add_disposables})
    elif (action == 'buy'):
        print("What do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino, back - to main menu:")
        type = str(input())
        if (type == 'back'):
            pass
        else:
            type = int(type)
            test = supply_test(machine_state, coffee_types[type])
            if (test == 'ok'):
                print("I have enough resources, making you a coffee!")
                machine_state.update({'money':machine_state.get('money') + coffee_types[type]['money'],
                         'water':machine_state.get('water') - coffee_types[type]['water'],
                         'milk':machine_state.get('milk') - coffee_types[type]['milk'],
                         'beans':machine_state.get('beans') - coffee_types[type]['beans'],
                         'disposables':machine_state.get('disposables') - 1})
            else:
                print('Sorry, not enough {}!'.format(test))
    elif (action == 'exit'):
        break
