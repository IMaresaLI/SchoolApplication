################################################
################################################
################################################
#########*******###*******####**********########
########**#####**#**#####**###**######**########
########**#####**#**#####**###**######**########
########**#####**#**#####**###**********########
########**#####**#**#####**###**################
########**#####**#**#####**###**################
########**######***######**###**################
########**###############**###**################
########**###############**###**################
################################################
########Copyright © Maresal Programming#########
################################################

import sqlite3


class sqliteData():
    def __init__(self):
        self.connect = sqlite3.connect("school.db")
        self.cursor = self.connect.cursor()


   
    def studentAdd(self,tc,studentName,studentLastname,birthday,studentAddr,studentClass,studentNumber):
        self.cursor.execute("INSERT INTO students (tc_no,studentName,studentLastname,birthday,studentAddr,studentClass,studentNumber) VALUES (?,?,?,?,?,?,?)",
                       (tc, studentName,studentLastname,birthday, studentAddr,studentClass,studentNumber))
        self.connect.commit()
        self.connect.close()
        print("işlem Tamamlandı.")

    def parentAdd(self,parentName,parentLastname,parentTelNo,parentDegree,studentId):
        self.cursor.execute(f"INSERT INTO parents (parentName,parentLastname,parentTelNo,parentDegree,studentId) VALUES (?,?,?,?,?)",
                       (parentName, parentLastname,parentTelNo,parentDegree, studentId))
        self.connect.commit()
        self.connect.close()
        print("işlem Tamamlandı.")


    def getData(self,tblname,id=None,tc=None,studentid=None,all=True):
        if all == True:
            self.cursor.execute(f"Select * from {tblname}")
            data = self.cursor.fetchall()
            self.connect.close()
            return data
        else :
            if id == None and studentid == None:
                self.cursor.execute(f"Select * from {tblname} where tc_no='{tc}'")
                data = self.cursor.fetchone()
                self.connect.close()
                return data
            elif studentid == None and tc == None :
                self.cursor.execute(f"Select * from {tblname} where id='{id}'")
                data = self.cursor.fetchone()
                self.connect.close()
                return data
            else :
                self.cursor.execute(f"Select * from {tblname} where studentid={studentid}")
                data = self.cursor.fetchone()
                self.connect.close()
                return data

    def studentUpdate(self,tc_no,studentName,studentLastname,birthday,studentAddr,studentClass,studentNumber,id):
        self.cursor.execute(f"Update students SET tc_no='{tc_no}',studentName='{studentName}',studentLastname='{studentLastname}',birthday='{birthday}',studentAddr='{studentAddr}',studentClass='{studentClass}',studentNumber='{studentNumber}' where id='{id}'")
        self.connect.commit()
        self.connect.close()
        print("işlem Tamamlandı.")

    def parentUpdate(self,parentName,parentLastname,parentTelNo,parentDegree,id):
        self.cursor.execute(f"Update parents SET parentName='{parentName}',parentLastname='{parentLastname}',parentTelNo='{parentTelNo}',parentDegree='{parentDegree}' where id='{id}'")
        self.connect.commit()
        self.connect.close()
        print("işlem Tamamlandı.")

    def getLessonData(self,id):
        self.cursor.execute(f"Select * from studentsLessons where studentId={id}")
        data = self.cursor.fetchall()
        self.connect.close()
        return data
    
    def LessonAdd(self,studentId,lesson,note):
        self.cursor.execute(f"INSERT INTO studentsLessons (studentId,{lesson}) VALUES (?,?)",
                       (studentId,note))
        self.connect.commit()
        self.connect.close()
        print("işlem Tamamlandı.")

    def LessonUpdate(self,lesson,note,id):
        self.cursor.execute(f"Update studentsLessons SET {lesson}='{note}' where studentId='{id}'")
        self.connect.commit()
        self.connect.close()
        print("işlem Tamamlandı.")
