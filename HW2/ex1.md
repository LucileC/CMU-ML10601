# 10601 Introduction to Machine Learning (Spring 2018), Homework 2: Decision Trees, 1: Written Questions

## Warm up

1. Entropy of Y: H(Y) = - p(Y=1) * log2(p(Y=1)) - p(Y=0) * log2(p(Y=0)) = - (3/7) * log2 (3/7) - (4/7) * log2 (4/7) ~ 0.9852.

2. Mutual information of Y and A : I(Y;A) = H(Y) - H(Y|A)

H(Y|A=1) = - p(Y=1|A=1) * log2(p(Y=1|A=1)) - p(Y=0|A=1) * log2(p(Y=0|A=1)) = - 3/4 * log2(3/4) - 1/4 * log2(1/4) = 0.8113

H(Y|A=0) = - p(Y=1|A=0) * log2(p(Y=1|A=0)) - p(Y=0|A=0) * log2(p(Y=0|A=0)) = - 0 * log2(0) - 1 * log2(1) = 0

H(Y|A) = p(A=1) * H(Y|A=1) + p(A=0) * H(Y|A=0) = 4/7 * H(Y|A=1) + 3/7 * H(Y|A=0) = 0.4636

I(Y;A) = 0.5216

3. Mutual information of Y and B : I(Y;B)

I(Y;B) = H(Y) - H(Y|B)

I(Y;B) = H(Y) - ( p(B=1) * H(Y|B=1) + p(B=0) * H(Y|B=0) )

I(Y;B) = H(Y) - ( p(B=1) *  ( - p(Y=1|B=1) * log2(p(Y=1|B=1)) - p(Y=0|B=1) * log2(p(Y=0|B=1)) ) + p(B=0) * - p(Y=1|B=0) * log2(p(Y=1|B=0)) - p(Y=0|B=0) * log2(p(Y=0|B=0)) )

I(Y;B) = H(Y) - ( 4/7 * ( - 2/4 * log2(2/4)) - 2/4 * log2(2/4) + 3/7 ( - 1/3 * log2(1/3)) - 2/3 * log2(2/3) )  = H(Y) - (4/7 * 1 + 3/7 * 0.9183) = H(Y) - 0.9650

I(Y;B) = 0.0202


4. Mutual information of Y and C : I(Y;C)

I(Y;C) = H(Y) - H(Y|C)

I(Y;C) = H(Y) - ( p(C=2) * H(Y|C=2) + p(C=1) * H(Y|C=1) + p(C=0) * H(Y|C=0) )

I(Y;C) = H(Y) - ( p(C=2) *  ( - p(Y=1|C=2) * log2(p(Y=1|C=2)) - p(Y=0|C=2) * log2(p(Y=0|C=2)) ) + p(C=1) *  ( - p(Y=1|C=1) * log2(p(Y=1|C=1)) - p(Y=0|C=1) * log2(p(Y=0|C=1)) ) + p(C=0) * - p(Y=1|C=0) * log2(p(Y=1|C=0)) - p(Y=0|C=0) * log2(p(Y=0|C=0)) )

I(Y;C) = H(Y) - ( 3/7 * ( - 2/3 * log2(2/3) - 1/3 * log2 (1/3)) + 1/7 * (0 - 1 * log(1)) + 3/7 * (- 2/3 * log2(2/3) - 1/3 * log2 (1/3)) )

I(Y;C) = H(Y) - ( 2 * 3/7 * ( - 2/3 * log2(2/3) - 1/3 * log2 (1/3)) + 0) = H(Y) - 0.7871

I(Y;C) = 0.1981

5. We chose to split on the attribute that has the highest mutual information with Y: attribute A. 

6. When we split on A, we know that A=0 => Y=0. We then only need to split for the case where A = 1.

We need to compute the mutual information I(Y;B|A=1) and I(Y;C|A=1).

I(Y;B|A=1) = H(Y|A=1) - H(Y|B,A=1)

I(Y;B|A=1) = H(Y|A=1) - ( p(B=1|A=1) * H(Y|B=1,A=1) + p(B=0|A=1) * H(Y|B=0,A=1) )

I(Y;B|A=1) = H(Y|A=1) - ( p(B=1|A=1) *  ( - p(Y=1|B=1,A=1) * log2(p(Y=1|B=1,A=1)) - p(Y=0|B=1,A=1) * log2(p(Y=0|B=1,A=1)) ) + p(B=0|A=1) * (- p(Y=1|B=0,A=1) * log2(p(Y=1|B=0,A=1)) - p(Y=0|B=0,A=1) * log2(p(Y=0|B=0,A=1)) ) )

I(Y;B|A=1) = H(Y|A=1) - ( 3/4 * ( - 2/3 * log2(2/3) - 1/3 * log2(1/3) ) + 1/4 * (-1 * log2(1) - 0) )

I(Y;B|A=1) = H(Y|A=1) - ( 3/4 * ( - 2/3 * log2(2/3) - 1/3 * log2(1/3) ) ) = 0.1226

On the other hand, we have:

I(Y;C|A=1) = H(Y|A=1) - H(Y|C,A=1)

I(Y;C|A=1) = H(Y|A=1) - ( p(C=2|A=1) * H(Y|C=2,A=1) + p(C=1|A=1) * H(Y|C=1,A=1) + p(C=0|A=1) * H(Y|C=0,A=1) )

I(Y;C|A=1) = H(Y|A=1) - ( p(C=2|A=1) *  ( - p(Y=1|C=2,A=1) * log2(p(Y=1|C=2,A=1)) - p(Y=0|C=2,A=1) * log2(p(Y=0|C=2,A=1)) ) + p(C=1,A=1) *  ( - p(Y=1|C=1,A=1) * log2(p(Y=1|C=1,A=1)) - p(Y=0|C=1,A=1) * log2(p(Y=0|C=1,A=1)) ) + p(C=0|A=1) * - p(Y=1|C=0,A=1) * log2(p(Y=1|C=0,A=1)) - p(Y=0|C=0,A=1) * log2(p(Y=0|C=0,A=1)) )

I(Y;C|A=1) = H(Y|A=1) - ( 2/4 * ( - 2/2 * log2(2/2) - 0 ) + 0 + 2/4 * ( - 1/2 * log2 (1/2) - 1/2 * log2 (1/2)) )

I(Y;C|A=1) = H(Y|A=1) - ( 2/4 * 0 + 0 + 2/4 * 1) = H(Y|A=1) - 0.5 = 0.3113

We have I(Y;C|A=1) > I(Y;B|A=1), so we should split on C.

7. We splitted on A and on C, so we have a tree of depth 2. The only uncertain case left is when A = 1 and C = 0. We then need to split on B. We will thus have a tree of depth 3. (given that we have 3 attributes, depth 3 is the maximal depth.)

8.  We obtain the following decision tree: 

<p align="center">
<img src="https://github.com/LucileC/CMU-ML10601/blob/master/HW2/decisiontree1.png ">
</p>

## Empirical Questions

9. Train and test errors on education and politicians dataset, depending on the depth of the tree.

| **Dataset** | **Max-Depth** | **Tain Error** | **Test Error** |
|-------------|---------------|----------------|----------------|
| politician  | 0             | 0.4430         | 0.5040         |
| politician  | 1             | 0.2013         | 0.2169         |
| politician  | 2             | 0.1342         | 0.1566         |
| politician  | 3             | 0.1145         | 0.1687         |
| politician  | 4             | 0.1074         | 0.2048         |
| education   | 0             | 0.3250         | 0.3100         |
| education   | 1             | 0.1950         | 0.2300         |
| education   | 2             | 0.1950         | 0.2300         |
| education   | 3             | 0.1700         | 0.2050         |
| education   | 4             | 0.1300         | 0.1600         |

10. Plot of train and test error against depth of the tree on the politicians dataset.

<p align="center">
<img src="https://github.com/LucileC/CMU-ML10601/blob/master/HW2/q10.png ">
</p>

11. Instead of selecting the depth of the tree according to the test error, we should split again the training set into a validation set and a training set. The selection of the best depth for the tree would be done on the validation set. Then we would report a final error on the test set, that would have been untouch. Because our sataset is small, we could also do cross-validation.

12. If we stop growing the tree whenever the mutual information for the best attribtute is lower than a threshold:
- if the threshold is too low, it won't help stopping and the tree will keep growing. We will still overfit.
- of the threshold is too high, it will stop growing the tree too early, and we will underfil.

In pratical settings, just as for choosing the best depth of the tree, we would need to use cross-validation to choose the best threshold.

13. Decision tree produced with the politician data with max depth 3.

	---------
	[ 66 republican / 83 democrat ]
	|  Superfund_right_to_sue = y: [ 64 republican / 28 democrat ]
	| |  Aid_to_nicaraguan_contras = y: [ 6 republican / 15 democrat ]
	| | |  Mx_missile = y: [ 6 republican / 3 democrat ]
	| | |  Mx_missile = n: [ 12 democrat ]
	| |  Aid_to_nicaraguan_contras = n: [ 58 republican / 13 democrat ]
	| | |  Export_south_africa = y: [ 38 republican / 13 democrat ]
	| | |  Export_south_africa = n: [ 20 republican ]
	|  Superfund_right_to_sue = n: [ 2 republican / 55 democrat ]
	| |  Export_south_africa = y: [ 1 republican / 55 democrat ]
	| | |  Immigration = y: [ 1 republican / 9 democrat ]
	| | |  Immigration = n: [ 46 democrat ]
	| |  Export_south_africa = n: [ 1 republican ]
	---------
	error(train): 0.114093959732
	error(test): 0.168674698795

