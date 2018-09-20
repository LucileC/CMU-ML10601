# 10601 Introduction to Machine Learning (Spring 2018), Homework 2: Decision Trees, 1: Written Questions

1. Entropy of Y: H(Y) = - p(Y=1) * log2(p(Y=1)) - p(Y=0) * log2(p(Y=0)) = - (3/7) * log2 (3/7) - (4/7) * log2 (4/7) ~ 0.9852.

2. Mutual information of Y and A : I(Y;A) = H(Y) - H(Y|A)

H(Y|A=1) = - p(Y=1|A=1) * log2(p(Y=1|A=1)) - p(Y=0|A=1) * log2(p(Y=0|A=1)) = - 3/4 * log2(3/4) - 1/4 * log2(1/4) = 0.8113

H(Y|A=0) = - p(Y=1|A=0) * log2(p(Y=1|A=0)) - p(Y=0|A=0) * log2(p(Y=0|A=0)) = - 0 * log2(0) - 1 * log2(1) = 0

H(Y|A) = p(A=1) * H(Y|A=1) + p(A=0) * H(Y|A=0) = 4/7 * H(Y|A=1) + 3/7 * H(Y|A=0) = 0.4636

I(Y;A) = 0.5216

3. Mutual information of Y and B : I(Y;B)

I(Y;B) = H(Y) - H(Y|A)

I(Y;B) = H(Y) - ( p(B=1) * H(Y|B=1) + p(B=0) * H(Y|B=0) )

I(Y;B) = H(Y) - ( p(B=1) *  ( - p(Y=1|B=1) * log2(p(Y=1|B=1)) - p(Y=0|B=1) * log2(p(Y=0|B=1)) ) + p(B=0) * - p(Y=1|B=0) * log2(p(Y=1|B=0)) - p(Y=0|B=0) * log2(p(Y=0|B=0)) )

I(Y;B) = H(Y) - ( 4/7 * ( - 2/4 * log2(2/4)) - 2/4 * log2(2/4) + 3/7 ( - 1/3 * log2(1/3)) - 2/3 * log2(2/3) )  = H(Y) - (4/7 * 1 + 3/7 * 0.9183) = H(Y) - 0.9650

I(Y;B) = 0.0202


4. Mutual information of Y and C : I(Y;C)

I(Y;C) = H(Y) - H(Y|C)

I(Y;C) = H(Y) - ( p(C=2) * H(Y|C=2) + p(C=1) * H(Y|C=1) + p(C=0) * H(Y|C=0) )

I(Y;C) = H(Y) - ( p(C=2) *  ( - p(Y=1|C=2) * log2(p(Y=1|C=2)) - p(Y=0|C=2) * log2(p(Y=0|C=2)) ) + p(C=2) *  ( - p(Y=1|C=1) * log2(p(Y=1|C=1)) - p(Y=0|C=1) * log2(p(Y=0|C=1)) ) + p(C=0) * - p(Y=1|C=0) * log2(p(Y=1|C=0)) - p(Y=0|C=0) * log2(p(Y=0|C=0)) )

I(Y;C) = H(Y) - ( 3/7 * ( - 2/3 * log2(2/3) - 1/3 * log2 (1/3)) + 1/7 * (0 - 1 * log(1)) + 2/7 * (- 1/2 log2(1/2) - 1/2 log2(1/2)) )

I(Y;C) = H(Y) - ( 3/7 * ( - 2/3 * log2(2/3) - 1/3 * log2 (1/3)) + 0 + 2/7) = H(Y) - 0.5957

I(Y;C) = 0.3895

5. We chose to split on the attribute that has the highest mutual information with H: attribute A. 

6. When we split on A, we know that A=0 => Y=0. We then only need to split for the case where A = 1.

We need to compute the mutual information I(Y;B|A=1) and I(Y;C|A=1).

I(Y;B|A=1) = H(Y|A=1) - H(Y|B,A=1)

I(Y;B|A=1) = H(Y|A=1) - ( p(B=1|A=1) * H(Y|B=1,A=1) + p(B=0|A=1) * H(Y|B=0,A=1) )

I(Y;B|A=1) = H(Y|A=1) - ( p(B=1|A=1) *  ( - p(Y=1|B=1,A=1) * log2(p(Y=1|B=1,A=1)) - p(Y=0|B=1,A=1) * log2(p(Y=0|B=1,A=1)) ) + p(B=0|A=1) * (- p(Y=1|B=0,A=1) * log2(p(Y=1|B=0,A=1)) - p(Y=0|B=0,A=1) * log2(p(Y=0|B=0,A=1)) ) )

I(Y;B|A=1) = H(Y|A=1) - ( 3/4 * ( - 2/3 * log2(2/3) - 1/3 * log2(1/3) ) + 1/4 * (-1 * log2(1) - 0) )

I(Y;B|A=1) = H(Y|A=1) - ( 3/4 * ( - 2/3 * log2(2/3) - 1/3 * log2(1/3) ) ) = H(Y|A=1) - 0. = 0.1226


