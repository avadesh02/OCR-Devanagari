from keras.models import model_from_json

import numpy as np
import cv2
import cPickle as pickle
import os


def make_prediction(d):
	
	d = cv2.resize(d,(32,32))
	data = np.array([d,d])
	class_dict_original = pickle.load(open('class_dict_original5.p','rb'))
	class_index = pickle.load(open('./official_database/class_index.p','rb'))

	json_file = open('model2.json','r')
	loaded_model_json = json_file.read()
	json_file.close()
	loaded_model = model_from_json(loaded_model_json)

	loaded_model.load_weights('model2.h5')
	predict = loaded_model.predict(data,batch_size=1)
	pred_class = (np.argmax(predict[0]))
	class_dict_original.append(pred_class)
		
	pred = (class_dict_original.index(pred_class))
	try:
		return  class_index[pred]
	except:
		return('!')

#pred = make_prediction(cv2.imread('./letters/11.png'))
#print(pred)
