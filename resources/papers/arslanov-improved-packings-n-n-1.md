---
title: "Improved packings of n(n-1) unit squares in a square"
authors: "M. Z. Arslanov, S. A. Mustafin, Z. K. Shangitbayev"
venue: "Electronic Journal of Combinatorics, 28(4), #P4.22"
year: 2021
source_url: "https://www.combinatorics.org/ojs/index.php/eljc/article/download/v28i4p22/pdf/"
doi: "https://doi.org/10.37236/8586"
archived: 2026-08-22
extraction_note: "Converted from PDF via pdfminer.six text extraction; math reconstructed to LaTeX, tables reformatted, (cid:XX) codes resolved, running footers and page numbers removed."
---

# Improved packings of $n(n-1)$ unit squares in a square

**M.Z. Arslanov**\*

**S.A. Mustafin**

Institute of Information and Computational Technologies
Almaty, Kazakhstan

mzarslanov@hotmail.com  sam@ipic.kz

**Z.K. Shangitbayev**

Almaty Management University
Almaty, Kazakhstan

sh.zhanbek@gmail.com

Submitted: Mar 14, 2019; Accepted: Oct 15, 2021; Published: Nov 5, 2021

&copy; The authors. Released under the CC BY-ND license (International 4.0).

## Abstract

Let $s(n)$ be the side of the smallest square into which we can pack $n$ unit squares. The purpose of this paper is to prove that $s(n^2 - n) < n$ for all $n \geq 12$. Besides, we show that $s(18^2 - 17) < 18$, $s(17^2 - 16) < 17$, and $s(16^2 - 15) < 16$.

Mathematics Subject Classifications: 05B40, 52C15

## 1 Introduction

The problem of packing equal squares in a square has been around for some 40 years [1]. Let $s(n)$ be the side of the smallest square into which we can pack $n$ unit squares. Nagamochi [3] proved that $s(n^2 - 2) = s(n^2 - 1) = n$. It follows from [1] that $s(n^2 - O(n^{7/11})) < n$ for big $n$. From [4] it follows that the $7/11$ degree can be reduced to $5/8$.

An important question is to find the minimum $n$ for which $s(n^2 - n) < n$. For small $n$, only $s(2) = 2$ and $s(6) = 3$ have been proved, but we dont even know the proof of $s(12) = 4$. It was proved in [2] that $s(n^2 - n - 1) < n$ for $3 < n < 11$. Due to Lars Cleemann it was known that $s(17^2 - 17) < 17$ [2]. Nagamochi in [3] mistakenly says that the following is proved in [2]

$$s(n^2 - n) < n \quad \forall n \geq 17. \tag{1}$$

The truth is that in [2] a sporadic squeezable packing of $272$ unit squares in a square $(17, 17)$ is given, proving that $s(17^2 - 17) < 17$, but from this it does not follow that $s(18^2 - 18) < 18$ etc. Thus, Nagamochi's implicit conjecture (1) needs a proof.

We prove the conjecture and even more: $s(n^2 - n) < n$ $\forall n \geq 12$, and, moreover,

$$s(18^2 - 17) < 18, \quad s(17^2 - 16) < 17, \quad s(16^2 - 15) < 16.$$

\*Supported by MSE of Kazakhstan grant GF4 AP05133090.

## 2 Some squeezable packing of rectangles

Let a packing of $m$ unit squares in a rectangle $R = (R_x, R_y)$ be given. We assume that $(R_x - 1)(R_y - 1) < m < R_x R_y$ and we can't pack a unit square in the waste area. This packing is called squeezable if both sides of a rectangle can be reduced, i.e., for some $\delta > 0$ there exists a packing of $m$ unit squares in a rectangle $(R_x - \delta, R_y - \delta)$. The maximum of such $\delta > 0$ is called the value of squeezing and is denoted by $\delta(R, m)$. We write $\delta(R, m) = 0$ if the packing is not squeezable.

The property of squeezability of a packing for small parameters can be proved rather simply. However proving this property for large parameters is a non-trivial mathematical problem. The following obvious formula connects $\delta(R, m)$ and $s(n)$:

$$s(n) = \lceil s(n) \rceil - \delta((\lceil s(n) \rceil, \lceil s(n) \rceil), n).$$

If $\delta((R_x, R_y), m) < 1$ then the fact that for integer $R_x$, $R_y$

$$\delta((R_x, R_y), m) \leq \delta((R_x + 1, R_y), m + R_y - 1) \tag{2}$$

can be proved by adding $R_y - 1$ unit squares to the $x$-side of a rectangle $(R_x, R_y)$. Figure 1 shows the basic idea for efficiently packing unit squares in a square $S$, where rectangles $C$ and $D$ are integer and the waste is in rectangles $A$ and $B$. It is easy to see that if the packing of unit squares in rectangles $A$, $B$ is squeezable, then the packing of unit squares in $S$ is squeezable and

$$\delta(S, \cdot) \geq \min(\delta(A, \cdot), \delta(B, \cdot)). \tag{3}$$

This bound can be increased if we note that after squeezing there is a little space between rectangles $A$, $B$. We can give this space to a rectangle with minimal squeezing value in order to increase that value and thus to increase the evaluation of $\delta(S, \cdot)$.

> *[Figure 1: Scheme of squeezable packing -- shows square S divided into four rectangles C, A, B, D]*

Let us consider a packing of 26 unit squares in a rectangle $(4, 8)$ (see Figure 2). This packing is centrally symmetric and the waste is equal to 6.

> *[Figure 2: Squeezable packing of 26 unit squares in a rectangle (4,8) -- shows tilted stacks with points P, S1, P1, and origin (0,0)]*

In Figure 2 we see one of the main ideas for packing unit squares: using of stacks $(4, 1)$ tilted by an angle $\alpha = \arcsin(8/17)$. The main idea for squeezing a packing follows from it: tilting stacks $(4, 1)$ by an angle $\alpha + \varepsilon$ so that the stack $(4, 1)$ is located in a vertical strip of width $4 - \delta$, where $\varepsilon$ and $\delta$ are sufficiently small. Hereinafter we determine the orientation of a unit square by a unit vector $(x, y)$ with $x > 0$, $y \geq 0$, $x^2 + y^2 = 1$ directed along the side of this unit square. If the bottom vertex of the unit square is at the origin then the three other vertices have coordinates $(x, y)$, $(x - y, y + x)$, $(-y, x)$. Note that if two points $P_t$, $P_b$ are taken on the top side and the bottom side of this unit square then the scalar product $\langle P_t - P_b, (x, y) \rangle$ is equal to 1.

Continuing with the example in Figure 2, after increasing the tilt the stack $(4, 1)$ in a vertical strip of width $4 - \delta$ has orientation $(x_1, y_1)$, $x_1 > 0$, $y_1 \geq 0$ satisfying the system of equations

$$4x_1 + y_1 = 4 - \delta, \quad x_1^2 + y_1^2 = 1.$$

To evaluate the squeezing value $\delta((4, 8), 26)$, we use the bisection method. The packing remains centrally symmetric. The distance between the point $P = (P_x, P_y) = (1 - \delta/2, 2 - \delta/2)$ and the upper side of the square $S_2$ intersecting the line $x = 1 - \delta/2$ in the point $P_1 = (P_{1x}, P_{1y}) = \left(1 - \frac{\delta}{2},\; \left(1 - \frac{\delta}{2}\right)\frac{y_1}{x_1} + \frac{1}{x_1} + \frac{1 - x_1}{x_1 y_1}\right)$ is critical. For $\delta = 0.01$ we have $x_1 = .877695\ldots$, $y_1 = .479219\ldots$, $P_y - P_{1y} = 0.021604 > 0$. For $\delta = 0.02$, $x_1 = .87312663\ldots$, $y_1 = .48749347\ldots$, $P_y - P_{1y} = -0.0061309\ldots < 0$. The bisection method gives evaluation $\delta((4, 8), 26) > 0.0177702$.

Figure 3 shows a more complex example, a centrally symmetric squeezable packing of 64 unit squares in a rectangle $(6, 12)$. Four unit squares: $S_3$, $S_6$ and their symmetric ones have not the orientation $\left(\frac{35}{37}, \frac{12}{37}\right)$ nor $(1, 0)$. Hereinafter we denote points and squares by the same indices in different figures without losing accuracy.

> *[Figure 3: Squeezable packing of 64 unit squares in a rectangle (6,12) -- shows centrally symmetric arrangement with labeled squares S1--S9 and points P0--P8]*

In this packing the left vertex of $S_2$ is on a side of $S_1$. The square $S_3$ is placed so that the right vertices of squares $S_2$, $S_5$, and the top vertex of $S_4$ are on the sides of $S_3$. Vertices of the squares $S_8$, $S_7$, $S_9$ are on sides of $S_6$. Calculations show that there is a small distance between $S_3$ and $S_6$, which guarantees squeezability of the given packing.

To calculate the squeezing value $\delta((6, 12), 64)$, take $\delta = 0.004$ and define the existence of a packing 64 unit squares in a rectangle $(6 - \delta, 12 - \delta)$. The distance between the right vertex of $S_3$ and the top side of $S_6$ should be not less than 1.

Table 1 contains calculations with $\delta = 0.004$.

| Object | Formulae or system of equations | Numerical value |
|---|---|---|
| $\delta$ | | $0.004$ |
| Orientation $(x_1, y_1)$ of stack $(6,1)$ | $y_1^2 + x_1^2 = 1$, $6y_1 + x_1 = 6 - \delta$ | $(0.328061226490, 0.94465646225)$ |
| $P_0$ | $P_0 = \left(-2 + \frac{\delta}{2},\; \frac{(2 - \delta/2)\, x_1}{y_1} + \frac{2}{y_1} + \frac{1 - y_1}{x_1 y_1}\right)$ | $(-1.998, 2.989621361)$ |
| $P_1$ | $P_1 = P_0 + (x_1 + y_1,\; y_1 - x_1)$ | $(-0.725282311, 3.6062165968)$ |
| $P_2$ | $P_2 = (\delta/2 - 1,\; 4 - \delta/2)$ | $(-0.998, 3.998)$ |
| $P_3$ | $P_3 = \left(3 - 3y_1 - \frac{\delta}{2},\; \frac{-(3 - 3y_1 - \delta/2)\, x_1}{y_1} + \frac{4}{y_1}\right)$ | $(0.1640306130, 4.177378839)$ |
| Orientation $(x_2, y_2)$ of $S_3$ | $x_2^2 + y_2^2 = 1$, $\langle P_2 - P_3, (-y_2, x_2) \rangle = 1$ | $(0.390085325, 0.92077871336)$ |
| $P_4$ | $P_4 = \langle P_1, (x_2, y_2) \rangle \cdot (x_2, y_2) + \langle P_2, (y_2, -x_2) \rangle \cdot (y_2, -x_2)$ | $(-1.0972231, 3.76378828)$ |
| $P_5$ | $P_5 = P_4 + (x_2 + y_2,\; y_2 - x_2)$ | $(0.213640902, 4.29448167498)$ |
| $P_6$ | $P_6 = \left(\frac{1}{2}\delta,\; 5 - \frac{1}{2}\delta\right)$ | $(0.002, 4.998)$ |
| $P_7$ | $P_7 = (3 - \delta/2,\; -(3 - \delta/2)\,x_1/y_1) + 5(0, 1/y_1) + 2(-y_1, x_1)$ | $(1.108687, 4.9079035)$ |
| $P_8$ | $P_8 = (1 - \delta/2,\; 5 - \delta/2)$ | $(0.998, 4.998)$ |
| Orientation $(x_3, y_3)$ of $S_6$ | $x_3^2 + y_3^2 = 1$, $\langle P_6 - P_7, (-y_3, x_3) \rangle = 1$ | $(0.5062565099, 0.862382946)$ |
| Distance between $P_5$ and top side of $S_6$ | $\langle P_8 - P_5, (x_3, y_3) \rangle$ | $1.00378910536129684$ |

**Table 1:** Calculations with $\delta = 0.004$.

Calculations with $\delta = 0.005$ give $\langle P_8 - P_5, (x_2, y_2) \rangle = 0.999617371807702270$, i.e., the squares $S_3$, $S_6$ intersect. The bisection method gives evaluation $\delta((6, 12), 64) > .00490823$.

A packing of 58 unit squares in a rectangle $(6, 11\text{-}2/35)$ can be obtained by removing one stack $(6,1)$ in Figure 3 and lifting up by $37/35$ all the squares that are below this stack. Similar calculations give the evaluation of the squeezing value $\delta((6, 11), 58) > 0.01681735886$.

Consider a more difficult problem of a squeezable packing of 43 unit squares in a rectangle $(5, 10)$. In Figure 4 six unit squares $S_1$, $S_4$, $S_9$, $S_{10}$, $S_{11}$, $S_{12}$ have not the orientation $\left(\frac{5}{13}, \frac{12}{13}\right)$ nor $(1, 0)$.

> *[Figure 4: Squeezable packing of 43 unit squares in a rectangle (5,10) -- shows arrangement with labeled squares S1--S15]*

The square $S_1$ has a vertex on the side of the rectangle $(5,10)$, one on a side of $S_2$, and one on a side of $S_3$. The right vertex of $S_1$ is on the bottom side of $S_4$. $S_4$ is tilted so that the bottom right vertex of $S_3$ is on the left side of $S_4$ and the top vertex of the stack $(3, 1)$ is on the right side of $S_4$. The left vertex of $S_5$ is on the side of $S_6$. The squares $S_9$, $S_{10}$ are tilted by the same angle so that the vertex of $S_8$ is on the side of $S_9$, the vertex of $S_5$ is on the bottom side of $S_9$, and the vertex of $S_7$ is on the bottom side of $S_{10}$. The squares $S_{11}$, $S_{12}$ form a rectangle $(2,1)$. The right vertex of $S_{12}$ is on the right side of a rectangle $(5,10)$. The vertex of $S_{13}$ is on the top side of $S_{11}$. The bottom sides of $S_{11}$ and $S_{12}$ are parallel to the line connecting the right vertices of $S_9$ and $S_{10}$. The vertex of $S_{14}$ is on the bottom side of $S_{15}$. Calculations show that there is a small distance $0.0055111\ldots$ between the bottom side of the rectangle $(2, 1) = S_{11} \cup S_{12}$ and the line connecting the right vertices of $S_9$ and $S_{10}$. This guarantees squeezability of the given packing.

Calculation of the squeezing value $\delta((5, 10), 43)$ gives the evaluation $\delta((5, 10), 43) > 0.0009652493$. This packing plays an important role in the squeezable packing of 132 unit squares in a square $(12,12)$. Below we show the evaluation of $\delta((12, 12), 132)$. From this evaluation one can obtain the evaluation of $\delta((5, 10), 43)$. Analogous calculations give the evaluation of the squeezing value $\delta((5, 9), 38) > 0.020403$.

Table 2 contains the evaluations of the squeezing values of some rectangles.

| Rectangle $R$ | $n$ | $\delta(R, n)$ |
|---|---|---|
| $(4,8)$ | $26$ | $> 0.01777021751$ |
| $(5,10)$ | $43$ | $> 0.0009652493$ |
| $(5,9)$ | $38$ | $> 0.020403$ |
| $(6,12)$ | $64$ | $> 0.004908231774819$ |
| $(6,11)$ | $58$ | $> 0.01681735886$ |

**Table 2.** Evaluations of squeezing value of some rectangles.

To prove conjecture (1), we need the following lemma.

**Lemma 1.** For any $k \geq 3$ there exists a squeezable packing of $4k^2 + 6k - 2$ unit squares in a rectangle $(2k, 2k + 4)$ (the waste is equal to $2k + 2$).

The proof is technically simple and can be understood from Figure 5, showing a centrally symmetric squeezable packing of 86 unit squares in a rectangle $(8, 12)$. For an arbitrary $k \geq 3$, the centrally symmetric packing in the upper half of a rectangle $(2k, 2k + 4)$ consists of 2 staircases. A staircase with orientation $(1,0)$ having $\frac{k(k+1)}{2}$ unit squares, and a staircase with orientation $(x_1, y_1) = \left(\frac{4k^2-1}{4k^2+1},\; \frac{4k}{4k^2+1}\right)$ that has $\frac{(3k-1)(k+2)}{2}$ unit squares. The top vertex of $S_{k+1}$ has ordinate

$$y_{k+1} = -\frac{4k^2}{4k^2 - 1} + (k + 2)\frac{4k^2 + 1}{4k^2 - 1} + (k - 1)\frac{4k}{4k^2 + 1}$$

$$< -\frac{4k^2}{4k^2 - 1} + (k + 2)\frac{4k^2 + 1}{4k^2 - 1} + (k - 1)\frac{4k}{4k^2 - 1} = k + 2 - \frac{2(k - 2)}{4k^2 - 1} < k + 2,$$

i.e., $S_{k+1}$ is in rectangle $(2k, 2k + 4)$. The top vertex of $S_0$ has ordinate

$$\frac{4k^2}{4k^2 - 1} + \frac{4k^2 - 1}{4k^2 + 1} = 2 + \frac{1}{4k^2 - 1} - \frac{2}{4k^2 + 1} < 2,$$

i.e., $S_0$ does not intersect the staircase with orientation $(1,0)$. Each square $S_j$, $1 \leq j \leq k$ intersects the vertical line $x = k - j$ in the point

$$\left(k - j,\; j \cdot \frac{1 - x_1}{x_1 y_1} + (k - j)\frac{y_1}{x_1} + \frac{j}{x_1}\right).$$

The ordinate of this point satisfies

$$j \cdot \frac{1 - x_1}{x_1 y_1} + (k - j)\frac{y_1}{x_1} + \frac{j}{x_1} = 1 + j + \frac{1}{2} \cdot \frac{j \cdot (-4k^2 + 4k + 1) + 2k}{k(4k^2 - 1)} < 1 + j,$$

i.e., none of the $S_j$, $1 \leq j \leq k$ intersects the staircase with orientation $(1,0)$. We see that there is a positive distance between the two staircases. Therefore, this packing is squeezable. The lemma is proved.

> *[Figure 5: Squeezable packing of $4k^2 + 6k - 2$ unit squares in a rectangle $(2k, 2k + 4)$ -- shows centrally symmetric packing with labeled squares $S_0$, $S_1$, $S_j$, $S_{k+1}$ and horizontal lines $y = 2$, $y = j+1$, $y = k+2$]*

## 3 Improved squeezable packing of some squares

As mentioned in the introduction, in [3] Nagamochi mistakebly says that in [2] it is proved that

$$s(n^2 - n) < n \quad \forall n \geq 17. \tag{4}$$

Thus he implicitly formulates the conjecture (4). For the proof of this conjecture we use lemma 1 as follows.

For even $n \geq 14$ we use Figure 1 with rectangles $A = (12, 6)$, $B = (n - 10, n - 6)$, $C = (10, n - 6)$, $D = (n - 12, 6)$.

For odd $n \geq 13$ we use Figure 1 with rectangles $A = (10, 5)$, $B = (n - 9, n - 5)$, $C = (9, n - 5)$, $D = (n - 10, 5)$.

Thus the conjecture (4) is proved for $n \geq 13$.

For the proof of this conjecture for $n = 12$ see Figure 6.

> *[Figure 6: Squeezable packing of 132 unit squares in a square (12,12) -- shows arrangement with labeled squares S1--S18 and points P0--P11]*

The packing in Figure 6 is obtained from the squeezable packing in rectangles $(8,4)$, $(5,10)$. In the packing in $(5,10)$ we tilt the angular squares $S_1$, $S_2$ by an angle $\arcsin(10/26)$ so that the bottom vertex of $S_1$ has an integer $y$-coordinate and $S_2$ has intruded space in the rectangle $(8,4)$. From the packing in $(8,4)$ we remove two right top squares and move to the left by $1/20$ unit squares tilted by an angle $\arcsin(8/17)$ so that the bottom vertex of $S_3$ is on the side of $S_4$. The small distance between $S_2$ and $S_5$ makes the packing in Figure 6 squeezable.

Thus we have proved that

$$s(n^2 - n) < n \quad \forall n \geq 12.$$

To evaluate $\delta((12, 12), 132)$, take $\delta = 0.002$. The origin is in the right bottom vertex of the integer rectangle $(7, 8)$. The bottom side of $(12,12)$ has $y$-coordinate $-4 + \delta$, the right side of $(12,12)$ has $x$-coordinate $5 - \delta$.

Table 2 contains the calculations.

| Object | Formulae or system of equations | Numerical value |
|---|---|---|
| $\delta$ | | $0.002$ |
| Orientation $(x_1, y_1)$ of stack $(4,1)$ | $y_1^2 + x_1^2 = 1$, $y_1 + 4x_1 = 4 - \delta$ | $(0.881413748866, 0.4723450045357421)$ |
| $P_0$ | $P_0 = (4/x_1 - 1/y_1 + x_1/y_1 - 5,\; 0)$ | $(-0.712894713, 0)$ |
| Orientation $(x_2, y_2)$ of stack $(5,1)$ | $y_2^2 + x_2^2 = 1$, $5y_2 + x_2 = 5 - \delta$ | $(0.386451637219073\ldots, 0.9223096725561\ldots)$ |
| $P_1 = (P_{1x}, P_{1y})$ | $P_1 = ((2 - 2x_2 - \delta) \cdot y_1/x_1 + 2y_2,\; -2 + \delta) + P_0$ | $(1.788247541, -1.998)$ |
| Lower ordinate of intersection $S_2$ with line $x = 0$ | $Y_1 = P_{1y} + P_{1x} \cdot \frac{x_2}{y_2}$ | $-1.248716749$ |
| Orientation $(x_3, y_3)$ of square $S_6$ | $x_3^2 + y_3^2 = 1$; <!-- GARBLED: geometric constraint formula for (x3,y3) orientation unrecoverable from extraction --> | $(0.1523435\ldots, 0.98832760\ldots)$ |
| $P_2$ | $P_2 = (x_3 + y_3,\; 4 - x_3)$ | $(1.140671137, 3.847656465)$ |
| $P_3$ | $P_3 = (x_2 + 2y_2,\; Y_1 + 5/y_2 + y_2 - 2x_2)$ | $(2.231070982, 4.321862330)$ |
| Orientation $(x_4, y_4)$ of square $S_9$ | $x_4^2 + y_4^2 = 1$, $\langle P_3 - (1, 4), (y_4, -x_4) \rangle = 1$ | $(0.39947627\ldots, 0.9167435347\ldots)$ |
| $P_4$ | $P_4 = \left(1,\; \frac{6}{y_2} + \frac{(P_{1x} - 1)\, x_2}{y_2} - 2 + \delta + \frac{1 - y_2}{x_2 y_2}\right)$ | $(1, 5.055655408)$ |
| $P_5$ | $P_5 = P_4 + (x_2 + y_2,\; y_2 - x_2)$ | $(2.30876131, 5.5915134434)$ |
| $P_6$ | $\langle P_6 - P_2, (x_4, y_4) \rangle = 1$; $\langle P_6 - P_4, (y_2, -x_2) \rangle = 1$ | $(1.897035430423, 4.608883990)$ |
| $P_7$ | $P_7 = P_6 + (x_2 + y_2,\; y_2 - x_2)$ | $(3.20579674042318, 5.14474202553891)$ |
| $P_8$ | $P_8 = P_3 + (2y_2,\; 2/y_2 - 2x_2)$ | $(4.075690327, 5.717428128)$ |
| Orientation $(x_5, y_5)$ of squares $S_{14}$, $S_{15}$ | $x_5^2 + y_5^2 = 1$, $\langle P_8 - (2, 6), (y_5, -x_5) \rangle = 2$ | $(0.4235421115\ldots, 0.905876415\ldots)$ |
| $P_9 = (P_{9x}, P_{9y})$ | $P_9 = \langle P_5, (x_5, y_5) \rangle \cdot (x_5, y_5) + \langle (2, 6), (-y_5, x_5) \rangle \cdot (-y_5, x_5) + (x_5 + y_5,\; y_5 - x_5)$ | $(3.22807975740513, 6.26558985540152)$ |
| $P_{10} = (P_{10x}, P_{10y})$ | $P_{10} = \langle P_7, (x_5, y_5) \rangle \cdot (x_5, y_5) + \langle (2, 6), (-y_5, x_5) \rangle \cdot (-y_5, x_5) + (x_5 + 2y_5,\; y_5 - 2x_5)$ | $(4.12345766036105, 5.81959341362795)$ |
| $P_{11} = (P_{11x}, P_{11y})$ | $P_{11} = (4 - \delta,\; 7)$ | $(3.998, 7)$ |
| Distance between $P_{11}$ and segment $[P_9, P_{10}]$ | $\dfrac{(P_{9y}-P_{10y})(P_{11x}-P_{9x}) - (P_{9x}-P_{10x})(P_{11y}-P_{9y})}{\sqrt{(P_{9y}-P_{10y})^2+(P_{9x}-P_{10x})^2}}$ | $1.000648944\ldots$ |

**Table 2:** Calculations for $\delta = 0.002$.

Calculations with $\delta = .0021$ give the distance $0.9999866543$ between the bottom left vertex of $S_{18}$ and the segment $[P_9, P_{10}]$. The bisection method gives the evaluation $\delta((12, 12), 132) > 0.00209798269$, i.e., $s(132) < 11.99790201731$.

Analogous calculations give evaluations

$$\delta((5, 10), 43) > 0.0009652493, \quad \delta((5, 9), 38) > 0.020403$$

$$\delta((13, 13), 156) > 0.0059576, \quad s(156) < 12.9940424.$$

Calculations with $C = (10, 8)$, $D = (3, 6)$, $A = (11, 6)$, $B = (4, 8)$ in Figure 1 give

$$\delta((14, 14), 182) > 0.01681735886, \quad s(14^2 - 14) < 13.98318264114.$$

For the square $(15, 15)$ we have $\delta((15, 15), 210) \geq \min(\delta((5, 9), 38), \delta((11, 6), 58)) > 0.01681735886$, i.e., $s(210) < 14.98318264114$.

For the square $(16, 16)$ we have $\delta((16, 16), 241) > \min(\delta((5, 10), 43), \delta((12, 6), 64)) > 0.0009652493$, i.e., $s(16^2 - 15) < 15.9990347507$.

More careful analysis when we use the space between rectangles $(5,10)$ and $(12,6)$ gives

$$\delta((16, 16), 241) > 0.00404996, \quad \text{i.e.,} \quad s(16^2 - 15) < 15.99595004.$$

Calculations with $A = (12, 6)$, $B = (6, 11)$, $C = (11, 11)$, $D = (5, 6)$ give

$$\delta((17, 17), 17^2 - 16) > 0.0049082317748, \quad s(17^2 - 16) < 16.9950917682252.$$

Notice that this squeezable packing of a square $(17,17)$ contains one unit square more than in [2].

Calculations with $A = (13, 6)$, $B = (6, 12)$, $C = (12, 12)$, $D = (5, 6)$ give

$$\delta((18, 18), 18^2 - 17) \geq 0.0049082317748, \quad s(18^2 - 17) < 17.9950917682252.$$

Table 4 contains the evaluations of the squeezing values and the upper bounds of $s(n)$ for new $n$.

| $n$ | $s(n)$ | $\delta((\lceil s(n) \rceil, \lceil s(n) \rceil), n)$ |
|---|---|---|
| $132$ | $s(12^2 - 12) < 11.99790201731$ | $\delta((12, 12), 132) > 0.00209798269$ |
| $156$ | $s(13^2 - 13) < 12.9940424$ | $\delta((13, 13), 156) > 0.0059576$ |
| $182$ | $s(14^2 - 14) < 13.98318264114$ | $\delta((14, 14), 182) > 0.01681735886$ |
| $210$ | $s(15^2 - 15) < 14.98318264114$ | $\delta((15, 15), 210) > 0.01681735886$ |
| $241$ | $s(16^2 - 15) < 15.99595004$ | $\delta((16, 16), 241) > 0.00404996$ |
| $273$ | $s(17^2 - 16) < 16.9950917682252$ | $\delta((17, 17), 17^2 - 16) > 0.0049082317748$ |
| $307$ | $s(18^2 - 17) < 17.9950917682252$ | $\delta((18, 18), 18^2 - 17) > 0.0049082317748$ |

**Table 4.** Evaluations of squeezing values and upper bounds of $s(n)$ for new $n$.

## References

[1] P. Erdos and R. L. Graham, On packing squares with equal squares, *J. Combin. Theory Ser. A*, 19 (1975) 119--123.

[2] E. Friedman, Packing unit squares in squares: A survey and new results, *Elect. J. Combin.*, Dynamic Survey # DS7 (1998, last version 2009). DOI: https://doi.org/10.37236/28

[3] Nagamochi H., Packing unit squares in a rectangle, *Elect. J. Combin.*, 12 (2005), #R37. DOI: https://doi.org/10.37236/1934

[4] Shuang Wang, Tian Dong, Jiamin Li, A New Result on Packing Unit Squares into a Large Square, arXiv:1603.02368 [math.CO]
