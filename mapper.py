a = raw_input("Enter file name: ")
b = a[:-4] + "_temp_working_file.txt"
f = open(b, "w")
c = 1
lookup = {'a':1, 'b':2, 'c':3, 'd':4, 'e':5, 'f':6, 'g':7, 'h':8, 'i':9, 'j':10, 'k':11,'l':12,'m':13,'n':14,'o':15,'p':16,'q':17,'r':18,'s':19,'t':20,'u':21, 'v':22, 'w':23,'x':24,'y':25,'z':26}
with open(a) as filein:
	while(c):
		c = filein.read(1)
		try:
			d = lookup[c.lower()]
			f.write(str(d))
		except:
			d = c
			if(d != ','):
				f.write(d)
			else:
				f.write('')
f.close()

