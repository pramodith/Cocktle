import json
import pandas as pd
import requests
import time
import shutil

def get_all_cocktails(url):
    names = []
    try:
        for i in range(97,123):
            response = requests.get(url,params={"f":chr(i)})
            if response.status_code == 200:
                json_body = response.json()
            else:
                raise Exception(f"API responded with non 200 status code {response.status_code}")
            if json_body and json_body["drinks"]:
                for drink in json_body["drinks"]:
                    if drink["strAlcoholic"] == "Alcoholic":
                        names.append(drink["strDrink"])
            #time.sleep(5)

    except Exception as e:
        print(e)
        return False

    df = pd.DataFrame(data=names,columns=["Cocktails"])
    df.to_csv("cocktail_drinks.csv",index=False)
    return True

def get_all_ingredients_cocktails(url):
    ingredients = []
    cocktails = pd.read_csv("../../data/cocktail_drinks.csv")

    try:
        for cocktail in cocktails["Cocktails"]:
            ingredients.append([])
            response = requests.get(url,params={"s": cocktail})
            if response.status_code == 200:
                json_body = response.json()
            else:
                raise Exception(f"API responded with non 200 status code {response.status_code}")
            if json_body and json_body["drinks"]:
                for drink in json_body["drinks"]:
                    img_response = requests.get(drink["strDrinkThumb"], stream=True)
                    with open(f"../../data/images/{cocktail}.png", 'wb') as out_file:
                        shutil.copyfileobj(img_response.raw, out_file)
                    del img_response
                    if drink["strDrink"] == cocktail:
                        for i in range(15):
                            if drink["strIngredient"+str(i+1)]!=None:
                                ingredients[-1].append(drink["strIngredient"+str(i+1)])
                            else:
                                break

    except Exception as e:
        print(e)
        return False

    ingredients = ["|".join(i) for i in ingredients]
    print(len(ingredients),len(cocktails["Cocktails"].values))
    df = pd.DataFrame(data=list(zip(cocktails["Cocktails"].tolist(),ingredients)),columns=["Cocktails","Ingredients"])
    df.to_csv("cocktail_ingredients.csv",index=False)
    return True

if __name__ == "__main__":
    get_all_ingredients_cocktails("https://www.thecocktaildb.com/api/json/v1/1/search.php")