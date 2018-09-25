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

	def print_tree(self,i):
		if self.parent:
			print('%s child of %s = %s (has %d children)'%(self.attribute,self.parent.attribute,self.parent_val,self.get_children_number()))
		else :
			print('%s root'%self.attribute)
		if self.get_children_number()>0 and i < 10:
			for (_,child) in self.children:
				child.print_tree(i+1)

def unambiguous(data):
	if len(list(set(data))) == 1:
		return True

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


def decision_tree_rec(csv_lists,attributes,label,cond=list(),parent=None,parent_val=None):
	# print(attributes)
	att, I = next_node_decision_tree(csv_lists,label,attributes,cond)
	next_node = Node(att,parent,parent_val)
	possible_values_att = inspect.get_possible_values(csv_lists,att)
	children_I_list = list()
	for possible_val in possible_values_att:
		new_attributes = attributes[:]
		# print(att,possible_val)
		new_cond = cond[:]
		new_cond.append((att,possible_val))
		Y_knowing_cond = inspect.get_column_by_label(csv_lists,label,new_cond)
		if Y_knowing_cond:
			## si une seule valeur de Y (labe) possible, alors on s arrete et on donne cette valeur au noeud enfant
			child = None
			if len(list(set(Y_knowing_cond))) == 1:
				child = Node(Y_knowing_cond[0],next_node,possible_val)
				# print('leaf node here %s, has %d children)'%(child.attribute,child.get_children_number()))
			else:
				# print(new_attributes,att)
				new_attributes.remove(att)
				if len(new_attributes) > 0:
					# att, I = next_node_decision_tree(csv_lists,label=label,attributes=new_attributes,cond=new_cond)
					child = decision_tree_rec(csv_lists,attributes=new_attributes,label=label,cond=new_cond,parent=next_node,parent_val=possible_val)
				# else :
				# 	child = Node('Leaf',next_node,possible_val)
			if child:
				next_node.add_child(child,possible_val)
				print('%s child of %s = %s (and has %d children)'%(child.attribute,att,possible_val,child.get_children_number()))
	return next_node



def decision_tree(csv_lists):
	attributes, label = get_attributes_and_label(csv_lists)
	return decision_tree_rec(csv_lists,attributes,label)
	# return my_tree(csv_lists,label,attributes)


def test(input):
	with open(input,'rb') as fin:
		csv_reader = csv.reader(fin)
		csv_lists = inspect.get_csv_lists(csv_reader)
		dt = decision_tree(csv_lists)
		print('---------')
		dt.print_tree(0)

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

	# decisionTree(args.train_input,args.test_input,args.max_depth,args.train_out,args.test_out,args.metrics_out)

	test(args.train_input)
	# utest.unit_test_entropy(args.train_input)
	# utest.unit_test_mutual_information(args.train_input)