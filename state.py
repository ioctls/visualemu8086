import func
from func import *
import ctypes
import sys
from table import *
c_uint8 = ctypes.c_uint8



# Objects defining registers and segment registers




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

reg = [virgin, ah, al, bh, bl, ch, cl, dh, dl, di, si, bp, sp, ds, es, ss, cs, ax, bx, cx, dx]


def action(lines) :
	for line in lines:
		#print columns
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
		
