import pymysql
import json
from keras.models import load_model
from keras import utils
import numpy as np
import os
import config

my_model = load_model('./trainedModel/model_trained.h5')

class FoodClassDao:
    def predictFood(self, filename):
        #databse connect
        database = pymysql.connect(host=config.HOST, user=config.USER, password=config.PASSWORD,
                                   db=config.DATABASE, charset='utf8', port=config.PORT)
        # cursor object create
        cur = database.cursor()

        food_list = []
        fl = cur.execute("SELECT * FROM food101")
        #print(">>food list (from RDS) is :")
        while (True):
            row = cur.fetchone()
            if row == None:
                break
            food_list.append(row[1])

        # Cursor obejct , Databse Connection closing
        cur.close()
        database.close()

        #print(food_list)

        print('>>uploaded filename (from USER) is : ' + filename)

        img = utils.load_img('./static/'+filename, grayscale=False, color_mode='rgb', target_size=(299,299))
        img = utils.img_to_array(img)
        img = np.expand_dims(img, axis=0)
        img /= 255.

        pred = my_model.predict(img)
        index = np.argmax(pred)

        food_list.sort()
        pred_value = food_list[index]
        print('>>classification result is  : ' +pred_value)

        if os.path.exists('./static/'+filename):
            os.remove('./static/'+filename)
            print('>>파일이 로컬에서 제거되었습니다.<<<')

        return pred_value

    def foodNutrient(self,food_type):
        # databse connect
        database = pymysql.connect(host=config.HOST, user=config.USER, password=config.PASSWORD,
                                   db=config.DATABASE, charset='utf8', port=config.PORT)
        # cursor object create
        cur = database.cursor()

        nutrientDto={}
        sql = "SELECT * FROM nutrient101 WHERE food_type = %s"
        cur.execute(sql,food_type)
        while (True):
            row = cur.fetchone()
            if row == None:
                break

            nutrientDto['name']=row[2]
            nutrientDto['capacity'] = row[3]
            nutrientDto['calory'] = row[4]
            nutrientDto['carb'] = row[5]
            nutrientDto['pro'] = row[6]
            nutrientDto['fat'] = row[7]

        #Cursor obejct , Databse Connection closing
        cur.close()
        database.close()
        return json.dumps(nutrientDto, ensure_ascii=False, indent=4)
