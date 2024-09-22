from datetime import date, timedelta
from os import name, system
import platform
import mysql.connector
#***********************************************************************************************************************#
def cls():
   system('cls')
def initdb():
   db = mysql.connector.connect(user='root', password='', host='localhost', database='hospital')
   cr = db.cursor()
   sql="INSERT INTO serial VALUES(1,1)"
   try:
      cr.execute(sql)
      db.commit()
      print("DataBase Initialized Successfully")
   except:
      db.rollback()
def checkdb():
   db = mysql.connector.connect(user='root', password='', host='localhost',)
   cr = db.cursor()
   cr.execute("create database if not exists hospital")
def checktbl():
   db = mysql.connector.connect(user='root', password='', host='localhost', database='hospital')
   cr = db.cursor()
   cr.execute("create table if not exists serial(pid int, did int)")
   cr.execute("create table if not exists patient(pid int primary key, pname varchar(30), gend char, dob date, phn varchar(10), addr varchar(50))")
   cr.execute("create table if not exists doctor(did int primary key, dname varchar(30), qual varchar(30), dept varchar(20), phn varchar(10))")
   cr.execute("create table if not exists treatment(pid int, did int, adate date, status varchar(10), fees int);")
   cr.execute("select count(*) from serial")
   dset=cr.fetchone()
   if(dset[0]==0):
      initdb()
   else:
      maintain()
      print("DataBase Verified Successfully")
def maintain():
   db = mysql.connector.connect(user='root', password='', host='localhost', database='hospital')
   cr1,cr2 = db.cursor(),db.cursor()
   try:
      cr1.execute("update treatment set status='FAIL' where timestampdiff(day,adate,now())>0")
      cr2.execute("delete from treatment where status in ('FAIL','CANCEL') and timestampdiff(day,adate,now())>365")
      db.commit()
   except:
      db.rollback()
#***********************************************************************************************************************#

def selection():
   db = mysql.connector.connect(user='root', password='', host='localhost', database='hospital')
   cursor = db.cursor()
   cls()
   print("----------------------------------------------")
   print("     WELCOME TO HOSPITAL MANAGEMENT SYSTEM    ")
   print("----------------------------------------------")
   print("           1. PATIENT MANAGEMENT              ")
   print("           2. DOCTOR MANAGEMENT               ")
   print("           3. TREATMENT MANAGEMENT            ")
   print("           4. QUIT PROJECT                    ")
   ch=input("          Enter ur choice (1-4) : ")
   if ch=='1':
      func_patient()
   elif ch=='2':
      func_doctor()
   elif ch=='3':
      func_treatment()
   elif ch=='4':
      exit()
   else:
      selection()

#***********************************************************************************************************#

def func_patient():
   cls()
   print('     WELCOME TO PATIENT MANAGEMENT SYSTEM      ')
   print('                                               ')
   print('          1. NEW PATIENT ENTRY                 ')
   print('          2. SEARCH PATIENT DETAILS            ')
   print('          3. VIEW ALL RECORDS                  ')
   print('          4. UPDATE RECORDS                    ')
   print('          5. DELETE RECORDS                    ')
   print('          6. Go BACK to MAIN MENU              ')
   c=int(input("       Enter ur choice (1-6) : "))
   if c==1:
      insert1()
   elif c==2:
      search1()
   elif c==3:
      display1()
   elif c==4:
      update1()
   elif c==5:
      delete1()
   elif c==6:
      selection()
   else:
      func_patient()
   func_patient()

#***********************************************************************************************************#

def func_doctor():
   cls()
   print('      WELCOME TO DOCTOR MANAGEMENT SYSTEM      ')
   print('                                               ')
   print('           1. NEW DOCTOR ENTRY                 ')
   print('           2. SEARCH DOCTORS                   ')
   print('           3. VIEW all DOCTORS                 ')
   print('           4. UPDATE DOCTOR                    ')
   print('           5. DELETE DOCTOR                    ')
   print('           6. Go BACK to MAIN MENU             ')
   
   c=int(input("       Enter ur choice (1-6) : "))
   if c==1:
      insert2()
   elif c==2:
      search2()
   elif c==3:
      display2()   
   elif c==4:
      update2()
   elif c==5:
      delete2()
   elif c==6:
      selection()
   else:
      func_doctor()
   func_doctor()

#***********************************************************************************************************#

def func_treatment():
   cls()
   print('       TREATMENT MANAGEMENT in HOSPITAL           ')
   print('                                                  ')
   print('           1. BOOK APPOINTMENT                    ')
   print('           2. SEARCH APPOINTMENT                  ')
   print('           3. UPDATE / DELETE Appointement        ')
   print('           4. NEW TREATMNENT Entry                ')
   print('           5. TREATMENT REPORTS                   ')
   print('           6. Go BACK to MAIN MENU                ')
   c=int(input("       Enter ur choice (1-6) : "))
   if c==1:
      insert3()
   elif c==2:
      search3()
   elif c==3:
      update3()
   elif c==4:
      treat3()
   elif c==5:
      report3()
   elif c==6:
      selection()
   else:
      func_treatment()
   func_treatment()

#***********************************************************************************************************#

def insert1():
   db = mysql.connector.connect(user='root', password='', host='localhost',database='hospital')
   cr = db.cursor()
   cr.execute("select pid from serial")
   dset=cr.fetchone()
   mno=int(dset[0])
   print("Patient Number         :",mno)
   pname=input("Enter Patient Name     : ")
   gnd = input("Enter Gender[m/f]      : ")
   dob = input("Enter DOB[yyyy-mm-dd]  : ")
   phn = input("Enter Phone No.        : ")
   addr= input("Enter Address          : ")
   csr1 = db.cursor()
   csr2 = db.cursor()
   csr3 = db.cursor()
   csr3.execute("select count(pid) from patient where pname='"+pname+"' and phn='"+phn+"' and addr='"+addr+"'")
   r=csr3.fetchone()
   if(r[0]>0):
      print("--------------- SIMILAR ENTRY Exists Already -------------")
   else:
      sql="INSERT INTO patient(pid,pname,gend,dob,phn,addr) VALUES('%d','%s','%s','%s','%s','%s')"%(mno,pname,gnd,dob,phn,addr)
      try:
         csr1.execute(sql)
         csr2.execute("update serial set pid=pid+1")
         db.commit()
         print('---------------NEW RECORD Successfully Added-----------------------')
      except:
         db.rollback()
   x=input('_______________Press ENTER to Continue_____________________________')
   db.close()   
   
#**************************************************************************************************************#

def display1():
   i=0
   try:
      db = mysql.connector.connect(user='root', password='', host='localhost',database='hospital')
      cursor = db.cursor()
      sql = "SELECT *,timestampdiff(year,dob,now()) FROM patient;"
      cursor.execute(sql)
      results = cursor.fetchall()
      print('\nP.ID.   Name                     Gend.     Age     Phone          Address')
      print('---------------------------------------------------------------------------')
      for c in results:
         i+=1
         pid=str(c[0])+" "*(7-len(str(c[0])))
         pname=c[1]+" "*(24-len(c[1]))
         gnd=c[2]+" "*(9-len(c[2]))
         age=str(c[6])+" "*(7-len(str(c[6])))
         phn=c[4]+" "*(14-len(c[4]))
         addr=c[5]
         print(pid,pname,gnd,age,phn,addr)
      print('----------------------- Total Records =',i,' --------------------------------')
   except Exception as e:
      print ("Error: ", e)
   x=input('_______________Press ENTER to Continue_____________________________')
   db.close()
   
#**************************************************************************************************************#

def search1():
   i=0
   numb=input("Enter Patient ID / Name to Search : ")
   if(numb.isnumeric()):
      sql = "SELECT *,timestampdiff(year,dob,now()) FROM patient WHERE pid="+numb
   else:
      sql = "SELECT *,timestampdiff(year,dob,now()) FROM patient WHERE pname like '%"+numb+"%'"
   try:
      db = mysql.connector.connect(user='root', password='', host='localhost',database='hospital')
      cursor = db.cursor()
      cursor.execute(sql)
      results = cursor.fetchall()
      print('\nP.ID.   Name                     Gend.     Age     Phone          Address')
      print('---------------------------------------------------------------------------')
      for c in results:
         i+=1
         pid=str(c[0])+" "*(7-len(str(c[0])))
         pname=c[1]+" "*(24-len(c[1]))
         gnd=c[2]+" "*(9-len(c[2]))
         age=str(c[6])+" "*(7-len(str(c[6])))
         phn=c[4]+" "*(14-len(c[4]))
         addr=c[5]
         print(pid,pname,gnd,age,phn,addr)
      print('----------------------- Total Records =',i,' --------------------------------')
   except Exception as e:
      print ("Error: ", e)
   x=input('_______________Press ENTER to Continue_____________________________')
   db.close()
   
#*************************************************************************************************************#

def update1():
   numb=input("Enter Patient Number to Update : ")
   try:
      db = mysql.connector.connect(user='root', password='', host='localhost',database='hospital')
      cursor = db.cursor()
      sql = "SELECT * FROM patient where pid="+numb
      cursor.execute(sql)
      rs = cursor.fetchone()
      if(rs==None):
         print('---------------No Such Records Found--------------------')
      else:
         pid=rs[0]
         pname=rs[1]
         gnd=rs[2]
         dob=rs[3]
         phn=rs[4]
         addr=rs[5]
         print("\nPatient Number : ",pid)
         print("Name : ",pname)
         sn=input("      New Name   : ")
         print("Gender : ",gnd)
         gd=input("      New Gender : ")
         print("D.O.B. : ",dob)
         dt=input("      New D.O.B. : ")
         print("Phone : ",phn)
         pn=input("      New Phone  : ")
         print("Addr. : ",addr)
         ad=input("      New Addr.  : ")
         if(sn==""):
            sn=pname
         if(gd==""):
            gd=gnd
         if(dt==""):
            dt=dob
         if(pn==""):
            pn=phn
         if(ad==""):
            ad=addr
         try:
            sql = "UPDATE patient SET pname='%s', gend='%s', dob='%s', phn='%s', addr='%s' where pid=%d" % (sn,gd,dt,pn,ad,pid)
            cursor.execute(sql)
            db.commit()
            print('---------------RECORD Updated Successfully --------------------')
         except Exception as e:
            print (e)
            db.rollback()
   except Exception as e:
      print ("Error: ", e)
   x=input('_______________Press ENTER to Continue_____________________________')
   db.close()
   
#*******************************************************************************************************************#

def delete1():
   pid=input("Enter Patient Number to Delete : ").strip()
   try:
      db = mysql.connector.connect(user='root', password='', host='localhost',database='hospital')
      cursor = db.cursor()
      sql = "SELECT *,timestampdiff(year,dob,now()) FROM patient where pid="+pid
      cursor.execute(sql)
      rs = cursor.fetchone()
      if(rs==None):
         print('---------------No Such Records Found--------------------')
      else:
         age,pname,phn=rs[6],rs[1],rs[4]
         print("Record Found as- ",pname," [Age:",age,"]\t\tPhone:",phn)
         try:
           sql = "delete from patient where pid=%s"%(pid)
           ans=input("Are you sure you want to delete the record(y/n) : ")
           if(ans=='y' or ans=='Y'):
              cursor.execute(sql)
              db.commit()
              print('---------------RECORD DELETED Successfully --------------------')
         except Exception as e:
            print (e)
            db.rollback()
   except Exception as e:
      print("Error: ",e)
   x=input('_______________Press ENTER to Continue_____________________________')
   db.close()
   
#**********************************************************************************************************************#

def insert2():
   db = mysql.connector.connect(user='root', password='', host='localhost',database='hospital')
   cur = db.cursor()
   cur.execute("select did from serial")
   rs = cur.fetchone()
   did =int(rs[0])
   print("Doctor Number          :",did)
   dname=input("Enter Doctor Name      : ")
   qual= input("Enter Qualification    : ")
   dept= input("Enter Department       : ")
   phn = input("Enter Phone            : ")
   csr1 = db.cursor()
   csr2 = db.cursor()
   csr3 = db.cursor()
   csr3.execute("select did,dept from doctor where dname='"+dname+"' and qual='"+qual+"' and phn='"+phn+"'")
   r=csr3.fetchall()
   if(r):
      print("SIMILAR Entry Already Exists as D.Id.: "+r[0]+" , with Department: "+r[1])
   sql="INSERT INTO doctor(did,dname,qual,dept,phn) VALUES('%d','%s','%s','%s','%s')"%(did,dname,qual,dept,phn)
   try:
      csr1.execute(sql)
      csr2.execute("update serial set did=did+1")
      db.commit()
      print('---------------NEW RECORD Successfully Added-----------------------')
   except:
      db.rollback()
   x=input('_______________Press ENTER to Continue_____________________________')
   db.close()   
         
#***********************************************************************************************************************#

def display2():
   i=0
   try:
      db = mysql.connector.connect(user='root', password='', host='localhost',database='hospital')
      cursor = db.cursor()
      sql = "SELECT * FROM doctor"
      cursor.execute(sql)
      results = cursor.fetchall()
      print('\nD.ID    D.Name                    Qualification             Department          Phone     ')
      print('------------------------------------------------------------------------------------------')
      for c in results:
         i+=1
         did=str(c[0])+" "*(7-len(str(c[0])))
         name=c[1]+" "*(25-len(c[1]))
         qual=c[2]+" "*(25-len(c[2]))
         dept=c[3]+" "*(19-len(c[3]))
         phn=c[4]
         print(did,name,qual,dept,phn)
      print('-------------------------------- Total Records =',i,' --------------------------------------')
   except Exception as e:
      print ("Error: ", e)
   x=input('_______________________Press ENTER to Continue_____________________________')
   db.close()
   
#**************************************************************************************************************#

def search2():
   x=input("Enter Doctor Name / Department to Search : ")
   sql = "SELECT * FROM doctor WHERE dname like '%"+x+"%' or dept like '%"+x+"%'"
   try:
      i=0
      db = mysql.connector.connect(user='root', password='', host='localhost',database='hospital')
      cursor = db.cursor()         
      cursor.execute(sql)
      results = cursor.fetchall()
      print('\nD.ID    D.Name                    Qualification             Department          Phone     ')
      print('------------------------------------------------------------------------------------------')
      for c in results:
         i+=1
         did=str(c[0])+" "*(7-len(str(c[0])))
         name=c[1]+" "*(25-len(c[1]))
         qual=c[2]+" "*(25-len(c[2]))
         dept=c[3]+" "*(19-len(c[3]))
         phn=c[4]
         print(did,name,qual,dept,phn)
      print('-------------------------------- Total Records =',i,' --------------------------------------')
   except Exception as e:
      print ("Error: ", e)
   x=input('_______________________Press ENTER to Continue_____________________________')
   db.close()
   
#***********************************************************************************************************************#

def update2():
   did=input("Enter Doctor ID to Update : ").strip()
   try:
      db = mysql.connector.connect(user='root', password='', host='localhost',database='hospital')
      cursor = db.cursor()
      sql = "SELECT * FROM doctor where did="+did
      cursor.execute(sql)
      rs = cursor.fetchone()
      if(rs==None):
         print('---------------No Such Records Found--------------------')
      else:
         name=rs[1]
         qual=rs[2]
         dept=rs[3]
         phn=rs[4]
         print("\nDoctor Number : ",did)
         print("Name : ",name)
         nm=input("      New Name   : ")
         print("Qualification : ",qual)
         qu=input("      New Qual. : ")
         print("Department : ",dept)
         de=input("      New Dept.  : ")
         print("Phone : ",phn)
         pn=input("      New Phone  : ")
         if(nm==""):
            nm=name
         if(qu==""):
            qu=qual
         if(de==""):
            de=dept
         if(pn==""):
            pn=phn
         try:
            sql = "UPDATE doctor SET dname='%s', qual='%s', dept='%s', phn='%s' where did=%d" %(nm,qu,de,pn,int(did))
            cursor.execute(sql)
            db.commit()
            print('---------------RECORD Updated Successfully --------------------')
         except Exception as e:
            print (e)
            db.rollback()
   except Exception as e:
      print ("Error: ", e)
   x=input('_______________Press ENTER to Continue_____________________________')
   db.close()
   
#*******************************************************************************************************************#

def delete2():
   numb=input("Enter Doctor Number to Delete : ")
   try:
      db = mysql.connector.connect(user='root', password='', host='localhost',database='hospital')
      cursor = db.cursor()
      sql = "SELECT * FROM doctor where did="+numb
      cursor.execute(sql)
      rs = cursor.fetchone()
      if(rs==None):
         print('---------------No Such Records Found--------------------')
      else:
         did=rs[0]
         name=rs[1]
         dept=rs[3]
         print("Record Found as:",name," [",did,"]\t\tDepartment:",dept)
         try:
           sql = "delete from doctor where did=%s" %(numb)
           ans=input("Are you sure you want to delete the record(y/n) : ")
           if(ans=='y' or ans=='Y'):
              cursor.execute(sql)
              db.commit()
              print('---------------RECORD DELETED Successfully --------------------')
         except Exception as e:
            print (e)
            db.rollback()
   except Exception as e:
      print("Error: ",e)
   x=input('_______________Press ENTER to Continue_____________________________')
   db.close()
   
#***********************************************************************************************************#

def insert3():
   pid=input("Enter Patient ID for Appointment : ").strip()
   try:
      db = mysql.connector.connect(user='root', password='', host='localhost',database='hospital')
      cursor = db.cursor()
      cursor2 = db.cursor()
      cursor3 = db.cursor()
      cursor4 = db.cursor()
      cursor.execute("SELECT *,timestampdiff(year,dob,now()) FROM patient where pid="+pid)
      results = cursor.fetchone()
      if(results==None):
         print('---------------No Such patient Records Found--------------------')
      else:
         pname = results[1]
         age,phn = results[6],results[4]
         print("P.ID:",pid,"\tName :",pname,"[Age:"+str(age)+"]\t\tPhone :",phn)           
         x=input("Enter DoctorID / Name / Department to Search : ")
         if(x.isnumeric()):
            x="SELECT * FROM doctor WHERE did="+x
         else:
            x="SELECT * FROM doctor WHERE dname like '%"+x+"%' or dept like '%"+x+"%'"
         cursor2.execute(x)
         results2 = cursor2.fetchall()
         if(results2==None):
            print("--------------------No Such Doctor Records Found--------------------")
         else:
            for r in results2:
               did,dname,qual,dept=r[0],r[1],r[2],r[3]
            print(did," - \t - ",dname," - \t - ",qual," - \t - ",dept)
            did=input("\nEnter Doctor ID to book Appointment: ")
            cursor3.execute("select * from treatment where status='BOOK' and pid="+pid+" and did="+did)
            results3=cursor3.fetchone()
            if(results3):
               print("_____________ Similar Appointment found on ",results3[2]," _______________")
            else:
               adt=input("Date of Appointment [yyyy-mm-dd]: ")
               if(adt==""):
                  adt=date.today()
               cursor4.execute("insert into treatment(did,pid,adate,status) values(%s,%s,'%s','%s')"%(did,pid,adt,'BOOK'))
               db.commit()
               print("_____________Appointment Booked on",adt,"____________")
   except Exception as e:
      print ("Error: ", e)
   x=input('_______________Press ENTER to Continue_____________________________')
   db.close()
         
#***********************************************************************************************************************#

def search3():
   c=int(input("Press 1.Search by doctor\t2.Search by Patient\t3.Search by Date : "))
   if(c==1):
      bn=input("Enter Doctor No. : ")
      sql="select * from treatment where did="+bn+" order by adate desc"
   elif(c==2):
      mn=input("Enter Patient No. : ")
      sql="select * from treatment where pid="+mn+" order by adate desc"
   elif(c==3):
      dt=input("Enter Date[yyyy-mm-dd] : ")
      sql="select * from treatment where adate='"+dt+"' order by did"
   else:
      sql=""
   try:
      i=0
      db = mysql.connector.connect(user='root', password='', host='localhost',database='hospital')
      cursor = db.cursor()
      cursor.execute(sql)
      results = cursor.fetchall()      
      print("\nPatientID      DoctorID       AppointmentDate    Status")
      print('-----------------------------------------------------------------')
      for r in results:
         i+=1
         pid=str(r[0])+" "*(15-len(str(r[0])))
         did=str(r[1])+" "*(15-len(str(r[1])))
         adt=str(r[2])+" "*(20-len(str(r[2])))
         sta=str(r[3])
         print (pid+did+adt+sta)
      print('---------------- Total Records = ',i,' ----------------------------')
   except Exception as e:
      print ("Error: ", e)
   x=input('_______________Press ENTER to Continue_____________________________')
   db.close()

#***********************************************************************************************************************#

def update3():
   bn=input("Enter Patient No.: ").strip()
   sql="select treatment.*,patient.pname,doctor.dname from treatment,doctor,patient where doctor.did=treatment.did and patient.pid=treatment.pid and status='BOOK' and treatment.pid="+bn
   try:
      db = mysql.connector.connect(user='root', password='', host='localhost',database='hospital')
      cursor = db.cursor()
      cursor.execute(sql)
      results=cursor.fetchall()
      if(results==None):
         print("-------------------- No Such Record Exists ----------------------")
      else:
         for r in results:
            print("Doctor:",r[6],"[ID:",r[1],"]\t---\tPatient:",r[5],"[ID:",r[0],"]\t-\tAppointmentDate:",r[2])
            did=input("Enter DoctorID to Update Appointment: ")
            if(not did==""):
               ut=input("Press C to Cancel / M to Modify : ")
               if(ut in "Cc"):
                  sql="delete from treatment where pid="+bn+" and did="+did+" and status='BOOK'"
               elif(ut in "Mm"):
                  at=input("New AppoinmentDate [yyyy-mm-dd] : ")
                  if(at==""):
                     at=date.today()
                  sql="update treatment set adate='"+str(at)+"' where pid="+bn+" and did="+did+" and status='BOOK'"
            cursor.execute(sql)
            db.commit()
            print('---------------RECORD Updated Successfully --------------------')
   except Exception as e:
      print ("Error: ", e)
   x=input('_______________Press ENTER to Continue_____________________________')

#***********************************************************************************************************************#

def treat3():
   bn=input("Enter Patient No.: ").strip()
   sql="select treatment.*,patient.pname,doctor.dname from treatment,doctor,patient where doctor.did=treatment.did and patient.pid=treatment.pid and adate=curdate() and status='BOOK' and treatment.pid="+bn
   try:
      db = mysql.connector.connect(user='root', password='', host='localhost',database='hospital')
      cursor,cursor2,cursor3 = db.cursor(),db.cursor(),db.cursor()
      cursor.execute(sql)
      results=cursor.fetchall()
      if(results==None):
         print("-------------------- No Such Record Exists ----------------------")
      else:
         for r in results:
            print("Doctor:",r[6],"[ID:",r[1],"]\t---\tPatient:",r[5],"[ID:",r[0],"]\t-\tAppointmentDate:",r[2])
         did=input("Enter DoctorID for Treatment: ")
         if(not did==""):
            fees=input("Enter Fees Paid: ")
            cursor2.execute("update treatment set status='PAID',fees="+fees+" where pid="+bn+" and did="+did+" and status='BOOK'")
            db.commit()
            print('---------------Bill Generated Successfully --------------------')
   except Exception as e:
      print ("Error: ", e)
   x=input('_______________Press ENTER to Continue_____________________________')
   
#***********************************************************************************************************************#

def report3():
   try:
      db = mysql.connector.connect(user='root', password='', host='localhost',database='hospital')
      csr0,csr1 = db.cursor(),db.cursor()
      csr0.execute("drop view if exists tv")
      csr1.execute("create view tv as select monthname(adate) as TM, year(adate) as TY, count(adate) as TB,count(fees) as TT, sum(fees) as TF from treatment group by adate")
      db.commit()
   except  Exception as e:
      print ("Error: ", e)
   c=int(input("Press 1.Doctors Report      2.Patients Report      3.Daily Report      4.Monthly Report: "))
   if(c==1):
      sql="select doctor.did as DoctorID,doctor.dname as DoctorName,doctor.dept as Department,count(adate) as Total_Booked,count(fees) as Total_Treated from treatment,doctor where treatment.did=doctor.did group by (treatment.did)"
   elif(c==2):
      sql="select patient.pid as PatientID,patient.pname as PatientName,patient.phn as Phone,count(adate) as Total_Booked,count(fees) as Total_Paid from treatment,patient where treatment.pid=patient.pid group by (treatment.pid)"
   elif(c==3):
      sql="select adate as Date, dayname(adate) as Day, count(adate) as Total_Booked,count(fees) as Total_Treated, sum(fees) as TotalFees from treatment where month(adate)=month(now()) and year(adate)=year(now()) group by adate"
   elif(c==4):
      sql="select tm as Month, ty as Year, sum(tb) as Total_Booked,sum(tt) as Total_Treated, sum(tf) as TotalFees from tv group by tm,ty"
   else:
      sql=""
   try:
      i=0
      db = mysql.connector.connect(user='root', password='', host='localhost',database='hospital')
      cursor = db.cursor()
      cursor.execute(sql)
      results = cursor.fetchall()
      head=cursor.column_names
      print("\n"+head[0]+"         "+head[1]+"          "+head[2]+"              "+head[3]+"              "+head[4])
      print('-----------------------------------------------------------------------------------------------------')
      for r in results:
         i+=1
         p1=str(r[0])+" "*(15-len(str(r[0])))
         p2=str(r[1])+" "*(20-len(str(r[1])))
         p3=str(r[2])+" "*(25-len(str(r[2])))
         p4=str(r[3])+" "*(25-len(str(r[3])))
         p5=str(r[4])
         print (p1+p2+p3+p4+p5)
      print('-------------------- Total Records = ',i,' --------------------------------')
   except Exception as e:
      print ("Error: ", e)
   x=input('_______________Press ENTER to Continue_____________________________')
   db.close()

#`````````````````````````````````````` MAIN PROGRAM STARTS HERE ```````````````````````````````````````````````````````#

checkdb()
checktbl()
selection()
