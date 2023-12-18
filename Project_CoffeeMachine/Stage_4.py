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
    print("""The coffee machine has:
{} ml of water
{} ml of milk
{} g of coffee beans
{} disposable cups
${} of money
""".format(state.get('water'),
                       state.get('milk'),
                       state.get('beans'),
                       state.get('disposables'),
                       state.get('money')))
    return 1

output_state(machine_state)

print("Write action (buy, fill, take):")
action = str(input())
if (action == 'take'):
    print("I gave you ${}".format(machine_state.get('money')))
    machine_state.update({'money':0})
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
    print("What do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino:")
    type = int(input())
    machine_state.update({'money':machine_state.get('money') + coffee_types[type]['money'],
                         'water':machine_state.get('water') - coffee_types[type]['water'],
                         'milk':machine_state.get('milk') - coffee_types[type]['milk'],
                         'beans':machine_state.get('beans') - coffee_types[type]['beans'],
                         'disposables':machine_state.get('disposables') - 1})

print("")
output_state(machine_state)
