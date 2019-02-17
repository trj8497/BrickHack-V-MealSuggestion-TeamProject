import Recipe

"""
BrickHack-V
Main.py
Using Wegmans' API, dev.wegmans.io, MealSuggestion provides recipes based on user's desired ingredients. 
To run, JSON and Python requests libraries are required. 

@authors: Jiwoo Baik - jxb4892@rit.edu
          Tejaswini Jagtap - trj8497@rit.edu
          Himani Munshi - hxm3443@rit.edu        
"""

def prettyprint(rep_link_table, rep_list):
    """
    Pretty prints the output showing the names of the recipes with their respective links (shows the most relevant
    recipes first, according to the user inputs).
    :param rep_link_table: a dictionary containing (recipe name, link) as (key, value)
    :param rep_list: list of recipes to be displayed
    """
    if rep_list == []:
        print("We're Sorry 😭")
        print("Do you have anything else in mind?")
    else:
        print("Here are some ideas... 🤤")
        for rep in rep_list:
            print('🍽'+rep)
            print(rep_link_table[rep]['href'])

def main():
    """
    This function is responsible for getting all the recipes that have been parsed from the Recipe.py file and then
    generating three dictionaries: a dictionary with product ID as a key and list of recipes that contains its key as
    one of the ingredients, a dictionary mapping a product ID and its name, and a dictionary mapping a recipe to a link where
    a recipe can be found. Gets the recipes with given conditions (user's ingredients inputs) and then sort it to
    display it
    """
    rep_dict = Recipe.get_recipes()
    sku_recipes = {}
    sku_name = {}
    recipe_name_link = {}

    for i in range(0, 25): # len(rep_dict['recipes']) to look through all the available recipes (2nd parameter)
        oneR = Recipe.open_recipe(rep_dict, i)
        Recipe.generate_table(oneR, sku_recipes, sku_name, recipe_name_link)

    user_input = input('What you got? (separate ingridients by comma[,] /"q" to quit): ')

    while not(user_input == 'q'):
        inputs = user_input.split(",")
        recipeNames = []

        # finding the products according to user inputs
        # and building a list of recipes including
        # products as ingredients
        for inp in inputs:
            for key in sku_name.keys():
                if inp.lower() in key.lower():
                    product = sku_name[key]
                    recipeNames += sku_recipes[product]
                else:
                    continue

        # sorting the recipes in the order of
        # relevancy.
        # Meaning that the more user input ingredients
        # a recipe has, the more relevant it gets.
        recipeFrq = {}
        for rep in recipeNames:
            if rep not in recipeFrq.keys():
                recipeFrq[rep] = 1
            else:
                recipeFrq[rep] += 1

        lst = []
        for count in recipeFrq.values():
            lst.append(count)
        lst = sorted(lst, reverse=True)

        ordered_recipes = []
        for each_freq in lst:
            for elt in recipeFrq.keys():
                if each_freq == recipeFrq[elt] and elt not in ordered_recipes:
                    ordered_recipes.append(elt)

        prettyprint(recipe_name_link, ordered_recipes)
        print()

        user_input = input('What you got? (separate ingridients by comma[,] /"q" to quit): ')

if __name__=='__main__':
    main()