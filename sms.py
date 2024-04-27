#https://www.youtube.com/watch?v=ohb-oknZQa8&list=PLUgFQtEcQLl_TmkNjA-UHg-PNABqTuXPb&index=56


#oğrenci tablosu
#öğretmen bilgi giriş ve tablosu
#üstte öğretmen bilgileri
#fakülte ve dersleri tablosu
#ogrencilere  bolum ekle
#bolum derslerine fakulte bilgisi ekle
#fakulte tablosu yerleşke bilgisi bölümler olsun
# ogrenci ogretmen fakulte bolum(dersler) 
#hepsinin detaylarına bak ve chate sor

import pyodbc
from tkinter import *
import time
import customtkinter
from PIL import ImageTk, Image
from tkinter import ttk, filedialog
from tkinter import messagebox
import pandas
import openpyxl

import global_deg

#global ogretmenin_mail
#ogretmenin_mail = ""

customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme("blue")

def clock():
    date =time.strftime("%d/%m/%Y")
    currentTime= time.strftime("%H:%M:%S")
    #print(date,currentTime)
    datetimeLabel.config(text=f'    Date: {date}\nTime: {currentTime}')
    datetimeLabel.after(1000,clock) #saniye artsın değişsin


count = 0
text=''
def slider():
    global text, count
    if count==len(s):
        text= ''
        count=0
    text = text+s[count]
    sliderLabel.config(text=text)
    count+=1
    sliderLabel.after(300,slider)

def dersTabloGuncelle():
    for child in dersATable.get_children():
        dersATable.delete(child)
    try:
        connection = pyodbc.connect('DRIVER={SQL SERVER};' +
                                    'Server=KORKMAZ\SQLEXPRESS;' +
                                    'Database=STUDENTMG_DB;' +
                                    'Trusted_Connection=True')
        cursor3 = connection.cursor()

        # Öğrenci sayısını hesaplamak için SQL sorgusu
        sql = "SELECT DERSID, DERSAD FROM DERS WHERE OGRETMENID = ?"
        cursor3.execute(sql, (global_deg.ogretmen_id,))

        for row in cursor3:
            ders_id, ders_adı = row
            dersA_tuple = (ders_id, ders_adı)

            # Ders bilgilerini dersTable'a ekle
            dersATable.insert("", END, value=dersA_tuple)

    except pyodbc.Error as ex:
        print("Failed! ", ex)




def dersEkle():
    def ekle():
        ders = nameEntry.get()
        try:
            connection = pyodbc.connect('DRIVER={SQL SERVER};' +
                                        'Server=KORKMAZ\SQLEXPRESS;' +
                                        'Database=STUDENTMG_DB;' +
                                        'Trusted_Connection=True')
            cursor = connection.cursor()

            # Öğretmenin yeni ders eklemesi için SQL SELECT komutu ile dersin var olup olmadığını kontrol et
            cursor.execute("SELECT DERSAD FROM DERS WHERE DERSAD = ? AND OGRETMENID = ?", (ders, global_deg.ogretmen_id))
            existing_ders = cursor.fetchone()

            if existing_ders:
                messagebox.showerror("Hata", "Bu ders zaten mevcut!")
            else:
                # Öğretmenin yeni ders eklemesi için SQL INSERT INTO komutu
                sql = "INSERT INTO DERS (DERSAD, OGRETMENID) VALUES (?, ?)"
                cursor.execute(sql, (ders, global_deg.ogretmen_id))

                connection.commit()  # Değişiklikleri kaydet
                dersTabloGuncelle()

        except pyodbc.Error as ex:
            print("Failed! ", ex)
        finally:
            if connection:
                connection.close()

    connectWindow = Toplevel()
    connectWindow.geometry('300x250+730+230')
    connectWindow.title("Ders Ekleme Ekranı")
    connectWindow.resizable(0, 0)

    nameLabel = Label(connectWindow, text="Ders İsmi ", font=("arial", 15))
    nameLabel.place(relx=0.1, rely=0.25)
    nameEntry = Entry(connectWindow, bd=1)
    nameEntry.place(relx=0.5, rely=0.25)

    connectButton = customtkinter.CTkButton(connectWindow, text="Dersi Ekle", fg_color="green", command=ekle)
    connectButton.place(relx=0.25, rely=0.5)


def dersEklee():

    def ekle():
        ders = nameEntry.get()
        try:
            connection = pyodbc.connect('DRIVER={SQL SERVER};' +
                                        'Server=KORKMAZ\SQLEXPRESS;' +
                                        'Database=STUDENTMG_DB;' +
                                        'Trusted_Connection=True')
            cursor = connection.cursor()

            # Öğretmenin yeni ders eklemesi için SQL INSERT INTO komutu
            sql = "INSERT INTO DERS (DERSAD, OGRETMENID) VALUES (?, ?)"
            cursor.execute(sql, (ders, global_deg.ogretmen_id))

            connection.commit()  # Değişiklikleri kaydet
            dersTabloGuncelle()
        except pyodbc.Error as ex:
            print("Failed! ", ex)

    connectWindow=Toplevel()
    connectWindow.geometry('300x250+730+230')
    connectWindow.title("Ders Ekleme Ekranı")
    connectWindow.resizable(0,0)

    nameLabel= Label(connectWindow, text="Ders İsmi ", font=("arial",15))
    nameLabel.place(relx=0.1, rely=0.25)
    nameEntry = Entry(connectWindow,bd=1)
    nameEntry.place(relx=0.5,rely=0.25)

    connectButton =customtkinter.CTkButton(connectWindow, text="Dersi Ekle", fg_color="green", command=ekle)
    connectButton.place(relx=0.25,rely=0.5)




def dersTablosu_yenile():
    for child in dersTable.get_children():
        dersTable.delete(child)
    try:
        connection = pyodbc.connect('DRIVER={SQL SERVER};' +
                                    'Server=KORKMAZ\SQLEXPRESS;' +
                                    'Database=STUDENTMG_DB;' +
                                    'Trusted_Connection=True')
        cursor2 = connection.cursor()

        # Öğrenci sayısını hesaplamak için SQL sorgusu
        sql = """
        SELECT D.DERSID,D.DERSAD, COUNT(N.OGRENCIID) AS 'Öğrenci Sayısı'
        FROM DERS D
        JOIN NOTLAR N ON D.DERSID = N.DERSID
        WHERE D.OGRETMENID = ?
        GROUP BY D.DERSID,D.DERSAD;
        """
        cursor2.execute(sql, (global_deg.ogretmen_id,))

        for row in cursor2:
            ders_id, ders_adı, öğrenci_sayısı = row
            ders_tuple = (ders_id, ders_adı, öğrenci_sayısı)

            # Ders bilgilerini dersTable'a ekle
            dersTable.insert("", END, value=ders_tuple)

    except pyodbc.Error as ex:
        print("Failed! ", ex)


def add_student():
    addStudentWindow = Toplevel()
    addStudentWindow.geometry('470x350+730+230')
    addStudentWindow.title("Öğrenci Ekleme Ekranı")
    addStudentWindow.resizable(0, 0)

    s_idLabel = Label(addStudentWindow, text="Öğrenci Id", font=("arial", 15))
    s_idLabel.place(relx=0.2, rely=0.1)
    s_idEntry = Entry(addStudentWindow, bd=1)
    s_idEntry.place(relx=0.47, rely=0.1)

    semailLabel = Label(addStudentWindow, text="Öğrenci Mail", font=("arial", 15))
    semailLabel.place(relx=0.2, rely=0.22)
    semailEntry = Entry(addStudentWindow, bd=1)
    semailEntry.place(relx=0.47, rely=0.22)

    sdersLabel = Label(addStudentWindow, text="Ders", font=("arial", 15))
    sdersLabel.place(relx=0.2, rely=0.34)
    sdersEntry = Entry(addStudentWindow, bd=1)
    sdersEntry.place(relx=0.47, rely=0.34)

    snotLabel = Label(addStudentWindow, text="Not", font=("arial", 15))
    snotLabel.place(relx=0.2, rely=0.46)
    snotEntry = Entry(addStudentWindow, bd=1)
    snotEntry.place(relx=0.47, rely=0.46)



    def addStudentData():

        id = s_idEntry.get()
        email = semailEntry.get()
        ders = sdersEntry.get()
        snot = snotEntry.get()
        print("üstteki ders :", sdersEntry.get())
        print("id: ", id)

        try:
            print("dersimiz :", ders)
            connection = pyodbc.connect('DRIVER={SQL SERVER};' +
                                        'Server=KORKMAZ\SQLEXPRESS;' +
                                        'Database=STUDENTMG_DB;' +
                                        'Trusted_Connection=True')

            # SQL sorgusu oluştur ve çalıştır
            cursor = connection.cursor()
            cursor.execute("SELECT DERSID FROM DERS WHERE DERSAD = (?)", (ders,))
            print(cursor)
            # Sonucu al
            ders_id = cursor.fetchone()
            print("VURADAAAAA  ", ders_id)
            connection.close()

            # Ders ID'sini yazdır
            print("dersinin ID'si:", ders_id[0])
            ders_id = ders_id[0]
            xmail = global_deg.ogretmenin_maili


            """
            connection = pyodbc.connect('DRIVER={SQL SERVER};' +
                                        'Server=KORKMAZ\SQLEXPRESS;' +
                                        'Database=STUDENTMG_DB;' +
                                        'Trusted_Connection=True')

            cursor = connection.cursor()

            # Yeni kaydı ekle
            # cursor.execute("INSERT INTO NOTLAR (OGRENCIID, DERSID, NOTDEGERI) VALUES (?, (SELECT DERSID FROM DERS WHERE DERSAD = ? AND OGRETMENID = ?), ?)",(id, ders, snot,global_deg.ogretmen_id))
            sql = "INSERT INTO NOTLAR (OGRENCIID, DERSID, NOTDEGERI) " \
                  "VALUES (?, (SELECT DERSID FROM DERS WHERE DERSAD = ? AND OGRETMENID = ?), ?)"

            # Sorguyu çalıştırırken demet içinde değerleri gönderme
            cursor.execute(sql, (id, ders, global_deg.ogretmen_id, snot))
            # Değişiklikleri kaydet
            connection.commit()

            # Bağlantıyı kapat
            connection.close()
"""

            try:
                connection = pyodbc.connect('DRIVER={SQL SERVER};' +
                                            'Server=KORKMAZ\SQLEXPRESS;' +
                                            'Database=STUDENTMG_DB;' +
                                            'Trusted_Connection=True')
                cursor = connection.cursor()

                # Var olan kaydı kontrol et
                cursor.execute("SELECT COUNT(*) FROM NOTLAR WHERE OGRENCIID = ? AND DERSID = ?", (id, ders_id))
                count = cursor.fetchone()[0]
                print("Count : ",count)
                if count == 0:
                    # Yeni kaydı ekle
                    sql = "INSERT INTO NOTLAR (OGRENCIID, DERSID, NOTDEGERI) " \
                          "VALUES (?, (SELECT DERSID FROM DERS WHERE DERSAD = ? AND OGRETMENID = ?), ?)"
                    cursor.execute(sql, (id, ders, global_deg.ogretmen_id, snot))

                    connection.commit()  # Değişiklikleri kaydet

                    messagebox.showinfo("Başarılı", "Notlar tablosuna yeni kayıt eklendi.")
                else:
                    messagebox.showinfo("Uyarı", "Bu öğrenciye ait bu ders zaten kayıtlı.")

                # Bağlantıyı kapat
                connection.close()

            except pyodbc.Error as ex:
                print("Failed! ", ex)

            for child in studentTable.get_children():
                studentTable.delete(child)


            dersTablosu_yenile()
            my_student()
            all_student()
            connection.close()
        except pyodbc.Error as ex:
            print("Failed! ", ex)


    addButton = customtkinter.CTkButton(addStudentWindow, text="Öğrenciyi ekle", fg_color="green", command= addStudentData)
    addButton.place(relx=0.25, rely=0.6)

def searchStudent():
    searchStudentWindow = Toplevel()
    searchStudentWindow.geometry('500x350+730+230')
    searchStudentWindow.title("Öğrenci Arama Ekranı")
    searchStudentWindow.resizable(0, 0)

    s_idLabel = Label(searchStudentWindow, text="Öğrenci Id", font=("arial", 15))
    s_idLabel.place(relx=0.2, rely=0.1)
    s_idEntry = Entry(searchStudentWindow, bd=1)
    s_idEntry.place(relx=0.47, rely=0.1)

    snameLabel = Label(searchStudentWindow, text="İsim", font=("arial", 15))
    snameLabel.place(relx=0.2, rely=0.22)
    snameEntry = Entry(searchStudentWindow, bd=1)
    snameEntry.place(relx=0.47, rely=0.22)

    slnameLabel = Label(searchStudentWindow, text="Soyisim", font=("arial", 15))
    slnameLabel.place(relx=0.2, rely=0.34)
    slnameEntry = Entry(searchStudentWindow, bd=1)
    slnameEntry.place(relx=0.47, rely=0.34)

    semailLabel = Label(searchStudentWindow, text="Öğrenci Mail", font=("arial", 15))
    semailLabel.place(relx=0.2, rely=0.46)
    semailEntry = Entry(searchStudentWindow, bd=1)
    semailEntry.place(relx=0.47, rely=0.46)

    sdersLabel = Label(searchStudentWindow, text="Ders", font=("arial", 15))
    sdersLabel.place(relx=0.2, rely=0.58)
    sdersEntry = Entry(searchStudentWindow, bd=1)
    sdersEntry.place(relx=0.47, rely=0.58)

    snotLabel = Label(searchStudentWindow, text="Not", font=("arial", 15))
    snotLabel.place(relx=0.2, rely=0.7)
    snotEntry = Entry(searchStudentWindow, bd=1)
    snotEntry.place(relx=0.47, rely=0.7)

    def searchStudentData():
        id = s_idEntry.get()
        name= snameEntry.get()
        lname = slnameEntry.get()
        email = semailEntry.get()
        ders = sdersEntry.get()
        snot = snotEntry.get()

        try:
            connection = pyodbc.connect('DRIVER={SQL SERVER};' +
                                        'Server=KORKMAZ\SQLEXPRESS;' +
                                        'Database=STUDENTMG_DB;' +
                                        'Trusted_Connection=True')

            # SQL sorgusu oluştur ve çalıştır
            cursor = connection.cursor()

            """
            SELECT O.OGRENCIID AS 'Öğrenci ID',
                                     O.AD AS 'Öğrenci Adı',
                                     O.SOYAD AS 'Öğrenci Soyadı',
                                     O.EMAIL AS 'Öğrenci Email',
                                     D.DERSAD AS 'Ders Adı',
                                     N.NOTDEGERI AS 'Not'
                             FROM OGRENCI O
                             JOIN DERS D ON O.OGRETMENID = D.OGRETMENID
                             JOIN NOTLAR N ON O.OGRENCIID = N.OGRENCIID AND D.DERSID = N.DERSID
                             WHERE O.OGRENCIID = ? OR O.AD = ? OR O.SOYAD = ? OR O.EMAIL = ? OR D.DERSAD = ? OR N.NOTDEGERI = ?
            """

            """SELECT O.OGRENCIID AS 'Öğrenci ID',
                   O.AD AS 'Öğrenci Adı',
                   O.SOYAD AS 'Öğrenci Soyadı',
                   O.EMAIL AS 'Öğrenci Email',
                   D.DERSAD AS 'Ders Adı',
                   N.NOTDEGERI AS 'Not'
            FROM OGRENCI O
            JOIN DERS D ON O.OGRETMENID = D.OGRETMENID
            JOIN NOTLAR N ON O.OGRENCIID = N.OGRENCIID OR D.DERSID = N.DERSID
            WHERE O.OGRENCIID = ? OR O.AD = ? OR O.SOYAD = ? OR O.EMAIL = ? OR D.DERSAD = ? OR N.NOTDEGERI = ?
            """

            """
                            SELECT O.OGRENCIID AS 'Öğrenci ID',
                            O.AD AS 'Öğrenci Adı',
                            O.SOYAD AS 'Öğrenci Soyadı',
                            O.EMAIL AS 'Öğrenci Email',
                            D.DERSAD AS 'Ders Adı',
                            N.NOTDEGERI AS 'Not'
                            FROM OGRENCI O
                    JOIN DERS D ON O.OGRETMENID = D.OGRETMENID
                    JOIN NOTLAR N ON O.OGRENCIID = N.OGRENCIID AND D.DERSID = N.DERSID
                    WHERE D.DERSAD = ?
                            """
            sql ="""
                SELECT O.OGRENCIID, O.AD, O.SOYAD, O.EMAIL, D.DERSAD, N.NOTDEGERI
                 FROM OGRENCI O
                 JOIN NOTLAR N ON O.OGRENCIID = N.OGRENCIID
                 JOIN DERS D ON N.DERSID = D.DERSID
                 WHERE (D.DERSAD = ? OR N.NOTDEGERI=? OR O.OGRENCIID=? OR O.AD=? OR O.SOYAD=? )
                 """


            cursor.execute(sql, (ders,snot,id,name,lname))#(id, name, lname, email, ders, snot))

            rows = cursor.fetchall()
            print(rows)
            # Tabloyu temizle
            studentTable.delete(*studentTable.get_children())

            # Sonuçları tabloya ekle
            for data in rows:
                my_tuple = ()
                for i in range(0, len(data)):
                    deger = data[i]
                    my_tuple = my_tuple + (deger,)

                studentTable.insert("", END, value=my_tuple)


            connection.close()


        except pyodbc.Error as ex:
            print("Failed! ", ex)



    searchButton = customtkinter.CTkButton(searchStudentWindow, text="Ara", fg_color="green",
                                        command=searchStudentData)
    searchButton.place(relx=0.25, rely=0.8)



def deleteStudent():
    print(studentTable.item(studentTable.selection())['values'])

    idSelected = studentTable.item(studentTable.selection())['values'][0]
    dersSelected = studentTable.item(studentTable.selection())['values'][4]
    nameSelected = studentTable.item(studentTable.selection())['values'][1]
    lnameSelected = studentTable.item(studentTable.selection())['values'][2]

    connection = pyodbc.connect('DRIVER={SQL SERVER};' +
                                'Server=KORKMAZ\SQLEXPRESS;' +
                                'Database=STUDENTMG_DB;' +
                                'Trusted_Connection=True')

    sql = "SELECT DERSID FROM DERS WHERE DERSAD = ?"
    cursor = connection.cursor()
    cursor.execute(sql, (dersSelected,))

    # Sonucu al
    ders_id = cursor.fetchone()
    ders_id = ders_id[0]
    # Ders ID'sini yazdır
    #print("Seçilen dersinin ID'si:", ders_id[0])
    #print(type(ders_id[0]))
    print(idSelected)

    # Bağlantıyı kapat
    connection.close()

    connection = pyodbc.connect('DRIVER={SQL SERVER};' +
                                'Server=KORKMAZ\SQLEXPRESS;' +
                                'Database=STUDENTMG_DB;' +
                                'Trusted_Connection=True')

    cursor = connection.cursor()
    #sql = "SELECT NOTLARID FROM NOTLAR WHERE OGRENCIID = ? AND DERSID = ?;"
    #cursor.execute(sql, (idSelected,ders_id))

    # Sonucu al
    #not_id = cursor.fetchone()

    # Ders ID'sini yazdır
    #print("Seçilen kişinin notlar ID'si:", not_id[0])

    sql = "DELETE FROM NOTLAR WHERE OGRENCIID = ? AND DERSID = ?"
    #delete = cursor.execute(sql, (idSelected, ders_id))
    cursor.execute("DELETE FROM NOTLAR WHERE OGRENCIID = {} AND DERSID = {}".format(idSelected, ders_id))
    #print(delete)
    connection.commit()
    studentTable.delete(studentTable.selection())
    messagebox.showinfo("Silme Başarılı",f"{nameSelected} {lnameSelected} isimli öğrencinin {dersSelected} dersi ve  notu silindi")
    dersTablosu_yenile()
    connection.close()



def updateStudent():
    updateWindow = Toplevel()
    updateWindow.geometry('300x250+730+230')
    updateWindow.title("Not Güncelleme Ekranı")
    updateWindow.resizable(0, 0)

    notLabel = Label(updateWindow, text="Yeni Not", font=("arial", 13))
    notLabel.place(relx=0.2, rely=0.2)
    notEntry = Entry(updateWindow, bd=1)
    notEntry.place(relx=0.5, rely=0.2)
    """
    def updateData():

        yeniNot = notEntry.get()
        print(studentTable.item(studentTable.selection())['values'])

        idSelected = studentTable.item(studentTable.selection())['values'][0]
        dersSelected = studentTable.item(studentTable.selection())['values'][4]
        nameSelected = studentTable.item(studentTable.selection())['values'][1]
        lnameSelected = studentTable.item(studentTable.selection())['values'][2]

        connection = pyodbc.connect('DRIVER={SQL SERVER};' +
                                    'Server=KORKMAZ\SQLEXPRESS;' +
                                    'Database=STUDENTMG_DB;' +
                                    'Trusted_Connection=True')

        sql = "SELECT DERSID FROM DERS WHERE DERSAD = ?"
        cursor = connection.cursor()
        cursor.execute(sql, (dersSelected,))

        # Sonucu al
        ders_id = cursor.fetchone()
        ders_id = ders_id[0]

        print(idSelected)
        connection.close()

        connection = pyodbc.connect('DRIVER={SQL SERVER};' +
                                    'Server=KORKMAZ\SQLEXPRESS;' +
                                    'Database=STUDENTMG_DB;' +
                                    'Trusted_Connection=True')

        cursor = connection.cursor()

        sql = "UPDATE NOTLAR SET NOTDEGERI = ? WHERE OGRENCIID = ? AND DERSID = ?;"
        cursor.execute(sql, (yeniNot, idSelected, ders_id))


        connection.commit()
        studentTable.delete(studentTable.selection())
        messagebox.showinfo("Not Güncelleme Başarılı",
                            f"{nameSelected} {lnameSelected} isimli öğrencinin {dersSelected} dersinin notu {yeniNot} olarak güncellendi")
        """
    """
    def updateData():
        yeniNot = notEntry.get()
        print(studentTable.item(studentTable.selection())['values'])

        idSelected = studentTable.item(studentTable.selection())['values'][0]
        dersSelected = studentTable.item(studentTable.selection())['values'][4]
        nameSelected = studentTable.item(studentTable.selection())['values'][1]
        lnameSelected = studentTable.item(studentTable.selection())['values'][2]

        connection = pyodbc.connect('DRIVER={SQL SERVER};' +
                                    'Server=KORKMAZ\SQLEXPRESS;' +
                                    'Database=STUDENTMG_DB;' +
                                    'Trusted_Connection=True')

        cursor = connection.cursor()

        # Öğretmenin verdiği dersleri sorgula
        sql_dersler = "SELECT DERSID FROM DERS WHERE DERSAD = ? AND OGRETMENID = ?"
        cursor.execute(sql_dersler, (dersSelected, global_deg.ogretmen_id))
        ders_row = cursor.fetchone()

        if ders_row:
            ders_id = ders_row[0]

            # Öğrenci ve dersin notunu güncelle
            sql_update = "UPDATE NOTLAR SET NOTDEGERI = ? WHERE OGRENCIID = ? AND DERSID = ?;"
            cursor.execute(sql_update, (yeniNot, idSelected, ders_id))
            connection.commit()
            
            # Başarılı mesajı göster
            messagebox.showinfo("Not Güncelleme Başarılı",
                                f"{nameSelected} {lnameSelected} isimli öğrencinin {dersSelected} dersinin notu {yeniNot} olarak güncellendi")
        else:
            # Öğretmenin vermediği bir ders için uyarı ver
            messagebox.showwarning("Uyarı", f"{global_deg.ogretmen_id} ID'li öğretmen bu dersi vermiyor.")

        connection.close()
        # Güncelleme işlemi tamamlandığında satırı tablodan sil
        studentTable.delete(studentTable.selection())
    """

    def updateData():
        yeniNot = notEntry.get()
        print(studentTable.item(studentTable.selection())['values'])

        idSelected = studentTable.item(studentTable.selection())['values'][0]
        dersSelected = studentTable.item(studentTable.selection())['values'][4]
        nameSelected = studentTable.item(studentTable.selection())['values'][1]
        lnameSelected = studentTable.item(studentTable.selection())['values'][2]

        connection = pyodbc.connect('DRIVER={SQL SERVER};' +
                                    'Server=KORKMAZ\SQLEXPRESS;' +
                                    'Database=STUDENTMG_DB;' +
                                    'Trusted_Connection=True')

        cursor = connection.cursor()

        # Öğretmenin verdiği dersleri sorgula
        sql_dersler = "SELECT DERSID FROM DERS WHERE DERSAD = ? AND OGRETMENID = ?"
        cursor.execute(sql_dersler, (dersSelected, global_deg.ogretmen_id))
        ders_row = cursor.fetchone()

        if ders_row:
            ders_id = ders_row[0]

            # Öğrenci ve dersin notunu güncelle
            # Öğrencinin bu dersi alıp almadığını kontrol et
            sql_ogrenci_ders = "SELECT COUNT(*) FROM NOTLAR WHERE OGRENCIID = ? AND DERSID = ?"
            cursor.execute(sql_ogrenci_ders, (idSelected, ders_id))
            ogrenci_ders_count = cursor.fetchone()[0]

            if ogrenci_ders_count > 0:
                # Öğrenci bu dersi almış, notu güncelle
                sql_update = "UPDATE NOTLAR SET NOTDEGERI = ? WHERE OGRENCIID = ? AND DERSID = ?;"
                cursor.execute(sql_update, (yeniNot, idSelected, ders_id))
                connection.commit()

                # Başarılı mesajı göster
                messagebox.showinfo("Not Güncelleme Başarılı",
                                    f"{nameSelected} {lnameSelected} isimli öğrencinin {dersSelected} dersinin notu {yeniNot} olarak güncellendi")
            else:
                # Öğrenci bu dersi almıyor, hata mesajı göster
                messagebox.showerror("Hata",
                                     f"{nameSelected} {lnameSelected} isimli öğrenci {dersSelected} dersini almıyor.")
        else:
            # Öğretmenin vermediği bir ders için uyarı ver
            messagebox.showwarning("Uyarı", f"{global_deg.ogretmen_id} ID'li öğretmen {dersSelected} dersini vermiyor.")

        connection.close()
        # Güncelleme işlemi tamamlandığında satırı tablodan sil
        studentTable.delete(studentTable.selection())

        connection.close()

        #tekrar tablei göstersin
        my_student()
        all_student()

    updateButton = customtkinter.CTkButton(updateWindow, text="Güncelle", fg_color="green",
                                           command=updateData)
    updateButton.place(relx=0.25, rely=0.5)


def all_student():
    for child in studentTable.get_children():
        studentTable.delete(child)
    try:
        connection = pyodbc.connect('DRIVER={SQL SERVER};' +
                                    'Server=KORKMAZ\SQLEXPRESS;' +
                                    'Database=STUDENTMG_DB;' +
                                    'Trusted_Connection=True')
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                O.OGRENCIID AS 'Öğrenci ID',
                O.AD AS 'Öğrenci Adı',
                O.SOYAD AS 'Öğrenci Soyadı',
                O.EMAIL AS 'Öğrenci Email',
                D.DERSAD AS 'Ders Adı',
                N.NOTDEGERI AS 'Not Değeri'
            FROM
                OGRENCI O
            LEFT JOIN
                NOTLAR N ON O.OGRENCIID = N.OGRENCIID
            LEFT JOIN
                DERS D ON N.DERSID = D.DERSID;
        """)

        #cursor.execute("""
        #SELECT   O.OGRENCIID AS 'Öğrenci ID', O.AD AS 'Öğrenci Adı', O.SOYAD AS 'Öğrenci Soyadı', O.EMAIL AS 'Öğrenci Email',
        #D.DERSAD AS 'Ders Adı', N.NOTDEGERI AS 'Not Değeri'
        #FROM NOTLAR N
        #JOIN OGRENCI O ON N.OGRENCIID = O.OGRENCIID
        #JOIN DERS D ON N.DERSID = D.DERSID;""")

        for data in cursor:
            my_tuple = ()
            for i in range(0, len(data)):
                deger = data[i]
                my_tuple = my_tuple + (deger,)

            studentTable.insert("", END, value=my_tuple)

    except pyodbc.Error as ex:
        print("Failed! ", ex)


def my_student():
    for child in studentTable.get_children():
        studentTable.delete(child)
    try:
        xmail = global_deg.ogretmenin_maili
        print("xmail = ", xmail)
        connection = pyodbc.connect('DRIVER={SQL SERVER};' +
                                    'Server=KORKMAZ\SQLEXPRESS;' +
                                    'Database=STUDENTMG_DB;' +
                                    'Trusted_Connection=True')
        cursor = connection.cursor()
        cursor.execute("""
        SELECT  O.OGRENCIID AS 'Öğrenci ID' ,O.AD AS 'Öğrenci Adı', O.SOYAD AS 'Öğrenci Soyadı', O.EMAIL AS 'Öğrenci Email',
        D.DERSAD AS 'Ders Adı', N.NOTDEGERI AS 'Not Değeri'
        FROM NOTLAR N
        JOIN OGRENCI O ON N.OGRENCIID = O.OGRENCIID
        JOIN DERS D ON N.DERSID = D.DERSID
        JOIN OGRETMEN T ON D.OGRETMENID = T.OGRETMENID
        WHERE T.EMAIL = (?)""",xmail)
        """
        cursor.execute("SELECT
                O.OGRENCIID AS 'Öğrenci ID',
                O.AD AS 'Öğrenci Adı',
                O.SOYAD AS 'Öğrenci Soyadı',
                O.EMAIL AS 'Öğrenci Email',
                D.DERSAD AS 'Ders Adı',
                N.NOTDEGERI AS 'Not'
            FROM OGRENCI O
            JOIN DERS D ON O.OGRETMENID = D.OGRETMENID
            JOIN NOTLAR N ON O.OGRENCIID = N.OGRENCIID AND D.DERSID = N.DERSID
            JOIN OGRETMEN T ON O.OGRETMENID = T.OGRETMENID
            WHERE T.EMAIL = (?)", xmail)
        """

        for data in cursor:
            my_tuple = ()
            for i in range(0, len(data)):
                deger = data[i]
                my_tuple = my_tuple + (deger,)

            studentTable.insert("", END, value=my_tuple)

    except pyodbc.Error as ex:
        print("Failed! ", ex)


def exportData():
    url = filedialog.asksaveasfilename(defaultextension='.xlsx')
    indexing = studentTable.get_children()
    print(indexing) # satır indexleri alır kendince
    newlist = []
    for index in indexing:
        content = studentTable.item(index)
        dataList = content['values']
        #print(dataList)  # satırları alt alta liste olarak yazar
        newlist.append(dataList)
    #print(newlist) # yanyana hepsini liste

    table = pandas.DataFrame(newlist,columns=['Id','Ad','Soyad','Email','Ders','Not'])
    table.to_excel(url,index=False)
    print(table)
    messagebox.showinfo('Başarılı','Tablo datası oluşturuldu.')

root=customtkinter.CTk() #Tk()

root.geometry("1380x700+100+50")
root.resizable(0,0)
root.title("Öğrenci Bilgi Sistemi")

datetimeLabel= Label(root,font=('arial',15,'bold'), fg="green")
datetimeLabel.place(x=50,y=10)

clock()

s='Student Management System' #s[count] = S count is 0
sliderLabel = Label(root,text=s,font=('arial',20,'italic bold'),width=40, fg="green") #width ile olduğu yerde kayıyomus gibi
sliderLabel.place(relx=0.25,y=10)
slider()

#connectButton= customtkinter.CTkButton(root, text="Veritabanına Bağlan", fg_color="green", command=connect_database)
#connectButton.place(relx=0.8,y=10)


#left Frame

leftFrame = Frame(root)
leftFrame.place(x=50, y=90, width=300, height=720)

image = Image.open("photo/group.png")#resmi yükle
image=image.resize((150,150))
backgroundImage= ImageTk.PhotoImage(image)
bgLabel =Label(leftFrame,image=backgroundImage)
bgLabel.pack(pady=20, padx=20)

allStudentButton= customtkinter.CTkButton(leftFrame,text="Tüm Öğrencileri Gör", hover_color="gray", command=all_student)
allStudentButton.pack(pady=10, padx=20)

myStudentButton= customtkinter.CTkButton(leftFrame,text="Kendi Öğrencilerim", hover_color="gray", command=my_student)
myStudentButton.pack(pady=10, padx=20)

addStudentButton= customtkinter.CTkButton(leftFrame,text="Öğrenci Ekle", hover_color="gray", command = lambda: add_student())
addStudentButton.pack(pady=10, padx=20)

searchStudentButton= customtkinter.CTkButton(leftFrame,text="Öğrenci Ara", hover_color="gray",command=lambda :searchStudent())
searchStudentButton.pack(pady=10, padx=20)

delStudentButton= customtkinter.CTkButton(leftFrame,text="Öğrenci Sil", hover_color="gray", command=lambda : deleteStudent())
delStudentButton.pack(pady=10, padx=20)

updateStudentButton= customtkinter.CTkButton(leftFrame,text="Öğrenci Güncelle", hover_color="gray", command=lambda :updateStudent())
updateStudentButton.pack(pady=10, padx=20)

exportStudentButton= customtkinter.CTkButton(leftFrame,text="Öğrenci Export", hover_color="gray", command= lambda :exportData())
exportStudentButton.pack(pady=10, padx=20)

exitStudentButton= customtkinter.CTkButton(leftFrame,text="Çıkış", hover_color="gray", command=quit)
exitStudentButton.pack(pady=10, padx=20)


#orta Frame

rightFrame = Frame(root,bg="red")
rightFrame.place(x=410, y= 100, width=900, height =650)

scrollBarX= Scrollbar(rightFrame,orient=HORIZONTAL)
scrollBarY= Scrollbar(rightFrame,orient=VERTICAL)


studentTable=ttk.Treeview(rightFrame,columns=("Id","Ad","Soyad","Email","Ders","Not"),
                               xscrollcommand=scrollBarX.set, yscrollcommand=scrollBarY.set)

#"Id","Isim","Telefon","Email","Adres","Cinsiyet","D.O.B","Kayıt Tarihi","Kayıt Saati")
scrollBarX.config(command=studentTable.xview)
scrollBarY.config(command=studentTable.yview)

scrollBarX.pack(side= BOTTOM, fill=X)
scrollBarY.pack(side=RIGHT,fill=Y)

studentTable.pack(fill=BOTH,expand=1)

studentTable.heading("Id", text="Id")
studentTable.heading("Ad", text="Ad")
studentTable.heading("Soyad", text="Soyad")
#studentTable.heading("Telefon", text="Telefon")
studentTable.heading("Email", text="Email")
studentTable.heading("Ders", text="Ders")
studentTable.heading("Not", text="Not")
#studentTable.heading("Adres", text="Adres")
#studentTable.heading("Cinsiyet", text="Cinsiyet")
#studentTable.heading("D.O.B", text="D.O.B")
#studentTable.heading("Kayıt Tarihi", text="Kayıt Tarihi")
#studentTable.heading("Kayıt Saati", text="Kayıt Saati")

studentTable.column("Id",width=100,anchor=CENTER)
studentTable.column("Ad",width=180,anchor=CENTER)
studentTable.column("Soyad", width=180,anchor=CENTER)
studentTable.column("Email", width=180,anchor=CENTER)
studentTable.column("Ders", width=180,anchor=CENTER)
studentTable.column("Not", width=150,anchor=CENTER)

studentTable.config(show="headings")

style = ttk.Style()
style.configure('Treeview',rowheight=40, font=('arial',12))


#isim frame
x=f"Merhaba {global_deg.ogretmen_name} {global_deg.ogretmen_lname}" #s[count] = S count is 0
sliderLabel2 = Label(root,text=x,font=('arial',19,'bold'), fg="green") #width ile olduğu yerde kayıyomus gibi
sliderLabel2.place(relx=0.8,y=15)



#end ust frame

endTopFrame = Frame(root)
endTopFrame.place(x=1370, y= 100, width=330, height =300)



scrollBar2X= Scrollbar(endTopFrame,orient=HORIZONTAL)
scrollBar2Y= Scrollbar(endTopFrame,orient=VERTICAL)

dersTable=ttk.Treeview(endTopFrame,columns=("Id","Ders","Kişi Sayısı"),
                               xscrollcommand=scrollBar2X.set, yscrollcommand=scrollBar2Y.set)

scrollBar2X.config(command=dersTable.xview)
scrollBar2Y.config(command=dersTable.yview)

scrollBar2X.pack(side= BOTTOM, fill=X)
scrollBar2Y.pack(side=RIGHT,fill=Y)

dersTable.pack(fill=BOTH,expand=1)

dersTable.heading("Id", text="Id")
dersTable.heading("Ders", text="Ders")
dersTable.heading("Kişi Sayısı", text="Kişi Sayısı")

dersTable.column("Id",width=100,anchor=CENTER)
dersTable.column("Ders", width=180,anchor=CENTER)
dersTable.column("Kişi Sayısı", width=150,anchor=CENTER)

dersTable.config(show="headings")

style = ttk.Style()
style.configure('Treeview',rowheight=40, font=('arial',12))



yeniDersButton= customtkinter.CTkButton(root, text="Yeni Ders Verin", fg_color="green",width=90, command=dersEkle)
yeniDersButton.place(x=1100,y=610)
#silDersButton= customtkinter.CTkButton(root, text="Ders Silin", fg_color="green", width=90, command=dersEkle)
#silDersButton.place(x=1220,y=610)



#end alt frame
endBottomFrame = Frame(root)
endBottomFrame.place(x=1370, y= 450, width=300, height =300)



scrollBar3X= Scrollbar(endBottomFrame,orient=HORIZONTAL)
scrollBar3Y= Scrollbar(endBottomFrame,orient=VERTICAL)

dersATable=ttk.Treeview(endBottomFrame,columns=("Id","Ders"),
                               xscrollcommand=scrollBar3X.set, yscrollcommand=scrollBar3Y.set)

scrollBar3X.config(command=dersATable.xview)
scrollBar3Y.config(command=dersATable.yview)

scrollBar3X.pack(side= BOTTOM, fill=X)
scrollBar3Y.pack(side=RIGHT,fill=Y)

dersATable.pack(fill=BOTH,expand=1)

dersATable.heading("Id", text="Id")
dersATable.heading("Ders", text="Ders")

dersATable.column("Id",width=100,anchor=CENTER)
dersATable.column("Ders", width=180,anchor=CENTER)

dersATable.config(show="headings")

style = ttk.Style()
style.configure('Treeview',rowheight=40, font=('arial',12))


#Display data in treeview object

try:
    xmail  = global_deg.ogretmenin_maili
    print("xmail = ",xmail)
    connection= pyodbc.connect('DRIVER={SQL SERVER};'+
                                    'Server=KORKMAZ\SQLEXPRESS;'+
                                    'Database=STUDENTMG_DB;'+
                                    'Trusted_Connection=True')
    cursor = connection.cursor()

    #cursor.execute("SELECT * FROM OGRENCI JOIN OGRETMEN ON OGRETMEN.OGRETMENID = OGRENCI.OGRETMENID WHERE OGRETMEN.EMAIL = (?)",xmail)
    #cursor.execute("SELECT O.OGRENCIID AS 'Öğrenci ID', O.AD AS 'Öğrenci Adı', O.SOYAD AS 'Öğrenci Soyadı', O.EMAIL AS 'Öğrenci Email' FROM OGRENCI O JOIN OGRETMEN T ON O.OGRETMENID = T.OGRETMENID WHERE T.EMAIL = (?)",xmail)

    cursor.execute("""
            SELECT  O.OGRENCIID AS 'Öğrenci ID' ,O.AD AS 'Öğrenci Adı', O.SOYAD AS 'Öğrenci Soyadı', O.EMAIL AS 'Öğrenci Email',
           D.DERSAD AS 'Ders Adı', N.NOTDEGERI AS 'Not Değeri'
    FROM NOTLAR N
    JOIN OGRENCI O ON N.OGRENCIID = O.OGRENCIID
    JOIN DERS D ON N.DERSID = D.DERSID
    JOIN OGRETMEN T ON D.OGRETMENID = T.OGRETMENID
    WHERE T.EMAIL = (?)
            """, xmail)
    """
    cursor.execute("SELECT
            O.OGRENCIID AS 'Öğrenci ID',
            O.AD AS 'Öğrenci Adı',
            O.SOYAD AS 'Öğrenci Soyadı',
            O.EMAIL AS 'Öğrenci Email',
            D.DERSAD AS 'Ders Adı',
            N.NOTDEGERI AS 'Not'
        FROM OGRENCI O
        JOIN DERS D ON O.OGRETMENID = D.OGRETMENID
        JOIN NOTLAR N ON O.OGRENCIID = N.OGRENCIID AND D.DERSID = N.DERSID
        JOIN OGRETMEN T ON O.OGRETMENID = T.OGRETMENID
        WHERE T.EMAIL = (?)", xmail)
    """

    for data in cursor:
        my_tuple = ()
        for i in range(0,len(data)):
            deger = data[i]
            my_tuple = my_tuple + (deger,)

        studentTable.insert("", END, value=my_tuple)

except pyodbc.Error as ex:
    print("Failed! ",ex)



try:
    connection= pyodbc.connect('DRIVER={SQL SERVER};'+
                                    'Server=KORKMAZ\SQLEXPRESS;'+
                                    'Database=STUDENTMG_DB;'+
                                    'Trusted_Connection=True')
    cursor2 = connection.cursor()

    # Öğrenci sayısını hesaplamak için SQL sorgusu
    sql = """
    SELECT D.DERSID,D.DERSAD, COUNT(N.OGRENCIID) AS 'Öğrenci Sayısı'
    FROM DERS D
    JOIN NOTLAR N ON D.DERSID = N.DERSID
    WHERE D.OGRETMENID = ?
    GROUP BY D.DERSID,D.DERSAD;
    """
    cursor2.execute(sql,(global_deg.ogretmen_id,))

    for row in cursor2:
        ders_id, ders_adı, öğrenci_sayısı = row
        ders_tuple = (ders_id, ders_adı, öğrenci_sayısı)

        # Ders bilgilerini dersTable'a ekle
        dersTable.insert("", END, value=ders_tuple)

except pyodbc.Error as ex:
    print("Failed! ", ex)




try:
    connection= pyodbc.connect('DRIVER={SQL SERVER};'+
                                    'Server=KORKMAZ\SQLEXPRESS;'+
                                    'Database=STUDENTMG_DB;'+
                                    'Trusted_Connection=True')
    cursor3 = connection.cursor()

    sql = "SELECT DERSID, DERSAD FROM DERS WHERE OGRETMENID = ?"
    cursor3.execute(sql, (global_deg.ogretmen_id,))

    for row in cursor3:
        ders_id, ders_adı = row
        dersA_tuple = (ders_id, ders_adı)

        # Ders bilgilerini dersTable'a ekle
        dersATable.insert("", END, value=dersA_tuple)

except pyodbc.Error as ex:
    print("Failed! ", ex)




#HOCAYA AİT ÖĞRENCİLERİ GÖSTERSİN------> BİR SUTUN TREVİEWDA OGRETMEN ADI OLSUN BUNLARI JOINLE GOSTERCEN GALIBA
#Bİ TANE BUTON DA TÜM ÖĞRENCİLERİ GOR OLSUN

root.mainloop()


#öğrenci ara yap isim, soyisim, id olsun hangisini alırsa

#ders sil uyarı çıksın bu dersi alan öğrenci notları silinecek diye
#sonra notlardan sil