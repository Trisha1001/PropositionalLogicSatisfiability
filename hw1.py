"""This is a sample file for hw1. 
It contains the function that should be submitted,
except all it does is output a random value out of the
possible values that are allowed.
- Dr. Licato"""

import random
import re
import collections
from hashlib import new

keyWords = ['OR','AND','NOT','IF']
toReturn = ""


"""F: A string which is an S-expression of a PC formula. You can assume:
The operators used are IF,AND,OR,and NOT. 
All operators (except for NOT) have two arguments
All propositional symbols will be lower-case alphanumberic strings
All formulae are well-formed (UNDERGRADUATE STUDENTS ONLY)

Returns either a string or integer: 
“E” – If the formula was not well-formed (GRADUATE STUDENTS ONLY)
“T” – If the formula is a tautology,
“U” – If the formula is unsatisfiable, else:
i – An integer showing the number of rows that are satisfiable
"""

def proveFormula(F):
	toReturn = ""
	wff = checkFormula(F)
	if wff == "E":
		toReturn = wff
	else:
		operands = getOperandCount(F)
		operandsCount = len(operands)
		iterationCount = 2**(len(operands))
		count = 0
		c=0
		operandsVal =[]
		""" Iteration over the truthtable. Rows count in the truth table is 2^(operand count). We calculate this count in above steps. Here we denote false as 0 and True as 1"""
		while(count !=iterationCount):
			operandsVal=dec_to_bin(operandsCount,count)
			dictVal = dict(zip(operands,operandsVal))
			result = getValueofFormula(F,dictVal)
			if int(result) ==0:
				c=c+1
			count = count +1
		if c ==0:
			toReturn ="T"
		elif c<iterationCount:
			toReturn=iterationCount-c
		elif c==iterationCount:
			toReturn = "U"	
	return toReturn

""" CheckFormula - to check if the input is well formed formula or not. If formula is not well formed, it returns E"""
def checkFormula(F):
	global checkFormulaResult;
	checkFormulaResult =""
	def nextsym():
		nonlocal current_token
		if tokens:
			current_token = tokens.pop(0)
		return
	
	def expect(token):
		if accept(token):
			return True
		else:
			global checkFormulaResult;
			checkFormulaResult = "E"
		
		return False
	def accept(token):
		nonlocal current_token
		if current_token == token:
			nextsym()
			return True
		return False
	
	def atom():
		nextsym()
		return
	
	
	def function():
		nonlocal current_token
		if current_token == '(' or current_token == ')':
			statement()
		else:
			atom()
		return
	
	def statement():
		expect('(')
		if accept("OR"):
			function()
			function()
		elif accept("AND"):
			function()
			function()
		elif accept("NOT"):
			function()
		elif accept("IF"):
			function()
			function()
		expect(')')
		return
	
	
	def expression():
		nextsym()
		statement()
		return
	
	tokens = [i for i in re.split(r'([\(\)\,])|(\"[^\"]*\")|\s',F) if i]
	if any(ext in tokens for ext in keyWords) == False:
		if len(tokens) ==1 and tokens[0] !="(" and tokens[0] !=")":
			return ""
		else:
			checkFormulaResult = "E"
	else:
		current_token = tokens[0]
		expression()	
	return checkFormulaResult

""" This function is to het the number of operand. This count later used to build the truth table """
def getOperandCount(F):
	tokens = [i for i in re.split(r'([\(\)\,])|(\"[^\"]*\")|\s',F) if i]
	uniqueList = [x for x, count in collections.Counter(tokens).items() if count >= 1]
	uniqueList = [e for e in uniqueList if e not in ("OR","AND","IF","NOT","(",")")]
	return uniqueList

""" To get the value of the formula by putting value according to truth table"""
def getValueofFormula(F,dictVal):
	tokens = [i for i in re.split(r'([\(\)\,])|(\"[^\"]*\")|\s',F) if i]
	newtokens = tokens
	for n,i in enumerate(newtokens):
		if i == "(" or i ==")" or i in keyWords:
			continue
		else:
			if i in dictVal:
				newtokens[n] = dictVal.get(i)
	
	val = getOperations(newtokens)
	return val

""" Depending upon truth value get the final true/false from the formula. This function iterate the formula until it gets the result."""
def getOperations(newtokens):
	
	def callOR(x,y):
		z=0
		if x==0 and y ==0:
			z=0
		elif x==0 and y==1:
			z=1
		elif x==1 and y==0:
			z=1
		elif x==1 and y==1:
			z=1
		return z
	def callAND(x,y):
		z=0
		if x==0 and y ==0:
			z=0
		elif x==0 and y==1:
			z=0
		elif x==1 and y==0:
			z=0
		elif x==1 and y==1:
			z=1
		return z
	def callIF(x,y):
		z=0
		if x==0 and y ==0:
			z=1
		elif x==0 and y==1:
			z=1
		elif x==1 and y==0:
			z=0
		elif x==1 and y==1:
			z=1
		return z
	
	def callNOT(x):
		z=0
		if x==0:
			z=1
		elif x==1:
			z=0
		return z
	
	while(len(newtokens) >1):
		for (j,k) in enumerate(newtokens):
			if k in keyWords:
				if k=="NOT":
					if newtokens[j+1] != "(":
						p=callNOT(int(newtokens[j+1]))
						newtokens[j-1]=p
						del(newtokens[j:j+3])
				else:
					if newtokens[j+1] != "(" and newtokens[j+2] !="(":
						if k == "OR":
							newtokens[j-1]=callOR(int(newtokens[j+1]),int(newtokens[j+2]))
							del(newtokens[j:j+4])
					
						elif k =="AND":
							newtokens[j-1]=callAND(int(newtokens[j+1]),int(newtokens[j+2]))
							del(newtokens[j:j+4])
						elif k == "IF":
							newtokens[j-1]=callIF(int(newtokens[j+1]),int(newtokens[j+2]))
							del(newtokens[j:j+4])
	
	return newtokens.pop(0)

""" This to convert decimal number to binary. The bit count in binary depending upon the number of literal in the formula"""
def dec_to_bin(operandsCount,n):
	bits = []
	bits.append(str(0 if n%2 == 0 else 1))
	while n > 1:
		n = n // 2
		bits.append(str(0 if n%2 == 0 else 1))
	bits.reverse()
	while (len(bits)<operandsCount):
		bits.insert(0, 0)
	return bits
