from flask import *
from pagesegmenter import *
import cv2
import numpy as np
from flask import *
import os
import sys
from flask import session
import cPickle as pickle
import shutil

app = Flask(__name__,static_url_path = "/words", template_folder='templates')
app.config['SECRET_KEY'] = 'oh_so_secret'



def store_f(start,no_words):
	no_letter_array = [] #stores number of letters in each word
	for i in range(start,no_words):
		img = 'words/'+ str(i) + '.png'
		word = letter_finder(img)
		word.store_cropped_letters(i)
		no_letter_array.append(word.no_words)
	return(no_letter_array)

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/image/get',methods=['POST','GET'])
def get_image():
	current_dir = os.getcwd()
	final_dir = os.path.join(current_dir, r'page')
	if os.path.exists(final_dir):
		shutil.rmtree(final_dir)
		os.makedirs(final_dir)	
	else:
		os.makedirs(final_dir)	
	file = request.files['page']
	file.save('page/image.jpg')
	return redirect(url_for('segment_image'))

@app.route('/image/process')
def segment_image():
	img = 'page/image.jpg'
	current_dir = os.getcwd()
	final_dir = os.path.join(current_dir, r'words')
	if os.path.exists(final_dir):
		shutil.rmtree(final_dir)
		os.makedirs(final_dir)	
	else:
		os.makedirs(final_dir)	
		
	image = word_finder(img)
	image.segment_page_into_words()	

	return redirect(url_for('segment_words'))	

@app.route('/words/process')
def segment_words():
	current_dir = os.getcwd()
	final_dir = os.path.join(current_dir, r'letters')
	if os.path.exists(final_dir):
		shutil.rmtree(final_dir)
		os.makedirs(final_dir)	
	else:
		os.makedirs(final_dir)	
	word_array = os.listdir('./words')
	print('finding letters and storing.....')
	label_array = store_f(0,len(word_array)-2)
	session['label_array'] = label_array
	print('letters have been stored...')
	print('uploading letters....')
	session['start'] = 0
	session['flag'] = 0
	session['no_words'] = session['start'] + 25
	return redirect(url_for('dev_home'))	

@app.route('/get/nextset',methods=['POST','GET'])
def get_next_set():
	value = 25
	limit = int(len(os.listdir('./words')))	
#	value = request.form['value']
#	print(value)
	if limit -session['start'] < 30 and limit -session['start'] > 0:
		print('if statment worked')
		print(session['flag'])
		session['start'] += 25
		session['no_words'] = limit-1 	
	elif limit - session['start'] > 25:
		print('elif is working')
		session['start'] += 25
		session['no_words'] = session['start'] + 25
	return redirect(url_for('dev_home'))

@app.route('/get/lastset',methods=['POST','GET'])
def go_back_one_set():
	
	value = request.form['value']
#	print(value)
	if session['start'] > 0:
		session['start'] -=  25
		session['no_words']  = session['start'] + 25
	
	return redirect(url_for('dev_home'))

@app.route('/dev_home')
def dev_home():
		return render_template('dev_page.html',no_words = session['no_words'],no_letter_array = session['label_array'],start = session['start'])	#start is th point from which words are thrown 


@app.route('/get/label_data',methods=['POST','GET'])
def get_data():
	temp_label_array = request.form.getlist('label')
	no_letter_array = session['label_array']
	#print(session['tmp'])
	index = 0
	label_array = []
	for w in range(session['start'],session['no_words']):
		label_array.append([])
		for l in range(0,no_letter_array[w]):
			label_array[w-session['start']].append(temp_label_array[index])
			index += 1
	#print(label_array)
	#print(no_letter_array)
	session['target_array'] = label_array
	session['no_letter_array'] = no_letter_array 
	return render_template('temp_page.html',temp_label_array=temp_label_array,no_letter_array = no_letter_array,no_words = session['no_words'],label_array = label_array,start = session['start'])

@app.route('/get/confirmation',methods=['GET','POST'])
def get_confirmation():
	dataset = []
	target_array = session['target_array']
	index = 0
	for w in range(session['start'],session['no_words']):
		for l in range(0,session['no_letter_array'][w]):
			img = 'letters/' + str(w) + str(l) + '.png' 
			letter_image = cv2.imread(img)
			dataset.append([])
			dataset[index].append(letter_image)
			dataset[index].append(target_array[w-session['start']][l])	
			index += 1

	current_dir = os.getcwd()
	final_dir = os.path.join(current_dir, r'database')
	if not os.path.exists(final_dir):
		os.makedirs(final_dir)
	i = os.listdir('./database')
	print(i)
	name_new_database = final_dir + '/' + str(len(i)) + '.p'
		
	pickle.dump( dataset ,open(name_new_database,'wb'))
	return redirect(url_for('get_next_set'))

@app.route('/prediction/image/get',methods=['POST','GET'])
def get_image_prediction():
	current_dir = os.getcwd()
	final_dir = os.path.join(current_dir, r'page')
	if os.path.exists(final_dir):
		shutil.rmtree(final_dir)
		os.makedirs(final_dir)	
	else:
		os.makedirs(final_dir)	
	file = request.files['page']
	file.save('page/image.jpg')
	return redirect(url_for('segment_image_prediction'))

@app.route('/prediction/image/process')
def segment_image_prediction():
	img = 'page/image.jpg'
	current_dir = os.getcwd()
	final_dir = os.path.join(current_dir, r'words')
	if os.path.exists(final_dir):
		shutil.rmtree(final_dir)
		os.makedirs(final_dir)	
	else:
		os.makedirs(final_dir)	
		
	image = word_finder(img)
	image.segment_page_into_words()	

	return redirect(url_for('segment_words_prediction'))	

@app.route('/prediction/words/process')
def segment_words_prediction():
	current_dir = os.getcwd()
	final_dir = os.path.join(current_dir, r'letters')
	if os.path.exists(final_dir):
		shutil.rmtree(final_dir)
		os.makedirs(final_dir)	
	else:
		os.makedirs(final_dir)	
	word_array = os.listdir('./words')
	print('finding letters and storing.....')
	label_array = store_f(0,len(word_array)-2)
	session['label_array'] = label_array
	print('letters have been stored...')
	print('uploading letters....')
	session['start'] = 0
	session['flag'] = 0
	session['no_words'] = session['start'] + 25
	return redirect(url_for('show_predictions'))	

from test_model import make_prediction

@app.route('/show/predictions',methods = ['GET','POST'])
def show_predictions():
	index_array = []
	prediction_array = []
	letters = os.listdir('./letters')
	print('predicitng output')
	#for i in range(session['start'],session['no_words']):
	for i in range(0,25):
		prediction_array.append([])
		for j in range(session['label_array'][i]):
			let = './letters/' + str(i) + str(j) +  '.png'
			print(let)
			img = cv2.imread(let)
			pred = make_prediction(img)
			prediction_array[i].append(pred)		
	return render_template('prediction.html',label_array = session['label_array'],prediction_array = prediction_array,start = 0,end = 25) 


@app.route('/uploads/<filename>')
def upload_image(filename):
	return send_from_directory('words',filename)

@app.route('/upload/<filename>')
def upload_letters(filename):
	return send_from_directory('letters',filename)

@app.route('/uploaded/<filename>')
def upload_page(filename):
	return send_from_directory('page',filename)


if __name__ == '__main__':
	#app.run(debug=True)
	app.run()







