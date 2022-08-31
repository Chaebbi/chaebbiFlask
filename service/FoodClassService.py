
class FoodClassService:
    def __init__(self, FoodClassDao):
        self.FoodClassDao = FoodClassDao

    def predictFood(self, filename):
        return self.FoodClassDao.predictFood(filename)

    def foodNutrient(self,food_type):
        return self.FoodClassDao.foodNutrient(food_type)
