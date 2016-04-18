import sqlite3
import sys
from func import *
from state import *

def start_tab():
    conn = sqlite3.connect('reg4.db')
    conn.execute('''CREATE Table reg \
                (reg_id TEXT NOT NULL,
                value   INT  NOT NULL);''')
    cursor = conn.execute("SELECT reg_id, value from reg");
    conn.close()

def insert_rec():
    conn = sqlite3.connect('reg3.db')
    conn.execute("INSERT into reg (reg_id, value)\
                VALUES ('ah', 0)");
    conn.execute("INSERT into reg (reg_id, value)\
                VALUES ('al', 0)");
    conn.execute("INSERT into reg (reg_id, value)\
                VALUES ('bh', 0)");
    conn.execute("INSERT into reg (reg_id, value)\
                VALUES ('bl', 0)");
    conn.execute("INSERT into reg (reg_id, value)\
                VALUES ('ch', 0)");
    conn.execute("INSERT into reg (reg_id, value)\
                VALUES ('cl', 0)");
    conn.execute("INSERT into reg (reg_id, value)\
                VALUES ('dh', 0)");
    conn.execute("INSERT into reg (reg_id, value)\
                VALUES ('dl', 0)");
    conn.commit
    conn.close()

def update_rec():
    conn = sqlite3.connect('reg3.db')
    cursor = conn.execute("SELECT reg_id, value from reg")
    #print "yes", reg[1].val
    cursor.execute('''update reg set value = ? where reg_id = 'ah' ''', (reg[1].val,))

    cursor.execute('''UPDATE reg set value = ? where reg_id = 'ah' ''', (reg[1].val,))
    #print "yes", reg[2].val
    cursor.execute('''UPDATE reg set value = ? where reg_id = 'al' ''', (reg[2].val,))
    #print "yes", reg[3].val
    cursor.execute('''UPDATE reg set value = ? where reg_id = 'bh' ''', (reg[3].val,))
    cursor.execute('''UPDATE reg set value = ? where reg_id = 'bl' ''', (reg[4].val,))
    cursor.execute('''UPDATE reg set value = ? where reg_id = 'ch' ''', (reg[5].val,))
    cursor.execute('''UPDATE reg set value = ? where reg_id = 'cl' ''', (reg[6].val,))
    cursor.execute('''UPDATE reg set value = ? where reg_id = 'dh' ''', (reg[7].val,))
    cursor.execute('''UPDATE reg set value = ? where reg_id = 'dl' ''',(reg[8].val,))
    conn.commit
    #row = 0
        #conn.close()
        #conn = sqlite3.connect('reg3.db')
    cursor = conn.execute("SELECT reg_id, value from reg")          
    conn.execute("SELECT reg_id, value from reg")
    conn.close()#for row in cursor:
    #    print "REG : ", row[0]
     #   print "VALUE : ", row[1], "\n"

def delete_tab():
    conn = sqlite3.connect('reg.db')
    cursor = conn.cursor()
    cursor.execute('''DROP TABLE reg''')
    conn.commit
    conn.close()

#delete_tab()
