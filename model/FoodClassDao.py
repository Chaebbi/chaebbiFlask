import pymysql
import json
from keras.models import load_model
from keras import utils
import numpy as np
import os
import config

#my_model = load_model('./trainedModel/model_trained.h5')   #food101
my_model = load_model('./trainedModel/trained_model.h5')    #모델 교체

class FoodClassDao:
    def predictFood(self, filename):
        #databse connect
        database = pymysql.connect(host=config.HOST, user=config.USER, password=config.PASSWORD,
                                   db=config.DATABASE, charset='utf8', port=config.PORT)
        # cursor object create
        cur = database.cursor()

        foodList = []
        fl = cur.execute("SELECT * FROM food276")
        while (True):
            row = cur.fetchone()
            if row == None:
                break
            foodList.append(row[1])


        print('>>uploaded filename (from USER) is : ' + filename)

        img = utils.load_img('./static/'+filename, grayscale=False, color_mode='rgb', target_size=(299,299))
        img = utils.img_to_array(img)
        img = np.expand_dims(img, axis=0)
        img /= 255.

        pred = my_model.predict(img)
        index = np.argmax(pred)

        foodList.sort()
        pred_value = foodList[index]

        fl = cur.execute("SELECT * FROM food276 f where f.class = %s", pred_value)
        while (True):
            row = cur.fetchone()
            if row == None:
                break
            food_id = row[2]

        print('>>classification result is  : ' + pred_value + "  and food_id(fk) is " + str(food_id))

        # Cursor obejct , Databse Connection closing
        cur.close()
        database.close()

        if os.path.exists('./static/'+filename):
            os.remove('./static/'+filename)
            print('>>파일이 로컬에서 제거되었습니다.<<<')

        return pred_value, food_id

    def foodNutrient(self, food_id):
        # databse connect
        database = pymysql.connect(host=config.HOST, user=config.USER, password=config.PASSWORD,
                                   db=config.DATABASE, charset='utf8', port=config.PORT)
        # cursor object create
        cur = database.cursor()

        nutrientDto={}
        sql = "SELECT * FROM food WHERE food_id = %s"
        cur.execute(sql, food_id)
        while (True):
            row = cur.fetchone()
            if row == None:
                break

            nutrientDto['name']=row[1]
            nutrientDto['capacity'] = row[2]
            nutrientDto['calory'] = row[3]
            nutrientDto['carb'] = row[4]
            nutrientDto['pro'] = row[5]
            nutrientDto['fat'] = row[6]

        #Cursor obejct , Databse Connection closing
        cur.close()
        database.close()

        return json.dumps(nutrientDto, ensure_ascii=False, indent=4)
