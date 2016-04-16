#update 7/4/16
#work in progress, works somehow
#implemented flag register
#limiting values of registers
#implemented ax as a function of ah and al, also vice versa
#added functionality to scan lines .model, .stack, .code and so on
#reg is now a list of object instances
#reg and alsoreg are combined now
import sys
import ctypes
import func
import state
from state import * 
from table import *

lookup = {'a':1, 'b':2, 'c':3, 'd':4, 'e':5, 'f':6, 'g':7, 'h':8, 'i':9, 'j':10, 'k':11,'l':12,'m':13,'n':14,'o':15,'p':16,'q':17,'r':18,'s':19,'t':20,'u':21, 'v':22, 'w':23,'x':24,'y':25,'z':26}

#Variables defining initialization 

code = False


# Func returns true if given string has at least one digit
def num_there(s):
	return any(i.isdigit() for i in s)
def set_model(a):
	ipass.model = a
def set_stack_size(size):
	ipass.stack = size 

#Function to split the line into segments sep with a spcae
def l_split(a, line):
	str_c = ""
	b = 0
	for i in line :
		if(i.isalnum()):
			str_c = str_c + i
			b = 1
		elif(b == 1):
			a.append(str_c)
			str_c = ""
			b = 0	

#Here lies the snippet to convert given file to appropriate format to read for the gui
def startup():
	if(ipass.model != ""):
		print "Model ",
		print ipass.model[:-1]
		#linestat = linestat + 1
	else:
		print "No model defined, but we got Akshay G, so we will run your program anyway."
	if(ipass.stack > 0):
		print "Size of stack is ",	#use len in push and pop
		print ipass.stack
		#linestat += 1
	else:
		print "Warning, no stack delacred. But we are awesome, so we will run your program anyway."	#disable push pop
	if(ipass.code):
		print ".code initialized"
		#linestat = linestat + 1						#do something for .data
	else:
		print "No '.code' section found, but we are awesome, so we will run your program anyway."
	print "We'll start with all flags with access set to 0."

a = raw_input("Enter file name: ")
filein = open(a)

# Make another file to write in modified version
c = a[:-4] + "sidekick.txt"
fileout = open(c, "w")

#Get the input of lines from the file given by user
lines2 = filein.readlines()
#Done Optimization for now.. Only HEx Conversion not working
for line in lines2:
	if(line[0] == '.'):
		if(line[1:6] == 'model'):
			ipass.model = line[7:]
			continue
		elif(line[1:6] == 'stack'):
			ipass.stack = int(line[7:])
			continue
		elif(line[1:] == 'data'):
			continue		
		elif(line[1:] == 'code\n'):	#skipping elements in loop, append to dictionary, dont write till '.code'
 			code = True
			ipass.code = True
 			continue	#how to differentiate in modes if appended mem to dictionary? make new dict for bss       
	if(code == True):
		columns = []  
		l_split(columns, line)
	    	for item in columns:
		    if(num_there(item)):
                # Add '$'in the end to indicate a no (hex or decimal)
			if(item[-1] == 'h'):
				item = item.replace(item, str(int(item[:-1], 16))+ '$') 
			else:
				item = item.replace(item, item + '$')								 
	    	    fileout.write(item)
	    	    fileout.write(" ") #Does this add a space after every write??
	    	if(len(columns) != 0):    	
	    		fileout.write("\n")    
filein.close()
fileout.close()

startup()

b = c[:-4] + "_temp_working_file.txt"
f = open(b, "w")
cha = 1

#Replaces all ',' with ' '
with open(c) as filein:
	while(cha):
		cha = filein.read(1)
		try:
			d = lookup[cha.lower()]
			f.write(str(d))
		except:
			d = cha
			f.write(d)
f.close()

filein = open(b)
lines = filein.readlines()
for line in lines:
	if(line == '\n'):
		pass
	else:
		columns = line.split(" ")
		lkey = lookup2[int(columns[0])]
		try:
			func.listoffunctions[lkey](columns[1], columns[2])
		except:
			try:
				func.listoffunctions[lkey](columns[1])
			except:
				func.listoffunctions[lkey]()	
	func.printstate()
