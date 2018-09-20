# 10601 Introduction to Machine Learning (Spring 2018), Homework 2: Decision Trees, 1: Written Questions

1. Entropy of Y: H(Y) = - p(Y=1) * log2(p(Y=1)) - p(Y=0) * log2(p(Y=0)) = - (3/7) * log2 (3/7) - (4/7) * log2 (4/7) ~ 0.9852.

2. Mutual information of Y and A : I(Y;A) = H(Y) - H(Y|A)

H(Y|A=1) = - p(Y=1|A=1) * log2(p(Y=1|A=1)) - p(Y=0|A=1) * log2(p(Y=0|A=1)) = - 3/4 * log2(3/4) - 1/4 * log2(1/4) = 0.8113

H(Y|A=0) = - p(Y=1|A=0) * log2(p(Y=1|A=0)) - p(Y=0|A=0) * log2(p(Y=0|A=0)) = - 0 * log2(0) - 1 * log2(1) = 0

H(Y|A) = p(A=1) * H(Y|A=1) + p(A=0) * H(Y|A=0) = 4/7 * H(Y|A=1) + 3/7 * H(Y|A=0) = 0.4636

I(Y;A) = 0.5216

3. Mutual information of Y and B : I(Y;B)

I(Y;B) 	= H(Y) - H(Y|A)

		= H(Y) - ( p(B=1) * H(Y|B=1) + p(B=0) * H(Y|B=0) )

		= H(Y) - ( p(B=1) *  ( - p(Y=1|B=1) * log2(p(Y=1|B=1)) - p(Y=0|B=1) * log2(p(Y=0|B=1)) ) + p(B=0) * - p(Y=1|B=0) * log2(p(Y=1|B=0)) - p(Y=0|B=0) * log2(p(Y=0|B=0)) )

		= H(Y) - ( 4/7 * ( - 2/4 * log2(2/4)) - 2/4 * log2(2/4) + 3/7 ( - 1/3 * log2(1/3)) - 2/3 * log2(2/3) )  = H(Y) - (4/7 * 1 + 3/7 * 0.9183) = H(Y) - 0.9650

		= 0.0202


