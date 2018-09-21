import argparse
import csv
import math 

def log2(a):
	return math.log(a,2)

def indexes(l,val):
	return [i for i, e in enumerate(l) if e == val]

'''	Returns a vector corresponding to the column col_idx in a csv file. 
	col_idx = -1 returns the last column. 
'''
def get_column(csv_lists,col_idx):
	col_vect = list()
	for i,row in enumerate(csv_lists):
		if i > 0:
			if col_idx > len(row):
				return False
			else : 
				col_vect.append(row[col_idx])
	return col_vect

'''
	Returns a vector of the column corresponding to label.
	If label is not present, returns False.
'''
def get_column_by_label(csv_lists,label):
	idx = csv_lists[0].index(label)
	if idx >= 0:
		return get_column(csv_lists,idx)
	return False

'''
	Returns a vector type Y|X=0: values of Y knowing X = 0.
	cond_list : list of conditions : [ (X1,0), (X2,0), ...]
'''
def get_column_by_label_knowing_cond(csv_lists,Y,cond_list):
	Y_vect = get_column_by_label(csv_lists,Y)
	cond_vectors = list()
	for (X,cond) in cond_list :
		X_vect = get_column_by_label(csv_lists,X)
		indexes_val_in_X = indexes(X_vect,cond)
		for i in range(len(Y_vect)):
			if i not in indexes_val_in_X:
				Y_vect[i] = None
	return [v for v in Y_vect if v]

'''
	Builds a list of lists from a csv read (easier to manipulate)
'''
def get_csv_lists(csv_reader):
	csv_lists = list()
	for row in csv_reader:
		csv_lists.append(row)
	return csv_lists

'''
	Returns a list of the values that variable "label" takes in dataset csv_lists
'''
def get_possible_values(csv_lists,label):
	X = get_column_by_label(csv_lists,label)
	return list(set(X))

def get_number_of_each_elt(col_vec):
	mylist = list(set(col_vec))
	number_of_each_label = dict()
	for l in mylist:
		number_of_each_label[l] = col_vec.count(l)
	return number_of_each_label

''' 
	Computes the entropy of a vector
'''
def compute_entropy(col_vec):
	n = len(col_vec)
	number_of_each_label = get_number_of_each_elt(col_vec)
	entropy = 0
	for l,count in number_of_each_label.items():
		f = float(count)/n
		entropy -=  f * log2(f)
	return entropy

'''
	Gets the entropy of a variable (label) given a dataset (list of lists)
'''
def get_entropy(csv_lists,label):
	X = get_column_by_label(csv_lists,label)
	return compute_entropy(X)

'''
	Gets the conditional entropy of a variable (label) given a dataset (list of lists) and a condition.
	cond_list : list/conjunction of conditions : [ cond1, cond2, ...] with cond as a variable (X) or cond as a tuple (X,1) for X=1.
'''
def get_conditional_entropy(csv_lists,label,cond_list):
	for cond in cond_list:
		## cond is just a variable
		if isinstance(cond,str):
			number_of_values_of_cond = get_number_of_each_elt(get_column_by_label(csv_lists,cond))
			entropy = 0
			n = len(csv_lists) - 1
			for possible_val, number_of_possible_val in number_of_values_of_cond.items():
				proba = float(number_of_possible_val)/n
				conditional_entropy = get_conditional_entropy(csv_lists,label,[(cond,possible_val)])
				entropy += proba * conditional_entropy
			return entropy
		else :
			Y = get_column_by_label_knowing_cond(csv_lists,label,[cond])
			return compute_entropy(Y)

def get_mutual_information(csv_lists,Y,A):
	return get_entropy(csv_lists,Y) - get_conditional_entropy(csv_lists,Y,[A])

def get_majority_vote(number_of_each_label):
	max = 0
	majority_vote = None
	for l,count in number_of_each_label.items():
		if count > max :
			max = count
			majority_vote = l
	return majority_vote

def get_error_majority_vote(col_vec):
	n = len(col_vec)
	number_of_each_label = get_number_of_each_elt(col_vec)
	majority_vote = get_majority_vote(number_of_each_label)
	number_of_majority_vote = number_of_each_label[majority_vote]
	error =  float(n - number_of_majority_vote) / n
	return error

def inspect(input,output):
	with open(input,'rb') as fin:
		csv_reader = csv.reader(fin)
		csv_lists = get_csv_lists(csv_reader)
		col_Y = get_column(csv_lists,-1)
		entropy = compute_entropy(col_Y)
		error = get_error_majority_vote(col_Y)
		with open(output,'w') as fout:
			fout.write('entropy: %.12f\nerror: %.12f'%(entropy,error))

if __name__ == '__main__':

	parser = argparse.ArgumentParser(description='Homework 2.')
	parser.add_argument('input', metavar='input', type=str, help='The path to the csv file with the data.')
	parser.add_argument('output', metavar='output', type=str, help='The path to the text file with the entropy score and the error.')
	parser.add_argument('--verbose', action="count", help='Printout information.')

	args = parser.parse_args()

	inspect(args.input,args.output)