## magine you are having dinner in a very fancy restaurant, but unfortunately you don't have a lot of money with you. 
## You want to have a main course, a dessert and a drink, but all that together shouldn't cost more than $30.
## Consider each possible combination of a main course, dessert and a drink from those offered by the restaurant 
## and print out only those meals that satisfy your budget, along with their total costs.

import itertools

main_courses = ['beef stew', 'fried fish']
price_main_courses = [28, 23]

desserts = ['ice-cream', 'cake']
price_desserts = [2, 4]

drinks = ['cola', 'wine']
price_drinks = [3, 10]

for first, second, third in itertools.product(zip(main_courses, price_main_courses),
                                              zip(desserts, price_desserts),
                                              zip(drinks, price_drinks)):
    (first_t, first_p) = tuple(first)
    (second_t, second_p) = tuple(second)
    (third_t, third_p) = tuple(third)
    total = first_p + second_p + third_p
    if total <= 30:
        print("{} {} {} {}".format(first_t, second_t, third_t, total))
