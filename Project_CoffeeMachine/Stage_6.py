class CoffeeMachine:
    def __init__(self):
        self.machine_state = {
                 'water': 400, 
                 'milk': 540, 
                 'beans': 120, 
                 'disposables': 9, 
                 'money': 550
                }
        self.coffee_types = {
                 1:{'type':'espresso','water':250,'milk':0,'beans':16,'money':4},
                 2:{'type':'latte','water':350,'milk':75,'beans':20,'money':7},
                 3:{'type':'cappuccino','water':200,'milk':100,'beans':12,'money':6}
                }

    def main(self):
        while True:
            action = input("Write action (buy, fill, take, remaining, exit):\n")
            if action == 'exit':
                break
            else:
                self.handle_action(action)

    def handle_action(self, action):
        if action == 'remaining':
            self.output_state()
        elif action == 'take':
            self.take_money()   
        elif action == 'buy':
            self.buy_coffee()
        elif action == 'fill':
            self.fill_machine()
 



    def output_state (self):
        print("""
The coffee machine has:
{} ml of water
{} ml of milk
{} g of coffee beans
{} disposable cups
${} of money""".format(self.machine_state.get('water'),
                       self.machine_state.get('milk'),
                       self.machine_state.get('beans'),
                       self.machine_state.get('disposables'),
                       self.machine_state.get('money')))

    def take_money (self):
        print("I gave you ${}".format(self.machine_state.get('money')))
        self.machine_state.update({'money':0})

    def fill_machine (self):
        print("Write how many ml of water you want to add:")
        add_water = int(input())
        print("Write how many ml of milk you want to add: :")
        add_milk = int(input())
        print("Write how many grams of coffee beans you want to add:")
        add_beans = int(input())
        print("Write how many disposable cups you want to add:")
        add_disposables = int(input())
        self.machine_state.update({'water':self.machine_state.get('water') + add_water,
                          'milk':self.machine_state.get('milk') + add_milk,
                          'beans':self.machine_state.get('beans') + add_beans,
                          'disposables':self.machine_state.get('disposables') + add_disposables})        

    def buy_coffee (self):
        print("What do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino, back - to main menu:")
        type = str(input())
        if (type == 'back'):
            pass
        else:
            type = int(type)
            test = self.supply_test(type)
            if (test == 'ok'):
                print("I have enough resources, making you a coffee!")
                self.machine_state.update({
                            'money':self.machine_state.get('money') + self.coffee_types[type]['money'],
                            'water':self.machine_state.get('water') - self.coffee_types[type]['water'],
                            'milk':self.machine_state.get('milk') - self.coffee_types[type]['milk'],
                            'beans':self.machine_state.get('beans') - self.coffee_types[type]['beans'],
                            'disposables':self.machine_state.get('disposables') - 1
                })
            else:
                print('Sorry, not enough {}!'.format(test))      
    
    def supply_test (self, type):
        coffee_type = self.coffee_types[type]
        water_cups = self.machine_state.get('water') // coffee_type['water']
        beans_cups = self.machine_state.get('beans') // coffee_type['beans']
        if (coffee_type['milk'] == 0):
            required_supplies = ['water','beans','disposables']
            available_supplies = [water_cups, beans_cups, self.machine_state.get('disposables')]
        else:
            milk_cups = self.machine_state.get('milk') // coffee_type['milk']
            required_supplies = ['water','milk','beans','disposables']
            available_supplies = [water_cups, milk_cups, beans_cups, self.machine_state.get('disposables')]
        min_cups = min(available_supplies)
        if (min_cups >= 1):
            return('ok')
        else:
            limiting_supply_index = available_supplies.index(min(available_supplies))
            return(required_supplies[limiting_supply_index])

if __name__ == '__main__':
    CoffeeMachine().main()
