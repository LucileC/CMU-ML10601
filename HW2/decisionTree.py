import inspect
import argparse
import csv 

# def mutual_information(vec1,vec2):


def test(input):
	with open(input,'rb') as fin:
		csv_reader = csv.reader(fin)
		csv_lists = inspect.get_csv_lists(csv_reader)
		# print(inspect.get_column_by_label_knowing_cond(csv_lists,'Y',[('A','1'),('C','0')]))
		# print(inspect.get_conditional_entropy(csv_lists,'Y',['C']))
		print(inspect.get_mutual_information(csv_lists,'Y','C'))


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