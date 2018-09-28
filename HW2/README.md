# Decision trees

## Compute entropy and mutual information

To run script:

* Small dataset:

```python inspect.py handout/small_train.csv small_output/insp.txt```

## Train and test a decision tree

Command line:

* Small dataset:

```python decisionTree.py handout/small_train.csv handout/small_test.csv 2 small_output/depth3/train.labels small_output/depth3/test.labels small_output/depth2/metrics.txt```

* Politicians dataset:

```python decisionTree.py handout/politicians_train.csv handout/politicians_test.csv 4 politicians_output/depth4/train.labels politicians_output/depth4/test.labels politicians_output/depth4/metrics.txt```

* Education dataset:

```python decisionTree.py handout/education_train.csv handout/education_test.csv 4 education_output/depth4/train.labels education_output/depth4/test.labels education_output/depth4/metrics.txt```