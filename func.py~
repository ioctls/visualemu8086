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
	print ""
	for item in stack:
		print item
		
def extract(string):
	#MODE 0 -> Registere
	#MODE 1 -> Literal value
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
						#we can maintain a list of values instead of a list of variables	
	if(moded == 1):
		pass
	if(modes == 1 and moded == 0):
		reg[lookup3[vald]].val = vals
	
	if(lookup3[vald] < 10) :
		reg[lookup3[vald]].update()
	else :
		reg[lookup3[vald]].valoverride(reg[lookup3[vald]].val)		
	
		
	return
		
def finc(dest):						#manage ax, bx, cx, dx in another list, split values? hex?
	(vald,moded) = extract(dest)
	if(moded == 1):
		declaresynerror()
		return
	reg[lookup3[vald]].val += 1
	if(lookup3[vald] < 9) :
		reg[lookup3[vald]].update()
	else : 
		reg[lookup3[vald]].valoverride(reg[lookup3[vald]].val)	
	
	#Updating the Flag Register
	if(lookup3[vald] < 9) :
		#pass
		#FOR Overflow
		if(reg[lookup3[vald]].val == 128) :
			flags.b.overflow = 1
			print "Overflow occured Oerflow bit = ", flags.b.overflow
	elif(reg[lookup3[vald]].val == 32768) :
		flags.b.overflow = 1 	
		print "Overflow occured Oerflow bit = ", flags.b.overflow	
	if(reg[lookup3[vald]].val == 0) :
		flags.b.carry = 1
		flags.b.zero  = 1 
		flags.b.overflow = 1
		print "Carry gen", flags.b.carry
		print "VAlue in reg is zero", flags.b.zero
		print "Overflow occured Oerflow bit = ", flags.b.overflow
	temp = reg[lookup3[vald]].val
	c = 0
	ac = 0
	while (temp > 0) :
		if(temp & 1 == 1):
			c = c + 1
		temp = temp >> 1
	if(c % 2 == 0) :
		flags.b.parity = 1
		print "Parity even so Parity bit set to 1", flags.b.parity
						
	temp = reg[lookup3[vald]].val - 1
	for i in range(4) :
		if(temp & 1 == 1) :
			ac = ac + 1
		temp = temp >> 1	
	if(ac == 4) :
		flags.b.ac = 1
		print "Auxiallary Carry ocuured" 						
 			
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
	if(lookup3[vals] < 13):
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
		if((lookup3[vald] < 10 and lookup3[vals] < 10) or (lookup3[vald] > 16 and lookup3[vals] > 16)) :
			reg[lookup3[vald]].val ^= reg[lookup3[vals]].val
		else: 
			declaresynerror()
	if(lookup3[vald] < 10):
		pass
	else: 
		reg[lookup3[vald]].valoverride(reg[lookup3[vald]].val)			
				
	
	temp = reg[lookup3[vald]].val
	c = 0
	ac = 0
	while (temp > 0) :
		if(temp & 1 == 1):
			c = c + 1
		temp = temp >> 1
	if(c % 2 == 0) :
		flags.b.parity = 1
		print "Parity even so Parity bit set to 1", flags.b.parity
	if(reg[lookup3[vald]].val == 0):
		flags.b.zero = 1
		print "Value is zero"		
		
	
		
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
		
	temp = reg[lookup3[vald]].val
	c = 0
	ac = 0
	while (temp > 0) :
		if(temp & 1 == 1):
			c = c + 1
		temp = temp >> 1
	if(c % 2 == 0) :
		flags.b.parity = 1
		print "Parity even so Parity bit set to 1", flags.b.parity
	if(reg[lookup3[vald]].val == 0):
		flags.b.zero = 1
		print "Value is zero"
				
		
def fdec(dest):
	(vald,moded) = extract(dest)
	if(moded == 1):
		declaresynerror()
		return
	#if(reg[lookup3[vald]].val == 0):
	#	if(lookup3[vald] >= 16):
	#		reg[lookup3[vald]].val = 65535
	#		declareoverflow()
	#		return
	#	if(lookup3[vald] < 13):
	#		reg[lookup3[vald]].val = 255
	#		declareoverflow()
	#		return
	reg[lookup3[vald]].val -= 1
	
	#Updating the Flag Register
	if(lookup3[vald] < 9) :
		#pass
		#FOR Overflow
		if(reg[lookup3[vald]].val == 127) :
			flags.b.overflow = 1
			print "Overflow occured Oerflow bit = ", flags.b.overflow
	elif(reg[lookup3[vald]].val == 32767) :
		flags.b.overflow = 1 	
		print "Overflow occured Oerflow bit = ", flags.b.overflow	
	if(reg[lookup3[vald]].val == -1) :
		flags.b.carry = 1
		flags.b.overflow = 1
		print "Carry gen", flags.b.carry
		print "VAlue in reg is zero", flags.b.zero
		print "Overflow occured Oerflow bit = ", flags.b.overflow
	temp = reg[lookup3[vald]].val
	c = 0
	ac = 0
	while (temp > 0) :
		if(temp & 1 == 1):
			c = c + 1
		temp = temp >> 1
	if(c % 2 == 0) :
		flags.b.parity = 1
		print "Parity even so Parity bit set to 1", flags.b.parity
						
	temp = reg[lookup3[vald]].val + 1
	for i in range(4) :
		if(temp & 1 == 1) :
			ac = ac + 1
		temp = temp >> 1	
	if(ac == 4) :
		flags.b.ac = 1
		print "Auxiallary Carry ocuured" 						
 	
 	if(lookup3[vald] < 10) : 		
		reg[lookup3[vald]].update()
	else :
		reg[lookup3[vald]].valoverride(reg[lookup3[vald]].val)	
	
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
		#we can maintain a list of values instead of a list of variables	
	#if(moded == 1):		#bro, 
		#pass
	if(modes == 1 and moded == 0):
		reg[lookup3[vald]].val -= vals	#reg[lookup3[vald]] -
	
	
	#Zero
	if(reg[lookup3[vald]].val == 0) :
		flags.b.zero = 1
		print "The value in reg is zero"	
	
	temp_0 = reg[lookup3[vald]].val
	c = 0
	ac = 0
	while (temp_0 > 0) :
		if(temp_0 & 1 == 1):
			c = c + 1
		temp_0 = temp_0 >> 1
	if(c % 2 == 0) :
		flags.b.parity = 1
		print "Parity even so Parity bit set to 1", flags.b.parity
					
	if(modes == 1 and moded == 0):					
		temp = reg[lookup3[vald]].val + vals
	else:
		temp = reg[lookup3[vald]].val + reg[lookup3[vals]].val
	
	temp_0 = reg[lookup3[vald]].val
	
	if(lookup3[vald] < 10):	
		if((temp > 127  and temp_0 < 127) or (temp > 0 and temp < 127 and temp_0 < 0)):
			flags.b.overflow = 1
			print "Overflow occured"
	else:
		if((temp > 32767  and temp_0 <= 32767) or (temp >= 0 and temp <= 32767 and ((temp_0 < 0) or temp_0 > 32767))
			or (temp > 32767 and temp_0 < 0)) :
			flags.b.overflow = 1
			print "Overflow Ocuured"
	
	if(temp >= 0 and temp_0 < 0):
			flags.b.carry = 1
			print "Carry generated"		
			
			
	for i in range(4) :
		if(temp & 1 == 1) :
			ac = ac + 1
		temp = temp >> 1	
	if(ac == 4) :
		flags.b.ac = 1
		print "Auxiallary Carry ocuured"
	
	if(lookup3[vald] < 10):
		reg[lookup3[vald]].update()
	else:
		reg[lookup3[vald]].valoverride(reg[lookup3[vald]].val)	
		 
		
def fadd(dest, source) :
	(vald, moded) = extract(dest)
	(vals, modes) = extract(source)
	#destination is memory, do later
	if(modes == 0 and moded == 0):
		reg[lookup3[vald]].val += reg[lookup3[vals]].val	#reg[lookup3[vald]] -
		#we can maintain a list of values instead of a list of variables	
	#if(moded == 1):		#bro, 
		#pass
	if(modes == 1 and moded == 0):
		reg[lookup3[vald]].val += vals	#reg[lookup3[vald]] -
	
	
	temp_0 = reg[lookup3[vald]].val
	c = 0
	ac = 0
	
					
	if(modes == 1 and moded == 0):					
		temp = reg[lookup3[vald]].val - vals
	else:
		temp = reg[lookup3[vald]].val - reg[lookup3[vals]].val
	
	temp_0 = reg[lookup3[vald]].val
	
	
	#FOr Overflow And Carry
	if(lookup3[vald] < 10) :
		if(((temp > 127) and (temp_0 < 127)) or ((temp < 127) and (temp_0 > 127))) :
			flags.b.overflow = 1
			print "Overflow occured"
		if(temp_0 > 255):
			flags.b.carry = 1
			print "Carry generated"	
	else:
		if(((temp > 32767 and temp) and (temp_0 > 65535)) or ((temp < 32767) and (temp_0 > 32767))) :
			flags.b.overflow = 1
			print "Overflow occured"
		if(temp_0 > 65536):
			flags.b.carry  = 1
			print "Carry Generated"
			
	
	
	if(lookup3[vald] < 10):
		reg[lookup3[vald]].update()
	else:
		reg[lookup3[vald]].valoverride(reg[lookup3[vald]].val)	
	
	#FOr Zerp			
	if(temp_0 == 0):
		flags.b.zero = 1
		#PRint here	
	
	temp_0 = reg[lookup3[vald]].val	
	while (temp_0 > 0) :
		if(temp_0 & 1 == 1):
			c = c + 1
		temp_0 = temp_0 >> 1
	if(c % 2 == 0) :
		flags.b.parity = 1
		print "Parity even so Parity bit set to 1", flags.b.parity	
	
	for i in range(4) :
		if(temp & 1 == 1) :
			ac = ac + 1
		temp = temp >> 1	
	if(ac == 4) :
		flags.b.ac = 1
		print "Auxiallary Carry ocuured"	
		 				 	
	
	
				
		
listoffunctions = [blank, fhlt, fmov, finc, fpop, fpush, fxor, fsub, fxchg, fmul, fnot, fbor, fand, fdec, fdiv, fadd]
		
