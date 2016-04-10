import sys
import ctypes
import state
from state import * 
from table import *				

def declaresynerror():
	print "You made a syntax error"
	sys.exit("Check your input")
def printstate():
	for item in reg:
		print item.val,
	print "next"
def extract(string):
	if('$' in string):
		#convert into decimal or convert decimal to hex
		value = int(string[:-1]) #remove '$'
		mode = 1 #if(value)
	else: 	#we have either value or registor! how to differentiate? add '$' at the end for values
		value = int(string) #if key
		mode = 0
	return (value, mode)
def fhlt():
	sys.exit("Executed HLT")
def fmov(dest , source):
	(vald, moded) = extract(dest)
	(vals, modes) = extract(source.rstrip())
	#destination is memory, do later
	if(modes == 0 and moded == 0):
		if((lookup3[vals] < 13 and lookup3[vald] >= 13) or (lookup3[vald] < 13 and lookup3[vals] >= 13)):
			declaresynerror()
			print "Size mis-match"
			return
 		reg[lookup3[vald]].val = reg[lookup3[vals]].val
		return					#we can maintain a list of values instead of a list of variables	
	if(moded == 1):
		pass
	if(modes == 1 and moded == 0):
		reg[lookup3[vald]].val = vals
		reg[lookup3[vald]].update()
		return
def finc(dest):						#manage ax, bx, cx, dx in another list, split values? hex?
	(vald,moded) = extract(dest)
	if(moded == 1):
		declaresynerror()
		return
	reg[lookup3[vald]].val += 1
	reg[lookup3[vald]].update()
	return
	
def fpop(dest):
	(vald, moded) = extract(dest)
	if(moded == 1):
		declaresynerror()
		return
	if(lookup3[vald] < 13):
		print "Cant pop 2 bytes in 1 byte register"
		declaresynerror()
	reg[lookup3[vald]].val = stack.pop() 
	return
def fpush(source):
	(vals, modes) = extract(source)
	if(modes == 1):
		declaresynerror()
		#add more stuff for error
	if(lookup3[vald] < 13):
		print "Cant push 1 byte registers"
		declaresynerror()
	stack.append(reg[lookup3[vals]].val)
	return
def fxor(dest, source):
	(vald, moded) = extract(dest)
	(vals, modes) = extract(source)
	if(modes == 1 and moded == 1):
		declaresynerror()
		return
	#do other cases
	if(modes == 0 and moded == 0):
		reg[lookup3[vald]].val ^= reg[lookup3[vals]].val
def blank():
	pass
def fxchg(dest, source):
	(vald, moded) = extract(dest)
	(vals, modes) = extract(source)
	if(modes == 1 and moded == 1):
		declaresynerror()
		return
	#do other cases
	if(modes == 0 and moded == 0):
		if((lookup3[vals] < 13 and lookup3[vald] >= 13) or (lookup3[vald] < 13 and lookup3[vals] >= 13)):
			declaresynerror()
			print "Size mis-match"
			return
		reg[lookup3[vald]].val ^= reg[lookup3[vals]].val
		reg[lookup3[vals]].val ^= reg[lookup3[vald]].val
		reg[lookup3[vald]].val ^= reg[lookup3[vals]].val
		return
def fmul(source):
	a = 17
	b = 2
	c = 20
	(vals, modes) = extract(source)
	if(modes == 1):
		if(vals < 256):
			reg[a].val = reg[b].val*vals
			#reg[17].update()
			reg[a].valoverride(reg[a].val)
			return 				#adjust overflow in classes? there should be no overflow here
		else:
			reg[a].val = reg[a].val*vals
			while(reg[a].val > 65535):
				reg[a].val -= 65536
				reg[c].val += 1
			reg[a].valoverride(reg[a].val)
			reg[c].valoverride(reg[c].val)
			return
	if(modes == 0):
		if(lookup3[vals] < 13):
			reg[a].val = reg[b].val * reg[lookup3[vals]].val
			reg[a].valoverride(reg[a].val)
			return				#no overflow expected, update ah and al too
		if(lookup3[vals] >= 17):
			reg[a].val = reg[a].val*reg[lookup3[vals]].val
			while(reg[a].val > 65535):
				reg[a].val -= 65536
				reg[c].val += 1
			reg[a].valoverride(reg[a].val)
			reg[c].valoverride(reg[c].val)				
			return
def fnot(dest):
	(vald, moded) = extract(dest)
	if(moded == 1):
		declaresynerror()
		return
	if(reg[lookup3[vald]].val <= 15):
		reg[lookup3[vald]].val ^= 15
	elif(reg[lookup3[vald]].val <= 255):
		reg[lookup3[vald]].val ^= 255
	#add more or go sustainable
def fbor(dest, source):
	(vald, moded) = extract(dest)
	(vals, modes) = extract(source)
	if(modes == 1 and moded == 1):
		declaresynerror()
		return
	#do other cases
	if(modes == 0 and moded == 0):
		reg[lookup3[vald]].val |= reg[lookup3[vals]].val
		return
def fand(dest, source):
	(vald, moded) = extract(dest)
	(vals, modes) = extract(source)
	if(modes == 1 and moded == 1):
		declaresynerror()
		return
	#do other cases
	if(modes == 0 and moded == 0):
		reg[lookup3[vald]].val &= reg[lookup3[vals]].val
		return
def fdec(dest):
	(vald,moded) = extract(dest)
	if(moded == 1):
		declaresynerror()
		return
	if(reg[lookup3[vald]].val == 0):
		if(lookup3[vald] >= 16):
			reg[lookup3[vald]].val = 65535
			declareoverflow()
			return
		if(lookup3[vald] < 13):
			reg[lookup3[vald]].val = 255
			declareoverflow()
			return
	reg[lookup3[vald]].val -= 1
	return
def fdiv(source):
	a = 17							#cite! make ax from ah and al for every update of ah and al
	(vals, modes) = extract(source)
	if(modes == 1):
		declaresynerror()
		return
	temp = reg[a].val
	reg[2].val = temp / reg[lookup3[vals]].val
	reg[1].val = temp % reg[lookup3[vals]].val
	return
	#AX, AL
	#al, bl -> ax! how to map?
def fsub(dest, source):
	(vald, moded) = extract(dest)
	(vals, modes) = extract(source)
	#destination is memory, do later
	if(modes == 0 and moded == 0):
		reg[lookup3[vald]].val -= reg[lookup3[vals]].val	#reg[lookup3[vald]] -
		return	#we can maintain a list of values instead of a list of variables	
	#if(moded == 1):		#bro, 
		#pass
	if(modes == 1 and moded == 0):
		reg[lookup3[vald]].val -= vals	#reg[lookup3[vald]] -
		return
		
listoffunctions = [blank, fhlt, fmov, finc, fpop, fpush, fxor, fsub, fxchg, fmul, fnot, fbor, fand, fdec, fdiv]		