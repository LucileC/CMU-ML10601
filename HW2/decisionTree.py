import myinspect as insp
import argparse
import csv 
import unit_test as utest
import matplotlib
import matplotlib.pyplot as plt


class Node:
	def __init__(self,attribute,parent=None,parent_val=None,Y=None,children=None):
		self.attribute = attribute
		self.parent = parent
		self.parent_val = parent_val
		self.children = children
		# self.depth = depth
		self.Y = Y

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

	def get_depth(self,depth=0):
		if self.parent == None:
			return depth
		else:
			return self.parent.get_depth(depth+1)


	def get_Y_string(self):
		if self.Y==None:
			print('No values for this node!')
		else:
			s = '[ '
			for val in list(set(self.Y)):
				s += '%d %s / '%(self.Y.count(val),val)
			s = s[:-2] + ']'
		return s

	def get_indent_string(self):
		s = ''
		for i in range(self.get_depth()):
			s += '| '
		return s

	def print_tree2(self):
		s = ''
		if self.parent:
			s += self.get_indent_string() + self.parent.attribute + ' = ' + self.parent_val + ': '
		s+= self.get_Y_string()
		print(s)
		if self.get_children_number()>0:
			for (_,child) in self.children:
				child.print_tree2()


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
		I = insp.get_mutual_information(csv_lists,label,att,cond)
		if I > I_max:
			I_max = I
			att_max = att
	return att_max, I_max


def decision_tree_rec(csv_lists,attributes,label,depth,cond=list(),parent=None,parent_val=None):

	if depth == 0:
		Y_knowing_cond = insp.get_column_by_label(csv_lists,label,cond)
		number_of_each_label = insp.get_number_of_each_elt(Y_knowing_cond)
		majority_vote = insp.get_majority_vote(number_of_each_label)
		## leaf node
		next_node = Node(attribute=majority_vote,parent=None,Y=Y_knowing_cond)


	else :
		att, I = next_node_decision_tree(csv_lists,label,attributes,cond)
		if I == 0:
			#if we do not gain abything by expending the tree, stop and create a leaf node.
			Y_knowing_cond = insp.get_column_by_label(csv_lists,label,cond)
			number_of_each_label = insp.get_number_of_each_elt(Y_knowing_cond)
			majority_vote = insp.get_majority_vote(number_of_each_label)
			## leaf node
			next_node = Node(attribute=majority_vote,parent=parent,parent_val=parent_val,Y=Y_knowing_cond,children=None)	
		else:
			next_node = Node(att,parent=parent,parent_val=parent_val,Y=insp.get_column_by_label(csv_lists,label,cond),children=None)
			depth -= 1
			possible_values_att = insp.get_possible_values(csv_lists,att) # est ce qu il ne fait pas la condition ici aussi??
			children_I_list = list()
			for possible_val in possible_values_att:
				# print(att,possible_val)
				new_attributes = attributes[:]
				new_cond = cond[:]
				new_cond.append((att,possible_val))
				Y_knowing_cond = insp.get_column_by_label(csv_lists,label,new_cond)
				if Y_knowing_cond:
					## si une seule valeur de Y (labe) possible, alors on s arrete et on donne cette valeur au noeud enfant
					child = None
					if len(list(set(Y_knowing_cond))) == 1:
						## leaf node
						child = Node(attribute=Y_knowing_cond[0],parent=next_node,parent_val=possible_val,Y=Y_knowing_cond)
					else:
						new_attributes.remove(att)
						if len(new_attributes) > 0 and depth>0:
							child = decision_tree_rec(csv_lists,attributes=new_attributes,label=label,depth=depth,cond=new_cond,parent=next_node,parent_val=possible_val)
						elif len(new_attributes) == 0 or depth==0:
							number_of_each_label = insp.get_number_of_each_elt(Y_knowing_cond)
							majority_vote = insp.get_majority_vote(number_of_each_label)
							## leaf node
							child = Node(attribute=majority_vote,parent=next_node,parent_val=possible_val,Y=Y_knowing_cond,children=None)
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
	return insp.get_column_by_label(csv_lists ,label)

def test_and_get_error(csv_lists,decision_tree_root,output_file=None):
	examples = get_examples(csv_lists)
	y_predict = list()
	if output_file:
		flabel = open(output_file,'w')
	for example in examples:
		label = decision_tree_root.decide(example)
		y_predict.append(label)
		# print(label)
		if output_file:
			flabel.write('%s\n'%label)
	## compute error on training set
	y = get_expected_values(csv_lists)
	error = get_error(y,y_predict)
	if output_file:
		flabel.close()
	return error

def run(train_input,test_input,max_depth,train_out,test_out,metrics_out):

	## training the decision tree
	ftrain = open(train_input,'r')
	csv_reader_train = csv.reader(ftrain)
	csv_lists_train = insp.get_csv_lists(csv_reader_train)
	dt = decision_tree_train(csv_lists_train,int(max_depth))
	print('---------')
	dt.print_tree2()
	print('---------')

	## test on training set
	train_error = test_and_get_error(csv_lists_train,dt,train_out)

	# test on test set
	ftest = open(test_input,'r')
	csv_reader_test = csv.reader(ftest)
	csv_lists_test = insp.get_csv_lists(csv_reader_test)
	test_error = test_and_get_error(csv_lists_test,dt,test_out)

	error_string = 'error(train): %.12f\nerror(test): %.12f'%(train_error,test_error)
	print(error_string)

	with open(metrics_out,'w') as fmetrics:
		fmetrics.write(error_string)

def plot(points1_x,points1_y,points2_x,points2_y):
	# pass
	plt.plot(points1_x,points1_y,label='Train error')
	plt.plot(points2_x,points2_y,label='Test error')
	plt.xlabel('Depth depth of tree')
	plt.ylabel('Error')
	plt.title('Error on training and test sets against depth of decision tree')
	plt.legend()
	plt.show()



def plot_errors_as_function_of_depth(train_input,test_input):
	ftrain = open(train_input,'r')
	csv_reader_train = csv.reader(ftrain)
	csv_lists_train = insp.get_csv_lists(csv_reader_train)

	ftest = open(test_input,'r')
	csv_reader_test = csv.reader(ftest)
	csv_lists_test = insp.get_csv_lists(csv_reader_test)

	depths = list()
	train_errors = list()
	test_errors = list()
	
	for depth in range(len(csv_lists_train[0])-1):
		dt = decision_tree_train(csv_lists_train,depth)
		train_error = test_and_get_error(csv_lists_train,dt)
		test_error = test_and_get_error(csv_lists_test,dt)
		depths.append(depth)
		train_errors.append(train_error)
		test_errors.append(test_error)

	plot(depths,train_errors,depths,test_errors)


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

	# run(args.train_input,args.test_input,args.max_depth,args.train_out,args.test_out,args.metrics_out)

	plot_errors_as_function_of_depth(args.train_input,args.test_input)
