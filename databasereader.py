import cPickle as pickle
import cv2
import sys

z = sys.argv[1:][0]
if z == 'countbyname':
	i = sys.argv[1:][1]
else:	
	i = int(sys.argv[1:][1])

#dataset = pickle.load(open("database/" + str(i) + ".p","rb"))
#dev_letter_db = pickle.load(open("data/dev_letter_db" + str(i) + ".p","rb"))
#dev_letter_db = pickle.load(open("data/dev_letter_db" + str(z) +  ".p","rb"))
dev_letter_db = pickle.load(open("data/dev_letter_D" +  ".p","rb"))
#dev_letter_db = pickle.load(open("./test_data" +  ".p","rb"))

def show_dataset(i):
	print(dev_letter_db[i][1])
	print(dev_letter_db[i][2])
	cv2.imshow('t',dev_letter_db[i][0])
	cv2.waitKey(0)

 
def integer_class_generator():
	try:
		class_index = pickle.load(open('data/class_index.p',"rb"))
	except:
		class_index = []
	real_dataset = []
	for z in range(0,len(dataset)-1):
		real_dataset.append([])
		if dataset[z][1] not in class_index:
			class_index.append(str(dataset[z][1]))
			img = cv2.resize(dataset[z][0],(32,32))
			real_dataset[z].append(img)
			real_dataset[z].append(class_index.index(dataset[z][1]))
			real_dataset[z].append(dataset[z][1])
		
		else:
			img = cv2.resize(dataset[z][0],(32,32))
			real_dataset[z].append(img)
			real_dataset[z].append(class_index.index(dataset[z][1]))
			real_dataset[z].append(dataset[z][1])
			
	#d1 = dev_letter_db + real_dataset 
	
	pickle.dump(real_dataset,open("data/dev_letter_db"+ str(i) + ".p","wb"))
	pickle.dump(class_index,open("data/class_index.p","wb"))

def find_no_in_same_class_index(i):
	count = 0
	class_index = pickle.load(open('data/class_index.p',"rb"))
	for data in dev_letter_db:
		#print data[1]
		if data[1] == i:
			count += 1

	#print count
	#print ('class is:' + class_index[i]) 
	return count

def find_count_by_name(z):
	class_index = pickle.load(open('data/class_index.p',"rb"))
	i = class_index.index(z)
	count = 0
	for data in dev_letter_db:
		#print data[1]
		if data[1] == i:
			count += 1

	print count
	print ('class is' + '  ' + z ) 
def info_db():
	class_index = pickle.load(open('data/class_index.p',"rb"))
	print('Number of classes is:'+ str(len(class_index)))
	print('size of database is :' + str(len(dev_letter_db)))

def print_class_index():
	class_index = pickle.load(open('data/class_index.p',"rb"))
	print class_index	

def count_dic_generator():
	print('finding count .....')	
	class_count = {}
	class_index = pickle.load(open('data/class_index.p',"rb"))
	for i in range(len(class_index)):
		count = find_no_in_same_class_index(i)
		class_count[i] = count
	print('done...')
	pickle.dump(class_count,open('data/class_count.p','wb')) 

#d1 = pickle.load(open("data/dev_letter_db0.p","rb"))
#d2 = pickle.load(open("data/dev_letter_db1.p","rb"))
#d3 = d1 + d2
#print(d1[0][2])
#pickle.dump(d3,open("data/dev_letter_D.p","wb"))

#class_index = pickle.load(open('class_index.p',"rb"))

#integer_class_generator()

if z == "data":
	show_dataset(i)
elif z == "info":
	info_db()
elif z == "help":
	print('info for information')
	print('data and index number to see that element')
	print('countbyindex and index: to search count of a class by index ')
	print('countbyname and name: to search by name of class to get count')
elif z == "countbyindex":
	find_no_in_same_class_index(i)	
elif z == "countbyname":
	find_count_by_name(i)
elif z== "printclassindex":
	print_class_index()
elif z== "create_count_dict":
	count_dic_generator()
