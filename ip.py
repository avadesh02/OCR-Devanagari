import cv2
import numpy as np
from matplotlib import pyplot as plt
import pylab
import sys

a = sys.argv[1:][0]
#flag = int(sys.argv[1:][1])

class letter_finder:
	def __init__(self,img):
		self.img = cv2.imread(img)
		self.img = cv2.resize(self.img,(0,0),fx=10,fy=5)
		avg = np.average(self.img)
		self.b_img = cv2.cvtColor(self.img,cv2.COLOR_BGR2GRAY)
		self.rows = self.img.shape[0]
		self.cols = self.img.shape[1]

	def threshold(self,thr_val):
		(t,thr_img) = cv2.threshold(self.b_img,thr_val,255,cv2.THRESH_BINARY)
		self.thr_img = thr_img 


	def find_line(self):
		count_matrix = []
		for y in range(0,self.thr_img.shape[0]-1):
			count = 0
			for x in range(0,self.thr_img.shape[1]-1):
				if self.thr_img[y][x] == 0:
					count += 1
			count_matrix.append(count)
		for i in range(len(count_matrix)-2,0,-1):
			if count_matrix[i] > int(self.cols/5):
				#print(count_matrix[i])
				bottom_line = i 
				break
		print(count_matrix)
		print('b',count_matrix[bottom_line])
		return (count_matrix,bottom_line)

	def remove_line(self,count_matrix):
		margin = 11
		y_line = count_matrix[0].index(max(count_matrix[0]))
		#print(count_matrix[1])
		upper_img = self.thr_img[0:(y_line - margin),0:self.cols]
		lower_img = self.thr_img[(y_line + margin):count_matrix[1],0:self.cols]
		
		final_image = np.concatenate((upper_img,lower_img),axis=0)
		#print('image has been formed without line')
		self.final_image = final_image

	def show_letters(self):
		for i in range(0,len(self.letter_matrix)-2):
			cv2.rectangle(self.img,(self.letter_matrix[i],0),(self.letter_matrix[i+1],self.cols),0,2)
		#print('letters are drawn')		

	def count_region(self,count_matrix,pos,r):
		count = sum(count_matrix[pos-r:pos+r])
		return count

	def find_letters(self,x1,y1,x2,y2):
		count_matrix = []
		letter_matrix = []
		letter_matrix.append(x1 + 10)
		for x in range(x1,x2):
			count = 0
			for y in range(y1,y2):
				if self.final_image[y][x] == 0:
					count += 1	
			count_matrix.append(count)
		#print(count_matrix)
		x = x1 + 80
		while x < len(count_matrix)-2:
			if self.count_region(count_matrix,x,3) < 2:
				if (x + x1) not in letter_matrix:
					letter_matrix.append(x + x1 + 10)
					x += 40
			x += 1
		for first,second in zip(letter_matrix,letter_matrix[1:]):
			#print(second-first)
			if second - first < 50:
			#	print('removing')
				letter_matrix.remove(first)
		#print('letters have been found')
		print('letter_matrix',letter_matrix)
		self.letter_matrix = letter_matrix
		print('letter_matrix',self.letter_matrix)
		self.no_words = len(letter_matrix)-1
		self.count_matrix = count_matrix

	def show_letters(self):#draws boxes around letters
		for i in range(0,len(self.letter_matrix)-1):
			cv2.rectangle(self.img,(self.letter_matrix[i],0),(self.letter_matrix[i+1],self.rows),0,1)
		#print('letters are drawn')	

	def resize_image(self,x,y):
		self.img = cv2.resize(self.img,(0,0),fx=x,fy=y)

	def show_image(self):
		cv2.imshow('letters',self.img)
		cv2.waitKey(0)

	def show_cropped_image(self):
		cv2.imshow('letters',self.final_image)
		cv2.waitKey(0)

	def plot_intensity(self):
		x = []
		for i in range(len(self.count_matrix)):
			x.append(i)
		
		plt.plot(x,self.count_matrix)
		plt.show()	
	
	def crop_letters(self,word_index):
		for x in range(0,len(self.letter_matrix)-1):
			letter = self.img[0:self.rows , self.letter_matrix[x]:self.letter_matrix[x+1]]
			letter = cv2.resize(letter,(0,0),fx=0.2,fy=0.2)
			cv2.imwrite('letters/' +str(word_index) + str(x)+'.png',letter)
		
		#print('letters have been stored...')	

	def store_cropped_letters(self,word_index):
		y = self.find_line()
		self.remove_line(y)
		self.find_letters(0,0,self.cols,self.final_image.shape[0])
		self.crop_letters(word_index)



im = 'test/' + a + '.png'
image = letter_finder(im)
img = cv2.imread(im)
#img = cv2.resize(img,(0,0),fx=10,fy=5)
avg1 = np.average(img)
med1 = np.median(img)
b_img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
avg = np.average(b_img)
#ratio = 190.0/avg
med = np.median(b_img)
#print('avg',avg,avg1)
#print('med',med,med1)
#b_img += 50
#cv2.imshow('1',b_img)
#cv2.waitKey(0)

#########################################
image.threshold(avg - 40)
y = image.find_line()
image.remove_line(y)
image.show_cropped_image()
image.find_letters(0,0,image.cols,image.final_image.shape[0])
#image.plot_intensity()
image.show_letters()
image.show_image()


