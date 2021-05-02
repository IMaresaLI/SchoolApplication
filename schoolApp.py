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

from datetime import datetime
from PyQt5 import QtWidgets,QtCore
import sys,base64,time
from schoolAppDesing import Ui_MainWindow
from DatabaseManager import sqliteData

class SchoolApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(SchoolApp,self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setStyleSheet(open("style.css","r").read())
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.menuItems(True)

        self.ui.ExitBtn.clicked.connect(self.exitButton)
        self.ui.MinimizeBtn.clicked.connect(self.minimize)
        self.ui.FullScreenBtn.clicked.connect(self.fullscreen)
        self.ui.menuBtn.clicked.connect(lambda:self.MenuAnimation(QtCore.QEasingCurve.InOutQuad))

        self.ui.homeBtn.clicked.connect(self.homePage)
        self.ui.authorizenLoginBtn.clicked.connect(self.loginPage)
        self.ui.loginBtn.clicked.connect(self.login)
        self.ui.LogoutBtn.clicked.connect(self.logout)

        self.ui.studentsOperationsBtn.clicked.connect(self.studentPage)
        self.ui.studentSave.clicked.connect(self.studentAdd)
        self.ui.studentTcTbx_2.textEdited.connect(self.studentUpdateLoad)
        self.ui.studentUpdateBtn.clicked.connect(self.studentUpdate)
        self.ui.NotBilgisi.doubleClicked.connect(self.lessonUpdate)
        self.ui.lessonAdd.clicked.connect(self.lessonAdd)
        self.ui.ClearAddBtn.clicked.connect(self.clearAdd)
        self.ui.ClearUpdateBtn.clicked.connect(self.clearUpdate)
        

        self.ui.teacherOperationsBtn.clicked.connect(self.teacherOperation)
        self.ui.settingBtn.clicked.connect(self.setting)
        self.ui.notificationBtn.clicked.connect(self.notification)



    def homePage(self):
        self.ui.stackedWidget.setCurrentIndex(0)

    def notification(self):
        pass
    
    def loginPage(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def login(self):
        tc = self.ui.tcTbx.text()
        pw = self.ui.pwTbx.text()
        sorgu = sqliteData().getData("authorities",tc=tc,all=False)
        if sorgu == None:
            QtWidgets.QMessageBox.information(self,"Hata","Girdiğiniz bilgiler yanlış.")
        else :
            pwdecode = base64.b85decode(sorgu[3].encode()).decode()
            if pw == pwdecode :
                QtWidgets.QMessageBox.information(self,"Giriş Onayı","Giriş Onaylandı.")
                self.ui.authorizenLoginBtn.setHidden(True)
                self.ui.studentsOperationsBtn.setHidden(False)
                self.ui.teacherOperationsBtn.setHidden(False)
                self.ui.LogoutBtn.setHidden(False)
                self.ui.userStatusLbl.setText("Giriş yapan kişi : %s" %sorgu[1])
                self.ui.stackedWidget.setCurrentIndex(0)
            else :
                QtWidgets.QMessageBox.warning(self,"Giriş Hata","Girdiğiniz şifre yanlıştır.")
        
    def logout(self):
        self.ui.authorizenLoginBtn.setHidden(False)
        self.ui.studentsOperationsBtn.setHidden(True)
        self.ui.teacherOperationsBtn.setHidden(True)
        self.ui.LogoutBtn.setHidden(True)
        self.ui.userStatusLbl.setText("Giriş yapılmadı.")
        self.ui.stackedWidget.setCurrentIndex(0)
        QtWidgets.QMessageBox.warning(self,"Çıkış Bildirimi","Mevcut hesaptan Çıkıldı.")

    def studentPage(self):
        self.ui.classCbx.clear()
        self.ui.studentClassCbx.clear()
        self.AllStudent()
        self.ui.stackedWidget.setCurrentIndex(2)
        data = sqliteData().getData("classes")
        for i in data:
            self.ui.classCbx.addItem(i[1])
            self.ui.studentClassCbx.addItem(i[1])

    def studentAdd(self):
        studentName = self.ui.studentNameTbx.text()
        studentLastname = self.ui.studentLastNameTbx.text()
        tc_no = self.ui.studentTcTbx.text()
        birthday = str(self.ui.dateEdit_2.date().getDate()).split(")")[0].split("(")[1]
        print(birthday)
        addr = self.ui.studentAddrsTbx.toPlainText()
        studentClass = self.ui.studentClassCbx.currentText()
        studentNumber = self.ui.studentNumber_2.text()

        parentName = self.ui.parentNameTbx.text()
        parentLastname = self.ui.parentLastnameTbx.text()
        parentTel = self.ui.parentTelTbx.text()
        degree = self.ui.degreeTbx.text()
        if studentName != "" and studentLastname != "" and tc_no != "" and birthday != "" and addr != "" and studentClass != "" and studentNumber != "" and parentTel != "":
            sqliteData().studentAdd(tc_no,studentName,studentLastname,str(birthday),addr,studentClass,studentNumber)
            data = sqliteData().getData("students",tc=tc_no,all=False)
            sqliteData().parentAdd(parentName,parentLastname,parentTel,degree,data[0])
            self.clearAdd()
            QtWidgets.QMessageBox.information(self,"Onaylama","Öğrencinin kaydı başarıyla yapıldı.")
            self.ui.stackedWidget.setCurrentIndex(0)
        else :
            QtWidgets.QMessageBox.information(self,"Hata","Tüm bilgilerin girilmesi zorunludur.")

    def studentUpdateLoad(self):
        try :
            tc_no = self.ui.studentTcTbx_2.text()
            studentData = sqliteData().getData("students",tc=int(tc_no),all=False)
            self.ui.studentNameTbx_2.setText(studentData[2])
            self.ui.studentLastNameTbx_2.setText(studentData[3])
            date = studentData[4].split(",")
            self.ui.dateEdit_2.setDateTime(datetime(int(date[0]),int(date[1]),int(date[2])))
            self.ui.studentAddrsTbx_2.setText(studentData[5])
            self.ui.classCbx.setCurrentText(studentData[6])
            self.ui.studentNumber.setText(studentData[7])
            parentData = sqliteData().getData("parents",studentid=studentData[0],all=False)
            self.ui.parentNameTbx_2.setText(parentData[1])
            self.ui.parentLastnameTbx_2.setText(parentData[2])
            self.ui.parentTelTbx_2.setText(parentData[3])
            self.ui.degreeTbx_2.setText(parentData[4])
            self.lessonGet(studentData[0])

        except Exception as err:
            print(err)

    def studentUpdate(self):
        try :
            tc = int(self.ui.studentTcTbx_2.text())
            data = sqliteData().getData("students",tc=tc,all=False)
            print(data[0])
            name = self.ui.studentNameTbx_2.text()
            lastname = self.ui.studentLastNameTbx_2.text()
            birthday = str(self.ui.dateEdit_2.date().getDate()).split(")")[0].split("(")[1]
            print(birthday)
            addr = self.ui.studentAddrsTbx_2.toPlainText()
            classes = self.ui.classCbx.currentText()
            sNumber = self.ui.studentNumber.text()
            prName = self.ui.parentNameTbx_2.text()
            prLastname = self.ui.parentLastnameTbx_2.text()
            prTel = self.ui.parentTelTbx_2.text()
            prDgr = self.ui.degreeTbx_2.text()
            if tc != "" and name != "" and lastname != "" and addr != "" and classes != "" and sNumber != "" and prName != "" and prLastname != "" and prTel != "" and prDgr != "":
                print("Çalışt-ı")
                result = QtWidgets.QMessageBox.question(self,"Güncelleme Onayı","Güncellemeyi onaylıyor musunuz?",QtWidgets.QMessageBox.StandardButton.Ok | QtWidgets.QMessageBox.StandardButton.Cancel)
                if result == QtWidgets.QMessageBox.StandardButton.Ok:
                    sqliteData().studentUpdate(tc,name,lastname,str(birthday),addr,classes,sNumber,data[0])
                    sqliteData().parentUpdate(prName,prLastname,prTel,prDgr,data[0])
                    self.clearUpdate()
                    QtWidgets.QMessageBox.information(self,"Onaylama","Öğrencinin kaydı başarıyla güncellendi.")
            else :
                QtWidgets.QMessageBox.information(self,"Hata","Tüm bilgilerin girilmesi zorunludur.")
        except :
            pass

    def clearAdd(self):
        self.ui.studentNameTbx.clear()
        self.ui.studentLastNameTbx.clear()
        self.ui.studentTcTbx.clear()
        self.ui.studentAddrsTbx.clear()
        self.ui.studentNumber_2.clear()

        self.ui.parentNameTbx.clear()
        self.ui.parentLastnameTbx.clear()
        self.ui.parentTelTbx.clear()
        self.ui.degreeTbx.clear()

    def clearUpdate(self):
        self.ui.studentTcTbx_2.clear()
        self.ui.studentNameTbx_2.clear()
        self.ui.studentLastNameTbx_2.clear()
        self.ui.studentAddrsTbx_2.clear()
        self.ui.studentNumber.clear()
        self.ui.parentNameTbx_2.clear()
        self.ui.parentLastnameTbx_2.clear()
        self.ui.parentTelTbx_2.clear()
        self.ui.degreeTbx_2.clear()

    def lessonGet(self,id):
        self.ui.NotBilgisi.clear()
        data = sqliteData().getLessonData(id)
        self.ui.NotBilgisi.setColumnWidth(0,70)
        self.ui.NotBilgisi.setColumnWidth(1,70)
        self.ui.NotBilgisi.setColumnWidth(2,70)
        self.ui.NotBilgisi.setColumnWidth(3,70)
        self.ui.NotBilgisi.setColumnWidth(4,70)
        self.ui.NotBilgisi.setColumnWidth(5,70)

        if data == None:
            pass
        else :
            for i in data :
                item = QtWidgets.QTreeWidgetItem(self.ui.NotBilgisi)
                item.setText(0,str(i[2]))
                item.setText(1,str(i[3]))
                item.setText(2,str(i[4]))
                item.setText(3,str(i[5]))
                item.setText(4,str(i[6]))
                item.setText(5,str(i[7]))
                
    def lessonAdd(self):
        try:
            items = ["Matematik","DilveAnlatım","Biyoloji","Kimya","Geometri","Edebiyat"]
            item, ok = QtWidgets.QInputDialog.getItem(self,"Ders Not Girişi","Girmek istediğiniz dersi seçiniz.",items)
            if item and ok :
                note,ok = QtWidgets.QInputDialog.getInt(self,"Not Girişi","Notu yazınız :")
                if note and ok:
                    data = sqliteData().getData("students",tc=self.ui.studentTcTbx_2.text(),all=False)
                    if note > -1:
                        sqliteData().LessonAdd(data[0],item,note)
                        QtWidgets.QMessageBox.information(self,"Onay","Ders notu eklendi.")
                    else :
                        sqliteData().LessonAdd(data[0],item,None)
                        QtWidgets.QMessageBox.information(self,"Onay","Ders notu eklendi.")
                    self.lessonGet(data[0])
                    
        except Exception as err :
            print(err)

    def lessonUpdate(self):
        try:
            items = ["Matematik","DilveAnlatım","Biyoloji","Kimya","Geometri","Edebiyat"]
            item, ok = QtWidgets.QInputDialog.getItem(self,"Ders Not Girişi","Girmek istediğiniz dersi seçiniz.",items)
            if item and ok :
                note,ok = QtWidgets.QInputDialog.getInt(self,"Not Girişi","Notu yazınız :")
                if note and ok:
                    data = sqliteData().getData("students",tc=self.ui.studentTcTbx_2.text(),all=False)
                    if note > -1:
                        sqliteData().LessonUpdate(item,note,data[0])
                        QtWidgets.QMessageBox.information(self,"Onay","Ders Notu Güncellendi.")
                    else :
                        sqliteData().LessonUpdate(item,"None",data[0])
                        QtWidgets.QMessageBox.information(self,"Onay","Ders Notu Güncellendi.")
                    self.lessonGet(data[0])
        except Exception as err :
            print(err)

    def AllStudent(self):
        self.ui.treeWidget_2.clear()
        self.ui.treeWidget_2.setColumnWidth(5,140)
        studentData = sqliteData().getData("students")
        for sData in studentData:
            parentData = sqliteData().getData("parents",id=sData[0],all=False)
            item = QtWidgets.QTreeWidgetItem(self.ui.treeWidget_2)
            item.setText(0,str(sData[1]))
            item.setText(1,str(sData[2]))
            item.setText(2,str(sData[3]))
            item.setText(3,str(sData[4]))
            item.setText(4,str(sData[6]))
            item.setText(5,str(sData[7]))
            item.setText(6,str(parentData[1]))
            item.setText(7,str(parentData[2]))
            item.setText(8,str(parentData[3]))

    def fullscreen(self):
        if self.isFullScreen():
            self.showNormal()
        else :
            self.showFullScreen()

    def minimize(self):
        self.showMinimized()

    def exitButton(self):
        app.exit()

    def mousePressEvent(self, event):
        try :
            if event.buttons() == QtCore.Qt.LeftButton:
                self.dragPos = event.globalPos()
                event.accept()
        except :
            pass

    def mouseMoveEvent(self, event):
        try:
            if event.buttons() == QtCore.Qt.LeftButton:
                self.move(self.pos() + event.globalPos() - self.dragPos)
                self.dragPos = event.globalPos()
                event.accept()
        except :
            pass

    def MenuAnimation(self,Animation):
        width = self.ui.menuFrame.width()
        stat = False

        if width == 50 :
            newWidth = 150
            stat = False

        else :
            newWidth = 50
            stat = True


        self.animation = QtCore.QPropertyAnimation(self.ui.menuFrame,b"maximumWidth")
        self.animation.setDuration(450)
        self.animation.setStartValue(width)
        self.animation.setEndValue(newWidth)
        self.animation.setEasingCurve(Animation)
        self.animation.start()
        time.sleep(0.01)
        self.menuItems(stat)

    def menuItems(self,stat=False):
        if stat == False:
            self.ui.menuBtn.setMinimumSize(150,50)
            self.ui.menuBtn.setText("Menu")
            self.ui.homeBtn.setMinimumSize(150,50)
            self.ui.homeBtn.setText("Anasayfa")
            self.ui.notificationBtn.setMinimumSize(150,50)
            self.ui.notificationBtn.setText("Bildirimler")
            self.ui.authorizenLoginBtn.setMinimumSize(150,50)
            self.ui.authorizenLoginBtn.setText("Yetkili Girişi")
            self.ui.LogoutBtn.setMinimumSize(150,50)
            self.ui.LogoutBtn.setText("Çıkış Yap")
            self.ui.studentsOperationsBtn.setMinimumSize(150,50)
            self.ui.studentsOperationsBtn.setText("Öğrenci Işlemleri")
            self.ui.teacherOperationsBtn.setMinimumSize(150,50)
            self.ui.teacherOperationsBtn.setText("Öğretmen Işlemleri")
            self.ui.settingBtn.setMinimumSize(150,50)
            self.ui.settingBtn.setText("Ayarlar")
        else :
            self.ui.menuBtn.setMinimumSize(50,50)
            self.ui.menuBtn.setText("")
            self.ui.homeBtn.setMinimumSize(50,50)
            self.ui.homeBtn.setText("")
            self.ui.notificationBtn.setMinimumSize(50,50)
            self.ui.notificationBtn.setText("")
            self.ui.authorizenLoginBtn.setMinimumSize(50,50)
            self.ui.authorizenLoginBtn.setText("")
            self.ui.LogoutBtn.setMinimumSize(50,50)
            self.ui.LogoutBtn.setText("")
            self.ui.studentsOperationsBtn.setMinimumSize(50,50)
            self.ui.studentsOperationsBtn.setText("")
            self.ui.teacherOperationsBtn.setMinimumSize(50,50)
            self.ui.teacherOperationsBtn.setText("")
            self.ui.settingBtn.setMinimumSize(50,50)
            self.ui.settingBtn.setText("")

# Yapım Aşamasında 


    def notification(self):
        QtWidgets.QMessageBox.information(self,"Bildirim","Yapım Aşamasında.")
    def setting(self):
        QtWidgets.QMessageBox.information(self,"Bildirim","Yapım Aşamasında.")
    def teacherOperation(self):
        QtWidgets.QMessageBox.information(self,"Bildirim","Yapım Aşamasında.")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main = SchoolApp()
    main.show()
    app.exit(app.exec_())
    