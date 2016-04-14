import sys
import ctypes
import state
from state import * 
from table import *				

def declaresynerror():
	print "You made a syntax error"
	sys.exit("Check your input")
	
def printstate():
	print "Reg : ",
	for item in reg:
		print item.val,
	print "\n"
	print "Stack : ",
	for item in stack:
		print item
	print "\n"
	print "Flags : ",
	print flags.b.overflow,
	print flags.b.direction,
	print flags.b.interrupt,
	print flags.b.trap,
	print flags.b.sign,
	print flags.b.zero,
	print flags.b.ac,
	print flags.b.parity,
	print flags.b.carry
	print "\n"


#Wont work Cause it takes care only wen positive are arguments as operations
#This func can be used only for INC operation	
def checkoverflow(key):
	if(key < 9) :
		#pass
		#FOR Overflow					#push this in update()
		if(reg[key].val == 128) :
			flags.b.overflow = 1			#this is Akshay G
	elif(reg[key].val == 32768) :
		flags.b.overflow = 1 	
	if(reg[key].val == 0) :
		flags.b.carry = 1 #Not always for zero
		flags.b.zero  = 1 
		flags.b.overflow = 1 

#Genereic func for every operation Except wen the op does involve and		
def updateacflag(temp):
	ac = 0
	temp -= 1
	for i in range(4) :
		if(temp & 1 == 1) :
			ac = ac + 1
		temp = temp >> 1	
	if(ac == 4) :
		flags.b.ac = 1 						
 	return
 	
def updatedep(plan):
	if(plan <= 2):
		ax.update()
	elif(plan <= 4 and plan > 2):
		bx.update()
	elif(plan <= 6 and plan > 4):
		cx.update()
	elif(plan <= 8 and plan > 6):
		dx.update()
		
def extract(string):
	#MODE 0 -> Register
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
	if(lookup3[vald] < 10):
		reg[lookup3[vald]].update()
		updatedep(lookup3[vald])
	else:
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
		updatedep(lookup3[vald])
	else : 
		reg[lookup3[vald]].valoverride(reg[lookup3[vald]].val)	
	
	#Updating the Flag Register, do for overflow
	#For overflow
	if(reg[lookup3[vald]].val == 128 or reg[lookup3[vald]].val == 32768 or 
		reg[lookup3[vald]].val == 0) :
		flags.b.overflow = 1
	
	if(lookup3[vald] > 16):
		updateacflag(reg[lookup3[vald]].val)
	
	
def fpop(dest):
	(vald, moded) = extract(dest)
	if(moded == 1):
		declaresynerror()
		return
	if(lookup3[vald] < 13):
		print "Cant pop 2 bytes in 1 byte register"
		declaresynerror()
	reg[lookup3[vald]].val = stack.pop()
	reg[lookup3[vald]].valoverride(reg[lookup3[vald]].val)
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
	(vald, moded) = extract(dest)		#check if xor ax, 05 is allowed
	(vals, modes) = extract(source)
	if(modes == 1 and moded == 1):
		declaresynerror()
		return
	#do other cases
	if(modes == 0 and moded == 0):
		if((lookup3[vald] < 10 and lookup3[vals] < 10) or (lookup3[vald] > 16 and lookup3[vals] > 16)) :
			temp_p = reg[lookup3[vald]].val
			temp_a = reg[lookup3[vals]].val
			reg[lookup3[vald]].val ^= reg[lookup3[vals]].val
		else: 	
			print "type mis-match"
			declaresynerror()
			return	#imp here
		if(lookup3[vald] < 10):
			reg[lookup3[vald]].update()
			updatedep(lookup3[vald])
		else:
			reg[lookup3[vald]].valoverride(reg[lookup3[vald]].val)
		#overflowcheck()
	if(lookup3[vald] < 10) :
		if((temp_p > 127 and temp_a > 127) or (temp_p <= 127 and temp_a > 127) or (temp_p > 127 and temp_a <= 127)):
			flags.b.overflow = 1
	else:		
		if ((temp_p > 32767 and temp_a > 32767) or (temp_p <= 32767 and temp_a > 32767) or(temp_p > 32767 and temp_a <= 32767)):
			flags.b.overflow = 1	
			
							
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
		if(lookup3[vald] < 10):	#both or none
			reg[lookup3[vald]].update()
			updatedep(lookup3[vald])
			reg[lookup3[vals]].update()
			updatedep(lookup3[vals])
		else:
			reg[lookup3[vald]].valoverride(reg[lookup3[vald]].val)
			reg[lookup3[vals]].valoverride(reg[lookup3[vals]].val)
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
	if(lookup3[vald] < 13):
		reg[lookup3[vald]].update()
		updatedep(lookup3[vald])
	else:
		reg[lookup3[vald]].valoverride(reg[lookup3[vald]].val)
	#add more or go sustainable
	
def fbor(dest, source):
	(vald, moded) = extract(dest)
	(vals, modes) = extract(source)
	if(moded == 1):
		declaresynerror()
		return
	#do other cases
	if(modes == 0 and moded == 0):
		if((lookup3[vals] < 13 and lookup3[vald] >= 13) or (lookup3[vald] < 13 and lookup3[vals] >= 13)):
			declaresynerror()
			print "Size mis-match"
			return
		temp_p = reg[lookup3[vald]].val
		temp_a = reg[lookup3[vals]].val
		reg[lookup3[vald]].val |= reg[lookup3[vals]].val
	elif(moded == 0) :
		temp_p = reg[lookup3[vald]].val
		temp_a = vals
		reg[lookup3[vald]].val |= vals		
	if(lookup3[vald] < 10):
		reg[lookup3[vald]].update()
		updatedep(lookup3[vald])
	else:
		reg[lookup3[vald]].valoverride(reg[lookup3[vald]].val)
	#For Overflow
	if(lookup3[vald] < 10):
		if((temp_p > 127 and temp_a <= 127) or (temp_p <= 127 and temp_a > 127)):
			flags.b.overflow = 1
	else:
		if((temp_p > 32767 and temp_a <= 32767) or (temp_p <= 32767 and temp_a > 32767)):
			flags.b.overflow = 1		
			
	return
		
def fand(dest, source):
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
		reg[lookup3[vald]].val &= reg[lookup3[vals]].val
	if(lookup3[vald] < 13):
		reg[lookup3[vald]].update()
		updatedep(lookup3[vald])
	else:
		reg[lookup3[vald]].valoverride(reg[lookup3[vald]].val)
				
		
def fdec(dest):
	(vald,moded) = extract(dest)
	if(moded == 1):
		declaresynerror()
		return
	reg[lookup3[vald]].val -= 1
	if(lookup3[vald] < 13):
		reg[lookup3[vald]].update
		updatedep(lookup3[vald])
	else:
		reg[lookup3[vald]].valoverride(reg[lookup3[vald]].val)
	#checkoverflow(lookup3[vald])
	if(lookup3[vald] > 16):
		updateacflag(reg[lookup3[vald]].val)
	
	if(reg[lookup3[vald]].val == 127 or reg[lookup3[vald]].val == 32767 or 
		reg[lookup3[vald]].val == 65536) :
		flags.b.overflow = 1	
	
		
def fdiv(source):
	a = 17							#cite! make ax from ah and al for every update of ah and al
	(vals, modes) = extract(source)
	if(modes == 1):
		declaresynerror()
		return
	temp = reg[a].val
	reg[2].val = temp / reg[lookup3[vals]].val
	reg[1].val = temp % reg[lookup3[vals]].val
	updatedep(1)
	return
	
def fsub(dest, source):
	(vald, moded) = extract(dest)
	(vals, modes) = extract(source)
	#destination is memory, do later
	if(modes == 0 and moded == 0):
		reg[lookup3[vald]].val -= reg[lookup3[vals]].val
	if(modes == 1 and moded == 0):
		reg[lookup3[vald]].val -= vals	#reg[lookup3[vald]] -

	if(modes == 1 and moded == 0):					
		temp = reg[lookup3[vald]].val + vals
	else:
		temp = reg[lookup3[vald]].val + reg[lookup3[vals]].val		#Akshay G
	temp_0 = reg[lookup3[vald]].val
	if(lookup3[vald] < 10):	
		if((temp > 127  and temp_0 <= 127) or (temp > 0 and temp <= 127 and temp_0 < 0)):
			flags.b.overflow = 1
	else:
		if((temp > 32767  and temp_0 <= 32767) or (temp >= 0 and temp <= 32767 and ((temp_0 < 0) or temp_0 > 32767))
			or (temp > 32767 and temp_0 < 0)) :
			flags.b.overflow = 1	
	if(lookup3[vald] < 13):
		reg[lookup3[vald]].update()
		updatedep(lookup3[vald])
	else:
		reg[lookup3[vald]].valoverride(reg[lookup3[vald]].val)	
	if(lookup3[vald] > 16):
		updateacflag(reg[lookup3[vald]].val)	 
		
def fadd(dest, source) :
	(vald, moded) = extract(dest)
	(vals, modes) = extract(source)
	#destination is memory, do later
	if(modes == 0 and moded == 0):
		reg[lookup3[vald]].val += reg[lookup3[vals]].val
	if(modes == 1 and moded == 0):
		reg[lookup3[vald]].val += vals

	temp_f = reg[lookup3[vald]].val		#Akshay G
	c = 0
	ac = 0
	if(modes == 1 and moded == 0):					
		temp = reg[lookup3[vald]].val - vals
	else:
		temp = reg[lookup3[vald]].val - reg[lookup3[vals]].val
	
	temp_f = reg[lookup3[vald]].val
	if(lookup3[vald] < 10) :
		if(((temp > 127) and (temp_f <= 127)) or ((temp <= 127) and (temp_f > 127))) :
			flags.b.overflow = 1
		if(temp_f > 255):
			flags.b.carry = 1
	else:
		if(((temp > 32767 and temp_f <= 32767)) or ((temp <= 32767) and (temp_f > 32767))) :
			flags.b.overflow = 1
		if(temp_f > 65536):
			flags.b.carry  = 1
			
	if(lookup3[vald] < 10):
		reg[lookup3[vald]].update()
		updatedep(lookup3[vald])
	else:
		reg[lookup3[vald]].valoverride(reg[lookup3[vald]].val)	
		 	
	if(lookup3[vald] > 16):
		updateacflag(reg[lookup3[vald]].val)
	
				
		
listoffunctions = [blank, fhlt, fmov, finc, fpop, fpush, fxor, fsub, fxchg, fmul, fnot, fbor, fand, fdec, fdiv, fadd]
		
