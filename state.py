import func
from func import *
import ctypes
import sys
from table import *
c_uint8 = ctypes.c_uint8

# Objects defining registers and segment registers

class Flags_bits(ctypes.LittleEndianStructure):
    _fields_ = [
    		("reserved_15", c_uint8, 1),
    		("I/O_Privilege", c_uint8, 1),
    		("Nested_f", c_uint8, 1),
		("overflow", c_uint8, 1),
		("direction", c_uint8, 1),
		("interrupt", c_uint8, 1),
		("trap", c_uint8, 1),
		("sign", c_uint8, 1),
		("zero", c_uint8, 1),
		("reserved_5", c_uint8, 1),
		("ac", c_uint8, 1),
		("reserved_3", c_uint8, 1),
		("parity", c_uint8, 1),
		("reserved_1", c_uint8, 1),
		("carry", c_uint8, 1),	
        ]
        
class Flags(ctypes.Union):
    _fields_ = [("b", Flags_bits),
                ("asbyte", c_uint8)]

class var_8(object):
	def __init__(self):
		self.val = 00
	def update(self):
		if(self.val > 255):
			while(self.val > 255):
				self.val -= 256
			flags.b.carry = 1
			flags.b.sign = 0
			flags.b.zero = 0
		elif(self.val < 0):
			flags.b.sign = 1
			flags.b.carry = 1 #Update #1
			flags.b.zero = 0
			self.val += 256
		elif(self.val == 0):
			flags.b.zero = 1
			flags.b.sign = 0
			flags.b.carry = 0	#sign, zero, carry, parity | overflow
		c = 0
		temp = self.val
		while (temp > 0):
			if(temp & 1 == 1):
				c = c + 1
			temp = temp >> 1
		if(c % 2 == 0 and c != 0):
			flags.b.parity = 1
		else:
			flags.b.parity = 0
class var_16(object):
	def __init__(self):
		self.val = 0000
	def update(self):
		if(self.val > 0):
			while(self.val > 65535):
				self.val -= 65536
			flags.b.carry = 1
			flags.b.sign = 0
			flags.b.zero = 0
		elif(self.val < 0):
			self.val += 65536		#store in 2'sc?
			flags.b.carry = 1 #Update #1
			flags.b.sign = 1
			flags.b.zero = 0
		elif(self.val == 0):
			flags.b.carry = 0
			flags.b.sign = 0
			flags.b.zero = 1
		c = 0
		temp = self.val
		while (temp > 0):
			if(temp & 1 == 1):
				c = c + 1
			temp = temp >> 1
		if(c % 2 == 0 and c != 0):
			flags.b.parity = 1
		else:
			flags.b.parity = 0		

class special_var(object):
	def __init__(self, order):
		self.val = 0000
		self.order = order
	def update(self):		
		self.val = int(hex(reg[self.order].val)[2:] + hex(reg[self.order + 1].val)[2:], 16)
	def valoverride(self, value):
		self.val = value
		if(self.val > 0):
			while(self.val > 65535):
				self.val -= 65536
			flags.b.carry = 1
			flags.b.sign = 0
			flags.b.zero = 0
		elif(self.val < 0):
			self.val += 65536
			flags.b.carry = 1 #Update #1
			flags.b.sign = 1
			flags.b.zero = 0
		elif(self.val == 0):
			flags.b.carry = 0
			flags.b.sign = 0
			flags.b.zero = 1
		c = 0
		temp = self.val
		while (temp > 0):
			if(temp & 1 == 1):
				c = c + 1
			temp = temp >> 1
		if(c % 2 == 0 and c != 0):
			flags.b.parity = 1
		else:
			flags.b.parity = 0
		if(self.val > 255):
			reg[self.order].val = int(hex(self.val)[2:-2], 16)
			reg[self.order + 1].val = int(hex(self.val)[-2:], 16)
		else:
			reg[self.order].val = 0
			reg[self.order + 1].val = self.val


#CREATING Instances for each variable
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

flags = Flags()
flags.asbyte = 0x0
#flags.b.I/O_Privilege = 0x1
flags.b.Nested_f = 1
flags.b.reserved_15 = 1

reg = [virgin, ah, al, bh, bl, ch, cl, dh, dl, di, si, bp, sp, ds, es, ss, cs, ax, bx, cx, dx]

