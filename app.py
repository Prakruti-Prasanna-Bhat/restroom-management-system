import csv
import mysql.connector as mys
import numpy 
import matplotlib.pyplot
count_=0

Tup=(28,29,30,31)
totday=0
soap=15
nextsoap=0
tissue=5
nexttissue=0
month=""
day31=['January','March','May','July','August','October','December']
day30=['April','June','September','November']
Feb=['February']
year=int(input("Enter year: "))
while True:
    month=input("Enter month(January,February,March,April,May,June,July,August,September,October,November,December): ")
    month=month.capitalize()
    if month in Feb:
        if(year%4==0):
            totday=Tup[1]            
        else:
            totday=Tup[0]
        break
    elif month in day31:
        totday=Tup[3]
        break
    elif month in day30:
        totday=Tup[2]
        break
    else:
        print("ERROR: wrong month-please check input")
        continue
while True:
    workday=int(input("Enter no. of working days: "))
    if workday>totday:
        print("ERROR: no. of working days more than total number of days in month-please check input")
        continue
    else:
        break
while True:
    workdaydone=int(input("Enter no of working days past: "))
    if (workdaydone>totday) or (workdaydone>workday):
        print("ERROR:no. of working days past more than no. of working days in month-please check input")
        continue
    else:
        break
nextsoap=(soap-(workdaydone%soap))
nexttissue=(tissue-(workdaydone%tissue))

def create():
    con=mys.connect(host="localhost",user='root',passwd='amaatra')
    cur=con.cursor()
    cur.execute("CREATE DATABASE Facility_fixing")
    cur.execute("USE Facility_fixing")
    cur.execute("CREATE table CONTACTS(Issue int ,Name varchar(100),Dept varchar(100),Contact varchar(15))")
    cur.execute("CREATE table ISSUES(StallNo int,DateOfComplaint date,Issue int)")
    
def display():
    print("*****")
    print("Year:",year)
    print("Month:",month)
    print("Total number of days in month:",totday)
    print("Number of working days in month:",workday)
    print("Number of working days past in month:",workdaydone)
    print("Order soap in ",nextsoap,"days")
    print("Order tissue in ",nexttissue,"days")
    print(count_," stalls are no longer in use")
    feedback()
    graph1_()
    graph2_()
 
def displaytable():
    cur.execute("Show tables")
    data1=cur.fetchall()
    for i in data1:
        print(i)
    tablename=input("Enter table name to be viewed: ")
    q="SELECT * FROM {}".format(tablename)
    cur.execute(q)
    data=cur.fetchall()
    if data==None:
        print("Record Not Found!")
    else:
       for i in data:
           print(i)

def addrowi():
    while True:
        stno=int(input("Enter Stall No: "))
        doc=input("Enter Date of Complaint: ")
        issue=int(input("1.Broken Toilets \n2.Broken Door Accessories \n3.Leaky Faucets \n4.Dirty Restroom \n5.No Waste Bin Present \n6.Other \nEnter Issue: "))
        q="INSERT INTO ISSUES VALUES({},'{}',{});".format(stno,doc,issue)
        cur.execute(q)
        con.commit()
        ch=input("Do you want continue? (y/n): ")
        if ch in"yY":
            continue
        elif ch in"nN":
            break
        else:
            print("Wrong Input")
            continue

def addrowc():
    d={"Aashir":[1,"Management",8861666629],"Prasanth":[1,"Management",9563748362],"Devyani":[2,"Management",674356656],"Manjunath":[2,"Management",4756475835],"Ankit":[3,"Plumbing",9658786484],"Arun":[3,"Plumbing",9365646584],"Aditya":[4,"Cleaning",9635634757],"Praneel":[4,"Cleaning",7845744876],"Hari":[5,"Cleaning",7867846834],"Rishi":[5,"Cleaning",8476539246],"Vishal":[6,"All",7658465784]}
    for n in d:
        name=n
        issue=d[n][0]
        dept=d[n][1]
        cont=d[n][2]
        q="INSERT INTO CONTACTS VALUES({},'{}','{}','{}');".format(issue,name,dept,cont)
        cur.execute(q)
        con.commit()

def count():
    cur.execute("SELECT COUNT(ISSUE),STALLNO FROM ISSUES GROUP BY STALLNO;")
    data2=cur.fetchall()
    for i in data2:
        print(i)
    global count_
    cur.execute("SELECT COUNT(ISSUE),STALLNO FROM ISSUES GROUP BY STALLNO having COUNT(issue)>5;")
    data3=cur.fetchall()
    if data3!=None:
        for i in data3:
            print(i[1],"is no longer in use")
            count_+=1
            
def feedback():
    file=open("Feedback.txt","a+")
    fb=input("Please provide feedback if any:")
    file.write(fb)
    file.close()

def join():
    stn=int(input("Enter stall no: "))
    q="Select STALLNO,ISSUES.ISSUE,DATEOFCOMPLAINT,NAME,DEPT,CONTACT from ISSUES,CONTACTS WHERE ISSUES.ISSUE=CONTACTS.ISSUE and stallno={}".format(stn)
    cur.execute(q)
    data=cur.fetchall()
    if data!=None:
        for i in data:
            print (i)
    else:
        print("Invalid Stall No")

    f=open("Contacts.csv","w",newline="")
    join_writer=csv.writer(f)
    join_writer.writerow(["Stall No","Issue","Date of Complaint","Name","Department","Contact"])
    join_writer.writerows(data)
    
def graph1_():
    cur.execute("SELECT COUNT(ISSUE),STALLNO FROM ISSUES GROUP BY STALLNO;")
    result=cur.fetchall()
    stall=[]
    num=[]
    for i in result:
        stall.append(i[1])
        num.append(i[0])
    matplotlib.pyplot.bar(stall,num)
    matplotlib.pyplot.ylim(0,10)
    matplotlib.pyplot.xlabel("Stall Numbers")
    matplotlib.pyplot.ylabel("Number of issues faced")
    matplotlib.pyplot.title("Issues")
    matplotlib.pyplot.show()

def graph2_():
    cur.execute("SELECT COUNT(STALLNO) FROM ISSUES GROUP BY STALLNO having COUNT(issue)>5;")
    nw=list(cur.fetchall())
    cur.execute("SELECT COUNT(STALLNO) FROM ISSUES GROUP BY STALLNO having COUNT(issue)<=5;")
    w=list(cur.fetchall())
    
    work =['Stalls Working','Stalls Not Working']
    data =[len(w),len(nw)]
    matplotlib.pyplot.pie(data,labels=work)
    matplotlib.pyplot.show()


run=input("Is this the first time you are running this program? (y/n):")
if run in "Yy":
    create()
    con=mys.connect(host="localhost",user='root',passwd='amaatra',database='Facility_fixing')
    cur=con.cursor()
    addrowc()
else:
    con=mys.connect(host="localhost",user='root',passwd='amaatra',database='Facility_fixing')
    cur=con.cursor()

while True:
    choices=int(input("1.Display tables \n 2.add a record in a table Issues \n 3.Find stalls no longer in use \n 4.Display contacts to fix stalls \n 5.End \nEnter Action to be done:  "))
    if choices==1:
        displaytable()
        
    elif choices==2:
        addrowi()
        
    elif choices==3:
        count()

    elif choices==4:
        join()

    elif choices==5:
        break

    else:
        print("Wrong Input")
        continue

display()













