import json
import pandas as pd
from collections import OrderedDict

from model.JaccardSimilarity import jaccard_similarity


class FoodDao:

    def foodRecommend(self, ingredients):
        data = pd.read_csv("./dataset/ingredients.csv", encoding='cp949')
        data.head()

        result = []
        #ingredients = ingredients.split(' ')

        for index in range(0, data['id'].count() - 1) :
            list = data['food'][index].split(" ")
            a = []
            a.append(jaccard_similarity(ingredients, list))
            a.append(data['id'][index])
            a.append(data['dish'][index])
            a.append(data['food'][index])
            a.append(data['recipe_url'][index])
            result.append(a)

        result.sort(key=lambda x:-x[0])

        column_names = ["result", "id", "dish", "food", "recipe_url"]
        df = pd.DataFrame(result, index=[i for i in range(1, data['id'].count())], columns=column_names)
        foods = df.head(3)['dish'].tolist()
        recipes = df.head(3)['recipe_url'].tolist()
        jsonData = OrderedDict()
        foodDto = []
        for i in range(3) :
            object = OrderedDict()
            ing = df.head(3)['food'].tolist()[i].split(' ')
            object['food'] = foods[i]
            no = [x for x in ing if x not in ingredients]
            no = [x for x in no if x not in '']
            object['no'] = no
            has = [x for x in ingredients if x in ing]
            has = [x for x in has if x not in '']
            object['has'] = has
            object['recipeUrl'] = recipes[i]
            foodDto.append(object)
        jsonData['foods'] = foods
        jsonData['foodDto'] = foodDto

        return json.dumps(jsonData, ensure_ascii=False, indent=4)