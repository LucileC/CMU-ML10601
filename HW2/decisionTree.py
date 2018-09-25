import inspect
import argparse
import csv 
import unit_test as utest

class Node:
	def __init__(self,attribute,parent=None,parent_val=None,children=None):
		self.attribute = attribute
		self.parent = parent
		self.parent_val = parent_val
		self.children = children

	def add_child(self,node,attribute_value):
		if self.children:
			self.children.append([attribute_value,node])
		else :
			self.children = [[attribute_value,node]]

	def is_leaf(self):
		if self.children == None or len(self.children)  == 0:
			return True
		return False

	def get_children_number(self):
		if self.children:
			return len(self.children)
		else :
			return 0

	def get_cond(self):
		cond = list()
		node = self
		while (node.parent):
			cond.append((node.parent.attribute,node.parent_val))
			node = node.parent
		return cond

	def print_tree(self):
		if self.parent:
			print('%s child of %s = %s (has %d children)'%(self.attribute,self.parent.attribute,self.parent_val,self.get_children_number()))
		else :
			print('%s root'%self.attribute)
		if self.get_children_number()>0:
			for (_,child) in self.children:
				child.print_tree()

	def decide(self,attributes_value_dict):
		node = self
		while not node.is_leaf():
			# print(node.attribute)
			branch_value = attributes_value_dict[node.attribute]
			child_found = False
			for (val,child) in node.children:
				if val == branch_value:
					node = child
					child_found = True
			if not child_found:
				return 'Unable to make a decision'
		return node.attribute


def get_attributes_and_label(csv_lists):
	attributes = csv_lists[0][0:-1]
	label = csv_lists[0][-1]
	return attributes, label

def next_node_decision_tree(csv_lists,label,attributes,cond=None):
	I_max = 0
	att_max = None
	for att in attributes:
	# 	print('Computes %s'%utest.get_mutual_information_string((label,att,cond)))
		I = inspect.get_mutual_information(csv_lists,label,att,cond)
		if I > I_max:
			I_max = I
			att_max = att
	return att_max, I_max


def decision_tree_rec(csv_lists,attributes,label,depth,cond=list(),parent=None,parent_val=None):

	if depth == 0:
		Y_knowing_cond = inspect.get_column_by_label(csv_lists,label,cond)
		number_of_each_label = inspect.get_number_of_each_elt(Y_knowing_cond)
		majority_vote = inspect.get_majority_vote(number_of_each_label)
		next_node = Node(majority_vote,None)


	else :
		att, I = next_node_decision_tree(csv_lists,label,attributes,cond)
		next_node = Node(att,parent,parent_val)
		depth -= 1
		possible_values_att = inspect.get_possible_values(csv_lists,att)
		children_I_list = list()
		for possible_val in possible_values_att:
			# print(att,possible_val)
			new_attributes = attributes[:]
			new_cond = cond[:]
			new_cond.append((att,possible_val))
			Y_knowing_cond = inspect.get_column_by_label(csv_lists,label,new_cond)
			if Y_knowing_cond:
				## si une seule valeur de Y (labe) possible, alors on s arrete et on donne cette valeur au noeud enfant
				child = None
				if len(list(set(Y_knowing_cond))) == 1:
					child = Node(Y_knowing_cond[0],next_node,possible_val)
				else:
					new_attributes.remove(att)
					if len(new_attributes) > 0 and depth>0:
						child = decision_tree_rec(csv_lists,attributes=new_attributes,label=label,depth=depth,cond=new_cond,parent=next_node,parent_val=possible_val)
					elif len(new_attributes) == 0 or depth==0:
						number_of_each_label = inspect.get_number_of_each_elt(Y_knowing_cond)
						majority_vote = inspect.get_majority_vote(number_of_each_label)
						child = Node(attribute=majority_vote,parent=next_node,parent_val=possible_val,children=None)
				if child:
					next_node.add_child(child,possible_val)
					# print('%s child of %s = %s (and has %d children)'%(child.attribute,att,possible_val,child.get_children_number()))
				# else:
				# 	print('no child')
	return next_node



def decision_tree_train(csv_lists,max_depth):
	attributes, label = get_attributes_and_label(csv_lists)
	return decision_tree_rec(csv_lists,attributes,label,max_depth)
	# return my_tree(csv_lists,label,attributes)

'''
	Returns a list of dictionaries
'''
def get_examples(csv_lists):
	examples_list = list()
	for i in range(1,len(csv_lists)):
		example = dict()
		for j in range(len(csv_lists[i])):
			example[csv_lists[0][j]] = csv_lists[i][j]
		examples_list.append(example)
	return examples_list

def get_error(y,y_predict):
	n = len(y)
	if len(y_predict) != n:
		return 'Number of predictions and number of examples are different!'
	n_not_OK = 0
	for i in range(n):
		if (y[i]!=y_predict[i]):
			n_not_OK += 1
	return float(n_not_OK)/n

def get_expected_values(csv_lists):
	label = csv_lists[0][-1]
	return inspect.get_column_by_label(csv_lists ,label)

def test_and_get_error(csv_lists,decision_tree_root,output_file):
	examples = get_examples(csv_lists)
	y_predict = list()
	flabel = open(output_file,'w')
	for example in examples:
		label = decision_tree_root.decide(example)
		y_predict.append(label)
		# print(label)
		flabel.write('%s\n'%label)
	## compute error on training set
	y = get_expected_values(csv_lists)
	error = get_error(y,y_predict)
	flabel.close()
	return error

def run(train_input,test_input,max_depth,train_out,test_out,metrics_out):

	## training the decision tree
	ftrain = open(train_input,'rb')
	csv_reader_train = csv.reader(ftrain)
	csv_lists_train = inspect.get_csv_lists(csv_reader_train)
	dt = decision_tree_train(csv_lists_train,int(max_depth))
	print('---------')
	dt.print_tree()
	print('---------')

	## test on training set
	train_error = test_and_get_error(csv_lists_train,dt,train_out)

	# test on test set
	ftest = open(test_input,'rb')
	csv_reader_test = csv.reader(ftest)
	csv_lists_test = inspect.get_csv_lists(csv_reader_test)
	test_error = test_and_get_error(csv_lists_test,dt,test_out)

	error_string = 'error(train): %.12f\nerror(test): %.12f'%(train_error,test_error)
	print(error_string)

	with open(metrics_out,'w') as fmetrics:
		fmetrics.write(error_string)



if __name__ == '__main__':

	parser = argparse.ArgumentParser(description='Homework 2.')
	parser.add_argument('train_input', metavar='train_input', type=str, help='path to the training input .csv file')
	parser.add_argument('test_input', metavar='test_input', type=str, help='path to the test input .csv file')
	parser.add_argument('max_depth', metavar='max_depth', type=str, help='maximum depth to which the tree should be built')
	parser.add_argument('train_out', metavar='train_out', type=str, help='path of output .labels file to which the predictions on the training data should be written')
	parser.add_argument('test_out', metavar='test_out', type=str, help='path of output .labels file to which the predictions on the test data should be written')
	parser.add_argument('metrics_out', metavar='metrics_out', type=str, help='path of the output .txt file to which metrics such as train and test error should be written')
	parser.add_argument('--verbose', action="count", help='Printout information.')

	args = parser.parse_args()

	run(args.train_input,args.test_input,args.max_depth,args.train_out,args.test_out,args.metrics_out)
