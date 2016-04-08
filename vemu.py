import sys
import ctypes
c_uint8 = ctypes.c_uint8
class Flags_bits(ctypes.LittleEndianStructure):
    _fields_ = [
		("overflow", c_uint8, 1),
		("direction", c_uint8, 1),
		("interrupt", c_uint8, 1),
		("trap", c_uint8, 1),
		("sign", c_uint8, 1),
		("zero", c_uint8, 1),
		("ac", c_uint8, 1),
		("parity", c_uint8, 1),
		("carry", c_uint8, 1),
	
        ]
class Flags(ctypes.Union):
    _fields_ = [("b", Flags_bits),
                ("asbyte", c_uint8)]
flags = Flags()
flags.asbyte = 0x0
#flags.b.overflow = 0
#flags.b.trap = 1
class var_8(object):
	def __init__(self):
		self.val = 0
	def update(self):
		while(self.val > 255):
			self.val -= 256
class var_16(object):
	def __init__(self):
		self.val = 0
	def update(self):
		while(self.val > 65535):
			self.val -= 65536
class special_var(object):
	def __init__(self, order):
		self.val = 0
		self.order = order
	def update(self):
		self.val = int(hex(reg[self.order].val)[-2:] + hex(reg[self.order + 1].val)[-2:], 16)
	def valoverride(self, value):
		self.val = value
		while(self.val > 65535):
			self.val -= 65536
		reg[self.order].val = int(hex(self.val)[2:-2], 16)
		reg[self.order + 1].val = int(hex(self.val)[-2:], 16)				
ah = var_8()
al = var_8()
bh = var_8()
bl = var_8()
ch = var_8()
cl = var_8()
dh = var_8()
dl = var_8()
di = var_16()
si = var_16()
bp = var_16()
sp = var_16()
ds = var_16()
es = var_16()
ss = var_16()
cs = var_16()
virgin =  var_8()
ax = special_var(1)
bx = special_var(3)
cx = special_var(5)
dx = special_var(7)
lookup3 = {18:1, 112:2, 212:3, 28:4, 38:5, 312:6, 48:7, 412:8, 49:9, 199:10, 216:11, 1916:12, 419:13, 519:14, 1919:15, 319:16, 124:17, 224:18, 324:19, 424:20}
reg = [virgin, ah, al, bh, bl, ch, cl, dh, dl, di, si, bp, sp, ds, es, ss, cs, ax, bx, cx, dx]
#pointers?
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
			reg[a].val = reg[b].val*reg[lookup3[vals]].val
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
def num_there(s):
	return any(i.isdigit() for i in s)
def setmodel(a):
	model = a
def setstacksize(size):
	stack_size = size
def setcodebegin():
	code = True				#manage stack[] with this, also check full and empty 
a = raw_input("Enter file name: ")
filein = open(a)
c = a[:-4] + "sidekick.txt"
fileout = open(c, "w")
lines2 = filein.readlines()
for line in lines2:
	if(line[0] == '.'):
		if(line[1:6] == 'model'):
			setmodel(line[7:])
		elif(line[1:6] == 'stack'):
			setstacksize(int(line[7:]))
		elif(line[1:] == 'data'):
			pass		
		elif(line[1:] == 'code'):	#skipping elements in loop, append to dictionary, dont write till '.code'
 			setcodebegin()		#how to differentiate in modes if appended mem to dictionary? make new dict for bss 							#and use try everywhere ref takes place, using mode in except!
	else:
		columns = line.split(" ")
		for item in columns:
			if(item == columns[len(columns) - 1]):
				temp = '$\n'
			else:
				temp = '$,'
			if(num_there(item)):
				if(item[-2] == 'h'):
					line = line.replace(item, str(int(item[:-2], 16)) + temp) #hex to int!
				else:
					line = line.replace(item, item[:-1] + temp)	
		fileout.write(line)
filein.close()
fileout.close()
b = c[:-4] + "_temp_working_file.txt"
f = open(b, "w")
cha = 1
lookup = {'a':1, 'b':2, 'c':3, 'd':4, 'e':5, 'f':6, 'g':7, 'h':8, 'i':9, 'j':10, 'k':11,'l':12,'m':13,'n':14,'o':15,'p':16,'q':17,'r':18,'s':19,'t':20,'u':21, 'v':22, 'w':23,'x':24,'y':25,'z':26}
with open(c) as filein:
	while(cha):
		cha = filein.read(1)
		try:
			d = lookup[cha.lower()]
			f.write(str(d))
		except:
			d = cha
			if(d != ','):
				f.write(d)
			else:
				f.write('')
f.close()
lookup2 = { 	81220 : 1,
		131522 :2,
		9143 :3,
		161516 :4,
		1621198 :5,
		241518 :6,
		19212 :7,
		24387:8,
		132112: 9,
		141520: 10,
		1518: 11,
		1144: 12,
		453: 13,
		4922: 14
	}
			
listoffunctions = [blank, fhlt, fmov, finc, fpop, fpush, fxor, fsub, fxchg, fmul, fnot, fbor, fand, fdec, fdiv]
stack = []


filein = open(b)
lines = filein.readlines()
for line in lines:
	columns = line.split(" ")
	if(line == '\n'):
		pass
	else:
		lkey = lookup2[int(columns[0])]
		try:
			listoffunctions[lkey](columns[1], columns[2])
		except:
			try:
				listoffunctions[lkey](columns[1])
			except:
				listoffunctions[lkey]()
	printstate()
		

