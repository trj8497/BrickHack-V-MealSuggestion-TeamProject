import requests
import json

"""
BrickHack-V
Recipe.py
Requests information from Wegmans' API and manipulating to gather data and
building relevant tables. 

@authors: Jiwoo Baik - jxb4892@rit.edu
          Tejaswini Jagtap - trj8497@rit.edu
          Himani Munshi - hxm3443@rit.edu  
"""

# Static fields
URL = "https://api.wegmans.io/meals/recipes"
PAYLOAD = ""
HEADERS = {
    'cache-control': "no-cache",
    'Postman-Token': "69dac8cb-b0b0-4a8c-978f-5b06cc2c71f7"
}

def get_recipes():
    """
    requests and gets data from Wegmans' API and loads to json
    :return: dictionary of all of the recipes' concise information
    """
    querystring = {"api-version": "2018-10-18", "Subscription-Key": "5558cf6b1b6140f0971d8df7369d524b"}
    response = requests.request("GET", URL, data=PAYLOAD, headers=HEADERS, params=querystring)
    recipes = response.text
    recipe_dict = json.loads(recipes)

    return recipe_dict

def open_recipe(dict, num):
    """
    requests information of a specific recipe
    :param dict: dictionary of all the recipes' concise information
    :param num: which recipe to request info from
    :return: a dictionary of a specific recipe
    """
    querystring = {"Subscription-Key": "5558cf6b1b6140f0971d8df7369d524b"}
    list1 = dict['recipes']
    query = list1[num]
    link = query['_links']
    href = link[0]['href']
    response = requests.request(link[0]['type'], 'https://api.wegmans.io'+href, data=PAYLOAD, headers=HEADERS, params=querystring)
    detail = response.text
    recipe = json.loads(detail)

    return recipe



def generate_table(recipe, sku_recipes, sku_name, name_link):
    """
    generates three dictionaries: a dictionary with product ID as a key and list of recipes that contains its key as
    one of the ingredients, a dictionary mapping a product ID and its name, and a dictionary mapping a recipe to a link where
    a recipe can be found.
    :param recipe: dictionary containing information of a single recipe
    :param sku_recipes: dictionary with product ID and list of recipes
    :param sku_name: dictionary mapping a product ID and its name
    :param name_link: dictionary mapping a recipe to a link where a recipe can be found
    """
    lst = recipe['_links']
    name_link[recipe['name']] = lst[1]
    for smalld in recipe['ingredients']:
        if 'sku' not in smalld:
            continue
        if smalld['name'] not in sku_name.keys():
            sku_name[smalld['name']] = smalld['sku']
        else:
            continue
        if smalld['sku'] not in sku_recipes.keys():
            sku_recipes[smalld['sku']] = [recipe['name']]
        else:
            sku_recipes[smalld['sku']].append(recipe['name'])