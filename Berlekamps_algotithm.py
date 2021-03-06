# -*- coding: utf-8 -*-
"""berlekamp(1).ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/15ukfbuHJpj9f75LpAm2TmAIsTXk5xM1Q
"""

from sympy import pdiv, div, poly, degree, Poly
from sympy.abc import x,y
from sympy import Symbol, ZZ, GF, LC
from sympy.solvers import solve
from sympy.solvers.diophantine import diophantine
from sympy.matrices import Matrix, eye, zeros, ones, diag, GramSchmidt
from sympy.matrices.dense import casoratian
from sympy.matrices.matrices import _iszero, _find_reasonable_pivot, _simplify
import numpy as np


p = 7
m = poly(x**4+3*x-2, domain=GF(p, symmetric=False))
size_m = m.degree()
print('Исходный многочлен:',m)
#формирование матрицы q
q = []
for i in range(0, m.degree() ):
    h = poly(x**(p*i),x, domain=GF(p, symmetric=False))
    r = h % m
    print('h[%i] = '%i,h,'r[%i] = '%i,r)
    new_arr = r.all_coeffs()
    q.append([0]*(m.degree()-len(new_arr)))
    q[i].extend(new_arr)
print('Матрица Q:')
for i in q:
  print(i)

a=Matrix(q[::-1]).transpose()-eye(4)
a=list(a)
for i in range(0, len(a)):
        a[i]= poly(a[i],x, domain=GF(p, symmetric=False))
a = Matrix(size_m ,size_m, a)       

'''
Алгоритм нахождения ядра
'''
arr=a
rows, cols = arr.rows, arr.cols
mat = list(arr)
iszerofunc = _iszero
simpfunc = _simplify
zero_above = True
def get_col(i):
    return mat[i::cols]

def row_swap(i, j):
    mat[i*cols:(i + 1)*cols], mat[j*cols:(j + 1)*cols] = \
        mat[j*cols:(j + 1)*cols], mat[i*cols:(i + 1)*cols]

def cross_cancel(a, i, b, j):
    """Does the row op row[i] = a*row[i] - b*row[j]"""
    q = (j - i)*cols
    for pit in range(i*cols, (i + 1)*cols):
        mat[pit] = a*mat[pit] - b*mat[pit + q]
piv_row, piv_col = 0, 0
pivot_cols = []
swaps = []

while piv_col < cols and piv_row < rows:
    pivot_offset, pivot_val, \
    assumed_nonzero, newly_determined = _find_reasonable_pivot(
        get_col(piv_col)[piv_row:], iszerofunc, simpfunc)
    
    # _find_reasonable_pivot may have simplified some things
    # in the process.  Let's not let them go to waste
    for (offset, val) in newly_determined:
        offset += piv_row
        mat[offset*cols + piv_col] = val

    if pivot_offset is None:
        piv_col += 1
        continue

    pivot_cols.append(piv_col)
    if pivot_offset != 0:
        row_swap(piv_row, pivot_offset + piv_row)
        swaps.append((piv_row, pivot_offset + piv_row))

    # if we aren't normalizing last, we normalize
    # before we zero the other rows
   

    # zero above and below the pivot
    for row in range(rows):
        # don't zero our current row
        if row == piv_row:
            continue
        # don't zero above the pivot unless we're told.
        if zero_above is False and row < piv_row:
            continue
        # if we're already a zero, don't do anything
        val = mat[row*cols + piv_col]
        if iszerofunc(val):
            continue

        cross_cancel(pivot_val, row, val, piv_row)
    piv_row += 1
#poly(1,x, domain=GF(p, symmetric=False))
#if normalize_last is True and normalize is True:
for piv_i, piv_j in enumerate(pivot_cols):
    pivot_val = mat[piv_i*cols + piv_j]
    mat[piv_i*cols + piv_j] = poly(1,x, domain=GF(p, symmetric=False))
    for pit in range(piv_i*cols + piv_j + 1, (piv_i + 1)*cols):
        mat[pit] = div(mat[pit], pivot_val)[0]

#print(mat)
q=Matrix(rows, cols, mat)

pivots= tuple(pivot_cols)
reduced = q
free_vars = [i for i in range(q.cols) if i not in pivots]
#p=13
basis = []
for free_var in free_vars:
    # for each free variable, we will set it to 1 and all others
    # to 0.  Then, we will use back substitution to solve the system
    vec = [poly(0,x, domain=GF(p, symmetric=False))]*q.cols
    vec[free_var] = poly(1,x, domain=GF(p, symmetric=False))
    for piv_row, piv_col in enumerate(pivots):
        vec[piv_col] -= reduced[piv_row, free_var]
    basis.append(vec)
k=[Matrix(q.cols, 1, b) for b in basis]
#g=k[0]
k,g
'''
print(k[1][0].coeffs()[0])
print('Ядро:')
ker = []
for i in k:
  print('Вектор ')
  for j in i:
    print(j.coeffs()[0])
'''
for i in range(1,p):
    c = list(k[0]*poly(i,x, domain=GF(p, symmetric=False)))
    if c[0]==1:
        #g = k[0]*poly(i,x, domain=GF(p, symmetric=False))
        g = list(k[0]*poly(i,x, domain=GF(p, symmetric=False)))
        break;
for i in range(len(g)):
    g[i] = LC(g[i])
#g=Matrix(len(g),1,g)
#g= list(g)
g = Poly(g, x, domain=GF(p, symmetric=False))
print('g = ',g)
dm = []
for i in range(p):
    d = m.gcd(g- poly(i, x, domain=GF(p, symmetric=False)))
    dm.append(d)
    print('d[%s] = '%i,d)
print('Рузультат:', dm[2]*dm[4])



from sympy import pdiv, div, poly, degree, Poly
from sympy.abc import x,y
from sympy import Symbol, ZZ, GF, LC
from sympy.solvers import solve
from sympy.solvers.diophantine import diophantine
from sympy.matrices import Matrix, eye, zeros, ones, diag, GramSchmidt
from sympy.matrices.dense import casoratian
from sympy.matrices.matrices import _iszero, _find_reasonable_pivot, _simplify
import numpy as np
a = []
a.append( poly(3,x, domain=GF(p, symmetric=False)))
a.append( poly(1,x, domain=GF(p, symmetric=False)))
a.append(poly(2,x, domain=GF(p, symmetric=False)))
a.append(poly(4,x, domain=GF(p, symmetric=False)))
a.append(poly(-2,x, domain=GF(p, symmetric=False)))
a.append(poly(1,x, domain=GF(p, symmetric=False)))
a.append(poly(7,x, domain=GF(p, symmetric=False)))
a.append(poly(-1,x, domain=GF(p, symmetric=False)))
a.append(poly(3,x, domain=GF(p, symmetric=False)))
print(len(a))

a = Matrix(3,3, a)
for i in Matrix(3 ,3, a) :
 print(i)


'''
Алгоритм нахождения ядра
'''
arr=a
rows, cols = arr.rows, arr.cols
mat = list(arr)
iszerofunc = _iszero
simpfunc = _simplify
zero_above = True
def get_col(i):
    return mat[i::cols]

def row_swap(i, j):
    mat[i*cols:(i + 1)*cols], mat[j*cols:(j + 1)*cols] = \
        mat[j*cols:(j + 1)*cols], mat[i*cols:(i + 1)*cols]

def cross_cancel(a, i, b, j):
    """Does the row op row[i] = a*row[i] - b*row[j]"""
    q = (j - i)*cols
    for pit in range(i*cols, (i + 1)*cols):
        mat[pit] = a*mat[pit] - b*mat[pit + q]
piv_row, piv_col = 0, 0
pivot_cols = []
swaps = []

while piv_col < cols and piv_row < rows:
    pivot_offset, pivot_val, \
    assumed_nonzero, newly_determined = _find_reasonable_pivot(
        get_col(piv_col)[piv_row:], iszerofunc, simpfunc)
    
    # _find_reasonable_pivot may have simplified some things
    # in the process.  Let's not let them go to waste
    for (offset, val) in newly_determined:
        offset += piv_row
        mat[offset*cols + piv_col] = val

    if pivot_offset is None:
        piv_col += 1
        continue

    pivot_cols.append(piv_col)
    if pivot_offset != 0:
        row_swap(piv_row, pivot_offset + piv_row)
        swaps.append((piv_row, pivot_offset + piv_row))

    # if we aren't normalizing last, we normalize
    # before we zero the other rows
   

    # zero above and below the pivot
    for row in range(rows):
        # don't zero our current row
        if row == piv_row:
            continue
        # don't zero above the pivot unless we're told.
        if zero_above is False and row < piv_row:
            continue
        # if we're already a zero, don't do anything
        val = mat[row*cols + piv_col]
        if iszerofunc(val):
            continue

        cross_cancel(pivot_val, row, val, piv_row)
    piv_row += 1
#poly(1,x, domain=GF(p, symmetric=False))
#if normalize_last is True and normalize is True:
for piv_i, piv_j in enumerate(pivot_cols):
    pivot_val = mat[piv_i*cols + piv_j]
    mat[piv_i*cols + piv_j] = poly(1,x, domain=GF(p, symmetric=False))
    for pit in range(piv_i*cols + piv_j + 1, (piv_i + 1)*cols):
        mat[pit] = div(mat[pit], pivot_val)[0]
for i in mat:
  print(' Что-то временное', i)
q=Matrix(rows, cols, mat)

pivots= tuple(pivot_cols)
reduced = q
free_vars = [i for i in range(q.cols) if i not in pivots]
#p=13
basis = []
for free_var in free_vars:
    # for each free variable, we will set it to 1 and all others
    # to 0.  Then, we will use back substitution to solve the system
    vec = [poly(0,x, domain=GF(p, symmetric=False))]*q.cols
    vec[free_var] = poly(1,x, domain=GF(p, symmetric=False))
    for piv_row, piv_col in enumerate(pivots):
        vec[piv_col] -= reduced[piv_row, free_var]
    basis.append(vec)
k=[Matrix(q.cols, 1, b) for b in basis]
print("Ядро")
print(basis)
#g=k[0]
#k,g
