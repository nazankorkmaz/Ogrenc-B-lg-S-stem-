#https://www.youtube.com/watch?v=k9ICA7LDIZQ&list=PLUgFQtEcQLl_TmkNjA-UHg-PNABqTuXPb&index=53


from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox
import pyodbc
from tkinter import ttk
import customtkinter

import global_deg

def login():
    try:
        connection = pyodbc.connect('DRIVER={SQL SERVER};' +
                                    'Server=KORKMAZ\SQLEXPRESS;' +
                                    'Database=STUDENTMG_DB;' +
                                    'Trusted_Connection=True')
        cursor = connection.cursor()

        username = usernameEntry.get()
        password = passwordEntry.get()

        if username == "" or password == "":
            messagebox.showerror("Hata", "Alan boş bırakılamaz")
        else:
            cursor.execute("SELECT EMAIL, SIFRE FROM OGRETMEN WHERE EMAIL=? AND SIFRE=?", (username, password))
            row = cursor.fetchone()
            if row:
                messagebox.showinfo("Başarılı", "Giriş yapıldı")
                window.destroy()
                global_deg.ogretmenin_maili =  username
                cursor.execute("SELECT OGRETMENID, AD, SOYAD FROM OGRETMEN WHERE EMAIL = ?", username)
                # Sonucu al
                row2 = cursor.fetchone()
                if row2:
                    oid = row2[0]
                    print(f"Öğretmenin ID'si: {oid}")
                    global_deg.ogretmen_id = oid
                    global_deg.ogretmen_name = row2[1]
                    global_deg.ogretmen_lname = row2[2]

                import sms  # Bu kısmı sizin uygulamanızın ana sayfasına yönlendirecek bir komutla değiştirin
            else:
                messagebox.showwarning("Hatalı Giriş", "Kullanıcı adı veya şifre hatalı!")
    except pyodbc.Error as ex:
        print("Failed! ", ex)




def signInPage():
    signInWindow = Toplevel()
    signInWindow.geometry('470x300+730+230')
    signInWindow.title("Yeni Kayıt Sayfası")
    signInWindow.resizable(0, 0)

    unameLabel = Label(signInWindow, text="İsim", font=("arial", 15))
    unameLabel.place(relx=0.2, rely=0.1)
    unameEntry = Entry(signInWindow, bd=1)
    unameEntry.place(relx=0.45, rely=0.1)

    usurnameLabel = Label(signInWindow, text="Soyisim ", font=("arial", 15))
    usurnameLabel.place(relx=0.2, rely=0.22)
    usurnameEntry = Entry(signInWindow, bd=1)
    usurnameEntry.place(relx=0.45, rely=0.22)

    emailLabel = Label(signInWindow, text="Email ", font=("arial", 15))
    emailLabel.place(relx=0.2, rely=0.34)
    emailEntry = Entry(signInWindow, bd=1)
    emailEntry.place(relx=0.45, rely=0.34)

    passwordLabel = Label(signInWindow, text="Şifre", font=("arial", 15))
    passwordLabel.place(relx=0.2, rely=0.46)
    passwordEntry = Entry(signInWindow, bd=1)
    passwordEntry.place(relx=0.45, rely=0.46)

    def saveUser():
        name = unameEntry.get()
        lname = usurnameEntry.get()
        email = emailEntry.get()
        password = passwordEntry.get()

        try:
            connection = pyodbc.connect('DRIVER={SQL SERVER};' +
                                        'Server=KORKMAZ\SQLEXPRESS;' +
                                        'Database=STUDENTMG_DB;' +
                                        'Trusted_Connection=True')

            cursor = connection.cursor()

            # Yeni kaydı ekle
            cursor.execute("INSERT INTO OGRETMEN (AD, SOYAD, EMAIL, SIFRE) VALUES (?, ?, ?,?)",
                           (name, lname, email,password))

            # Değişiklikleri kaydet
            connection.commit()
            messagebox.showinfo("Başarılı", "Kayıt yapıldı")
            info_label.configure(text="Kullanıcı Kaydı Tamamlandı!")

            # Bağlantıyı kapat
            connection.close()

            connection = pyodbc.connect('DRIVER={SQL SERVER};' +
                                        'Server=KORKMAZ\SQLEXPRESS;' +
                                        'Database=STUDENTMG_DB;' +
                                        'Trusted_Connection=True')

            cursor = connection.cursor()
            cursor.execute("SELECT * FROM OGRETMEN ORDER BY OGRETMENID DESC")

            rows = cursor.fetchall()

            for row in rows:
                print(row)

            connection.close()
            #signInWindow.after(8000,signInWindow.destroy())

        except pyodbc.Error as ex:
            print("Failed! ", ex)
            info_label.configure(text="INSERT FAILED!")
        signInWindow.after(3000, signInWindow.destroy())

    saveButton = customtkinter.CTkButton(signInWindow, text="Kaydet", fg_color="green",command=saveUser)
    saveButton.place(relx=0.25, rely=0.7)

    info_label = customtkinter.CTkLabel(signInWindow, text="")
    info_label.place(relx=0.25, rely=0.8)

window=Tk()
window.geometry('1380x700+100+50')
window.title("Öğrenci Bilgi Sistemi Giriş")
window.resizable(False,False)


image = Image.open("photo/tahta.jpg")#resmi yükle
image=image.resize((1380,700))
backgroundImage= ImageTk.PhotoImage(image)
bgLabel =Label(window,image=backgroundImage)
#bgLabel.pack(fill="both", expand=True)
bgLabel.place(x=0,y=0)


loginFrame= Frame(window,background="#DFD9D8", highlightthickness=2, highlightbackground="black")
loginFrame.place(relx=0.5, rely=0.5, anchor="center")


imageStudent = Image.open("photo/student.png")#resmi yükle
imageStudent=imageStudent.resize((150,150))
logoImage= ImageTk.PhotoImage(imageStudent)
logoLabel =Label(loginFrame,image=logoImage, bg="#172905")
logoLabel.grid(row=0,column=0,columnspan=2, pady=10) #columspan yani 2 sutun kaplasın


userNameIm=Image.open("photo/user.png")
userNameIm=userNameIm.resize((30,30))
logoUsername= ImageTk.PhotoImage(userNameIm)
userNameLabel=Label(loginFrame,image=logoUsername,text="Kullanıcı Adı",compound=LEFT, font="20", padx=10, pady=10,background="#DFD9D8")
#compound=LEFT: Bu parametre, görüntü ve metni nasıl düzenleyeceğinizi belirtir.
userNameLabel.grid(row=1,column=0)

usernameEntry =Entry(loginFrame,font="20")
usernameEntry.grid(row=1,column=1, padx=5)


passwordIm=Image.open("photo/padlock.png")
passwordIm=passwordIm.resize((30,30))
logopassword= ImageTk.PhotoImage(passwordIm)
passwordLabel=Label(loginFrame,image=logopassword,text="Şifre",compound=LEFT, font="20", padx=10, pady=10,background="#DFD9D8")
passwordLabel.grid(row=2,column=0, sticky=W) #sola yapışsın

passwordEntry =Entry(loginFrame,font="20")
passwordEntry.grid(row=2,column=1, padx=5)


loginButton=Button(loginFrame, text="Giriş", font="20", width=15, activebackground="#172905", cursor="hand2", command=login)
loginButton.grid(row=3,column=0, columnspan=2,pady=10)

new_ogretmen=Label(window,text="Yeni Kayıt Açmak İçin", font=('Open Sans',13,'bold'))
new_ogretmen.place(relx=0.5, rely=0.82, anchor="e")

signInButton=Button(window, text="Tıklayınız!", font=('Open Sans',13,'bold underline'), bd=0, activebackground="firebrick1", activeforeground="blue",cursor="hand2",command=signInPage)
signInButton.place(relx=0.51, rely=0.82, anchor="w")



try:
    connection= pyodbc.connect('DRIVER={SQL SERVER};'+
                                    'Server=KORKMAZ\SQLEXPRESS;'+
                                    'Database=STUDENTMG_DB;'+
                                    'Trusted_Connection=True')
    cursor = connection.cursor()
    cursor.execute("SELECT EMAIL,SIFRE FROM OGRETMEN")
    for row in cursor:
        email= row.EMAIL
        sifre = row.SIFRE
        print(f"Email: {email}, Şifre: {sifre}")

except pyodbc.Error as ex:
    print("Failed! ",ex)

window.mainloop()