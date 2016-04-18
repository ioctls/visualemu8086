import PyQt4
from PyQt4.QtGui import * 
from PyQt4.QtCore import * 
import sys
from func import *
from state import *
import dbmg
from table import *
app 	= QApplication(sys.argv)
table 	= QTableWidget()
table1 = QTableWidget()
table3 = QTableWidget()
table4 = QTableWidget()
tablei = QTableWidget()
tableItem 	= QTableWidgetItem()
row = 0
ex  = 1
ey = 1
fi = ''
trow = 0
def endt():
    return app.exec_()

def start(s):
    file = open(str(s))
    global fi
    fi = s
    #n_line = 0
    lin = file.readlines()
    global row
    for line in lin:
        row += 1
        #return n_line
    file.close()
    
class tables1:
    global ex
    global ey
    def printt(self):  
        
        z = 10
        # initiate table
        table.setWindowTitle("P.A.S.S Assembler-cum-Debugger ")
        #table.resize(1380, 80)
        #row = start()
        table.resize(500, 130)#35*row)
        table.setRowCount(3)
        table.setColumnCount(1)

        def cellClick(row,col):
            global ex
            ex += 1
            #print "ex", ex#print "Click on " + str(row) + " " + str(col) +  ": "
            string = table.item(row, col)
            print string.text()
            r = table.row(string)
            if r == 0:
                t1 = tables2()
                t1.printt()
            elif r == 1:
                t3 = tables3()
            elif r == 2:
                t4 = tables4()
            endt()
                
                
            #print table.label()
            #print table.visualRow(table.currentRow())

        # set label
        #table.setVerticalHeaderLabels(QString("Values:;").split(";"))
        table.setColumnWidth(0, 120)
        table.horizontalHeader().setStretchLastSection(True)

        table.setVerticalHeaderLabels(QString(";;;;;;;;;;;;;;;;;;;;;;;;;;").split(";"))
        table.setHorizontalHeaderLabels(QString("STATUS;").split(";"))
     
        am = reg[0].val
        
        # set data
        table.setItem(0,0, QTableWidgetItem("\t\t             Registers"))
        am = reg[1].val
        table.setItem(0,1, QTableWidgetItem("\t\t                 Flag"))
        table.setItem(0,2, QTableWidgetItem("\t\t                 Stack"))

        
        brush = QBrush(QColor(238, 233, 233))
        brush.setStyle(Qt.SolidPattern)

        i = table.item(0, 0)
        i.setBackground(brush)

        brush = QBrush(QColor(255, 250, 250))
        
        i = table.item(0, 1)
        i.setBackground(brush)
        
        brush = QBrush(QColor(238, 233, 233))

        i = table.item(0, 2)
        i.setBackground(brush)

        table.show()

# on click function
        table.cellClicked.connect(cellClick)
        #print "rere"
        global ex
        endt()
        #print "ex", ex
        #ez = ex + ey
        
        
        

            
class tables2:
    def printt(self):  
        
        
        # initiate table
        table1.setWindowTitle("Register Status ")
        table1.resize(1000, 160)
        #table1.resize(150, 500)
        table1.setRowCount(4)
        table1.setColumnCount(10)

        # set label
        table1.horizontalHeader().setStretchLastSection(True)

        table1.setVerticalHeaderLabels(QString(";;;;;").split(";"))
        table1.setHorizontalHeaderLabels(QString("ah;al;bh;bl;ch;cl;dh;dl;di;si;es;ss;ds;cs").split(";"))
     
        #am = reg[0].val

        c = 1
        while c < 11:
            # set data
            am = reg[c].val
            table1.setItem(0,-1+c, QTableWidgetItem(str(am)))
            table1.setItem(2,-1+c, QTableWidgetItem("          "+str(reg[8+c].name)))
            c += 1
        c = 11
        while c < 21:
            # set data
            am = reg[c].val
            table1.setItem(3,-11 + c, QTableWidgetItem(str(am)))
            c += 1

        table.horizontalHeader().setStretchLastSection(True)

        i = table1.item(0, 0)
        
        brush = QBrush(QColor(224, 255, 255))
        brush.setStyle(Qt.SolidPattern)
        i.setBackground(brush)
        i.setTextColor(QColor(0, 0, 0))
        i = table1.item(0, 0)
        i.setBackground(brush)
        brush1 = QBrush(QColor(242, 255, 255))
        brush1.setStyle(Qt.SolidPattern)
        
        
        i = table1.item(0, 1)
        i.setBackground(brush1)
        i = table1.item(0, 2)
        i.setBackground(brush)
        i = table1.item(0, 3)
        i.setBackground(brush1)
        i = table1.item(0, 4)
        i.setBackground(brush)
        i = table1.item(0, 5)
        i.setBackground(brush1)
        i = table1.item(0, 6)
        i.setBackground(brush)
        i = table1.item(0, 7)
        i.setBackground(brush1)
        i = table1.item(0, 8)
        i.setBackground(brush)
        i = table1.item(0, 9)
        i.setBackground(brush1)
        
        i = table1.item(3, 0)
        i.setBackground(brush)
        i = table1.item(3, 1)
        i.setBackground(brush1)
        i = table1.item(3, 2)
        i.setBackground(brush)
        i = table1.item(3, 3)
        i.setBackground(brush1)
        i = table1.item(3, 4)
        i.setBackground(brush)
        i = table1.item(3, 5)
        i.setBackground(brush1)
        i = table1.item(3, 6)
        i.setBackground(brush)
        i = table1.item(3, 7)
        i.setBackground(brush1)
        i = table1.item(3, 8)
        i.setBackground(brush)
        i = table1.item(3, 9)
        i.setBackground(brush1)
        
        
        table1.show()
        endt()

class tables3:
    def __init__(self):  
        
        
        # initiate table
        table3.setWindowTitle("Flag Register")
        table3.resize(920, 80)
        #table1.resize(150, 500)
        table3.setRowCount(1)
        table3.setColumnCount(9)
       
        table3.setVerticalHeaderLabels(QString(";;;").split(";"))
        table3.setHorizontalHeaderLabels(QString("O;D;I;T;S;Z;AC;P;C;;;;;").split(";"))
     
        am = reg[0].val

        
        # set data
        table3.setItem(0,0, QTableWidgetItem("            "+str(flags.b.overflow)))
        am = reg[1].val
        table3.setItem(0,1, QTableWidgetItem("            "+str(flags.b.direction)))
        am = reg[2].val
        table3.setItem(0,2, QTableWidgetItem("            "+str(flags.b.interrupt)))
        am = reg[3].val
        table3.setItem(0,3, QTableWidgetItem("            "+str(flags.b.trap)))
        am = reg[4].val
        table3.setItem(0,4, QTableWidgetItem("            "+str(flags.b.sign)))
        am = reg[5].val
        table3.setItem(0,5, QTableWidgetItem("            "+str(flags.b.zero)))
        am = reg[6].val
        table3.setItem(0,6, QTableWidgetItem("            "+str(flags.b.ac)))
        am = reg[7].val
        table3.setItem(0,7, QTableWidgetItem("            "+str(flags.b.parity)))
        am = reg[8].val
        table3.setItem(0,8, QTableWidgetItem("            "+str(flags.b.carry)))
        am = reg[9].val
        
        table3.show()

        i = table3.item(0, 0)
        
        brush = QBrush(QColor(224, 255, 255))
        brush1 = QBrush(QColor(240, 255, 255))
        brush.setStyle(Qt.SolidPattern)
        i.setBackground(brush)
        i.setTextColor(QColor(0, 0, 0))
        i = table3.item(0, 0)
        i.setBackground(brush)
        i = table3.item(0, 1)
        i.setBackground(brush1)
        i = table3.item(0, 2)
        i.setBackground(brush)
        i = table3.item(0, 3)
        i.setBackground(brush1)
        i = table3.item(0, 4)
        i.setBackground(brush)
        i = table3.item(0, 5)
        i.setBackground(brush1)
        i = table3.item(0, 6)
        i.setBackground(brush)
        i = table3.item(0, 7)
        i.setBackground(brush1)
        i = table3.item(0, 8)
        i.setBackground(brush)
        table3.show()

        endt()
        
class tables4:
    def __init__(self):  
        
        ct = 0
        for item in stack:
            ct += 1

        
        # initiate table
        table4.setWindowTitle("Stack Status")
        table4.resize(300, 80)
        #table1.resize(150, 500)
        table4.setRowCount(ct)
        table4.setColumnCount(1)

        # set label
        table4.horizontalHeader().setStretchLastSection(True)

        table4.setVerticalHeaderLabels(QString(";;;;;;;;;").split(";"))
        table4.setHorizontalHeaderLabels(QString("Stack;;;").split(";"))
     
        ct1 = ct
        ct = 0
        while ct < ct1:
            table4.setItem(ct,0, QTableWidgetItem(str(stack[ct])))
            ct += 1
        table4.show()

        brush = QBrush(QColor(224, 255, 255))
        brush.setStyle(Qt.SolidPattern)

        ct = 0
        
        endt()
        
class tablesi:
    global ey
    
    def printt(self, kl):  
            
        z = 10

        # initiate table
        tablei.setWindowTitle("P.A.S.S Assembler-cum-Debugger ")
            #table.resize(1380, 80)
            #row = start()
        global row
        
        tablei.resize(500, 34*(row-kl))
        tablei.setRowCount(row - kl)
        tablei.setColumnCount(1)
        global trow
        trow = row - kl
        
        def cellClick(row,col):
            global ex
            ex += 1
            print "ey", ey
            string = tablei.item(row, col)
            #print string.text()
            r = tablei.row(string)
            func.seek_line(r)
            dbmg.update_rec()
            tt = tables1()
            tt.printt()
            endt()
                    
        
            #print table.label()
                #print table.visualRow(table.currentRow())

            # set label
            #table.setVerticalHeaderLabels(QString("Values:;").split(";"))
        
        tablei.horizontalHeader().setStretchLastSection(True)

        tablei.setVerticalHeaderLabels(QString(";;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;").split(";"))
        tablei.setHorizontalHeaderLabels(QString("Instructions;").split(";"))
        global fi
        file = open(str(fi))
        lines = file.readlines()
        counter = 0
        rc = 0
        for line in lines:
            instruc = line
            if counter < kl:
                pass
            else:
                tablei.setItem(rc, 0, QTableWidgetItem("\t\t          "+str(instruc)))
                rc += 1
            counter += 1
        brush = QBrush(QColor(238, 233, 233))
        brush.setStyle(Qt.SolidPattern)
        brush1 = QBrush(QColor(255, 250, 250))

        qw = 0
        while qw < trow:
            if qw % 2 == 0:
                i = tablei.item(qw, 0)
                i.setBackground(brush)
            else:     
                i = tablei.item(qw, 0)
                i.setBackground(brush1)
            qw += 1
            
        tablei.show()
      # on click function
        tablei.cellClicked.connect(cellClick)
            #print "rere"'
        global ex
        ex -= 1
        while ex > 0:
            ex -= 1
            endt()
       
        
        
