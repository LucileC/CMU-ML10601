import csv
import inspect
import argparse

def get_condition_string(cond_list):
	s = ''
	for cond in cond_list:
		if isinstance(cond,str):
			s += cond
		else :
			s += cond[0] + '=' + cond[1]
		s += ', '
	s = s[0:-2]
	return s

def get_entropy_string(triple):
	if triple[1] == None:
		return "H(%s)"%triple[0]
	else :
		return "H(%s|%s)"%(triple[0],get_condition_string(triple[1]))

def get_mutual_information_string(triple):
	if triple[2] == None:
		return "I(%s,%s)"%(triple[0],triple[1])
	else :
		return "I(%s,%s|%s)"%(triple[0],triple[1],get_condition_string(triple[2]))


def unit_test_entropy(input):
	b = True
	with open(input,'rb') as fin:
		csv_reader = csv.reader(fin)
		csv_lists = inspect.get_csv_lists(csv_reader)
		entropies = list()
		entropies.append(('Y',None,0.9852))
		entropies.append(('Y',[('A','1')],0.8113))
		entropies.append(('Y',[('A','0')],0.0))
		entropies.append(('Y',['A'],0.4636))
		entropies.append(('Y',['B'],0.9650))
		entropies.append(('Y',['C'],0.7871))
		entropies.append(('Y',['B',('A','1')],-0.1226+0.8113))
		entropies.append(('Y',['C',('A','1')],0.5))
		for triple in entropies:
			entropy = inspect.get_entropy(csv_lists,triple[0],triple[1])
			if entropy >= 0:
				if (round(entropy,4) != triple[2]) :
					print('---------------- Warning: different values here :-----------------')
					b = False
				print('%s = %.4f. (expected value is %.4f)'%(get_entropy_string(triple),entropy,triple[2]))
			else :
				print('Warning: Unable to compute %s'%get_entropy_string(triple))
				b = False
	return b



def unit_test_mutual_information(input):
	b = True
	with open(input,'rb') as fin:
		csv_reader = csv.reader(fin)
		csv_lists = inspect.get_csv_lists(csv_reader)
		mutual_info = list()
		mutual_info.append(('Y','A',None,0.5216))
		mutual_info.append(('Y','B',None,0.0202))
		mutual_info.append(('Y','C',None,0.1981))
		mutual_info.append(('Y','B',[('A','1')],0.1226))
		mutual_info.append(('Y','C',[('A','1')],0.3113))
		for triple in mutual_info:
			I = inspect.get_mutual_information(csv_lists,triple[0],triple[1],triple[2])
			if I >= 0:
				if (round(I,4) != triple[3]) :
					print('--------------- Warning: different values here :--------------------')
					b = False
				print('%s = %.4f. (expected value is %.4f)'%(get_mutual_information_string(triple),I,triple[3]))
			else :
				print('Warning: Unable to compute %s'%get_entropy_string(triple))
				b = False
	return b


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

	
