class FoodService :
    def __init__(self, FoodDao):
        self.FoodDao = FoodDao

    def foodRecommend(self, ingredients):
        return self.FoodDao.foodRecommend(ingredients)