# ============== modules and libraries =========================================================
from tkinter import *
from tkcalendar import *
import tkinter.messagebox
import datetime
import sqlite3
# =============== root window and its configuration ============================================
root = Tk()
root.title('UDYOG')
screenwidth = root.winfo_screenwidth()
screenheight = root.winfo_screenheight()
root.geometry("%dx%d%+d%+d" % (screenwidth, screenheight, 0, 0))
root.minsize(900, 800)
root.resizable(width=FALSE, height=TRUE)
bgcolor = '#EEECEB'
root.configure(bg=bgcolor)
udyog = Label(root, text='UDYOG', bg=bgcolor, fg='grey', font=('poppins', 310))
# ================= frames  =====================================================================
loginframe = Frame(root, height=screenheight, width=screenwidth, bg='white')
signup_frame = Frame(root, height=150, width=250, bg=bgcolor)
sellerframe = Frame(root, height=screenheight, width=screenwidth*20/100, bg='skyblue')
productframe = Frame(root, height=screenheight, width=screenwidth*80/100, bg='#A1A1A1')
stocksframe = Frame(root, height=screenheight, width=screenwidth*80/100, bg=bgcolor)
saleframe = Frame(root, height=screenheight, width=screenwidth*80/100, bg='white')
dailyframe = Frame(root, height=screenheight, width=screenwidth*80/100, bg='white')
monthlyframe = Frame(root, height=screenheight, width=screenwidth*80/100, bg='white')
aboutframe = Frame(root, height=screenheight, width=screenwidth*80/100, bg='white')
buyerframe = Frame(root, height=screenheight, width=screenwidth*20/100, bg='skyblue')
shopframe = Frame(root, height=screenheight, width=screenwidth*80/100, bg=bgcolor)
wishlistframe = Frame(root, height=screenheight, width=screenwidth*80/100, bg=bgcolor,)

# ================images===========================================================================
iconimg = PhotoImage(file='resources/appicon.png')
loginbuttonimg = PhotoImage(file='resources/loginbutton.png')
signupbuttonimg = PhotoImage(file='resources/sigupbuttonimg.png')
existingimg = PhotoImage(file='resources/existingimg.png')
productbutton = PhotoImage(file='resources/addproduct.png')
stocksbutton = PhotoImage(file='resources/getstocks.png')
addtocartbutton = PhotoImage(file='resources/addtocart.png')
clearselectbutton = PhotoImage(file='resources/clearselection.png')
gettotalbutton = PhotoImage(file='resources/gettotal.png')
# ============== global variables ==================================================================
userid = ''
data = ''
# ================ variables for login and signup ================
userName = StringVar()
userPass = StringVar()
name = StringVar()
usertype = StringVar()
saleyear = StringVar()
salemonth = StringVar()
# =======variables for products additon==========
productname = StringVar()
productqty = IntVar()
productrate = DoubleVar()
units = StringVar()
# ==========app icon =============================
root.iconphoto(FALSE, iconimg)
# ========variables for wishlist =================
x = datetime.datetime.now()
responce = list()
slistitems = []
slstitemsqty = []
slstvar = []
itemrate = list()
itemunit = ''
selections = tuple()

# ======================================================================================================
flist = [sellerframe, productframe, stocksframe, buyerframe, shopframe,
                    wishlistframe, saleframe, dailyframe, monthlyframe]
framelist = [productframe, stocksframe, saleframe, dailyframe, monthlyframe]
framelist1 = [shopframe, wishlistframe]
scrollbar = Scrollbar(stocksframe)
scrollbar1 = Scrollbar(shopframe)
scrollbar2 = Scrollbar(wishlistframe)
stocklist = Listbox(stocksframe, yscrollcommand=scrollbar.set, font=('poppins', 20))
shoplist = Listbox(shopframe, yscrollcommand=scrollbar.set, font=('poppins', 20), selectmode=MULTIPLE)


# ======================================== Flags =============================================================

logincount = False
signupcount = False
sellercount = False
productcount = False
stockscount = False
salecount = False
dailycount = False
monthlycount =False
buyercount = False
shopcount = False
wishlistcount = False
# ================= functions and widget packings==========================================================

def validatelogin():
    global userid
    userid = userName.get()
    user = userName.get()
    pas = userPass.get()

    if len(user) == 0:
        tkinter.messagebox.showerror('Error', 'Blank UserID, try again')

    elif len(user) == 0 or len(pas) == 0:
        tkinter.messagebox.showerror('Error', 'Please fill the required information')

    elif len(user) <= 5 or len(user) >= 15:
        tkinter.messagebox.showerror('Error', 'Username must be between 5 to 15 characters')

    elif user.isalnum() != 1:
        tkinter.messagebox.showerror('Error', 'Special character or blank space in username is invalid')

    elif user.isalnum() and len(pas) > 7:
        try:
            login = FALSE
            connection = sqlite3.connect('udyog.db')
            cursor = connection.cursor()
            cursor.execute("""SELECT Username, Pass, Type FROM Users""")
            records = cursor.fetchall()
            for row in records:
                if row[0] == user and row[1] == pas:
                    login = True
                    if row[2] == 'SELLER':
                        tkinter.messagebox.showinfo('User Type', 'You are ' + row[2])
                        onseller()
                    elif row[2] == 'CONSUMER':
                        tkinter.messagebox.showinfo('User Type', 'You are ' + row[2])
                        onbuyer()
                userPass.set('')

            cursor.close()
            if not login:
                tkinter.messagebox.showerror('Error', 'Credentials Mismatch !!!')
        except sqlite3.Error as error:
            tkinter.messagebox.showerror('Error', error)


def validatesignup():
    user = userName.get()
    pword = userPass.get()
    typeofuser = usertype.get()
    nameofuser = name.get()
    nameofuser = nameofuser.upper()

    if len(user) == 0:
        tkinter.messagebox.showerror('Error', 'UserID can not be blank')

    elif nameofuser == '':
        tkinter.messagebox.showerror('Error', 'Full name can not be null')

    elif len(user) <= 5 or len(user) >= 15:
        tkinter.messagebox.showerror('Error', 'Username must be between 5 to 15 characters')

    elif user.isalnum() != 1:
        tkinter.messagebox.showerror('Error', 'Special character or blank space in username is invalid')

    elif pword == '':
        tkinter.messagebox.showerror('Error', 'Password can not be null')

    elif user.isalnum() and len(pword) > 7:
        try:
            conn = sqlite3.connect('udyog.db')
            cur = conn.cursor()

            cur.execute('''CREATE TABLE IF NOT EXISTS Users (
                            Username VARCHAR,
                            Name CHAR(30),
                            Pass VARCHAR,
                            Type CHAR
                            );''')

            cur.execute('SELECT Username FROM Users')
            query = cur.fetchall()
            if (user,) in query:
                tkinter.messagebox.showerror('Error', 'Username is already taken')
            else:
                cur.execute('''INSERT INTO Users (Username, Name, Pass, Type)
                            VALUES (?,?,?,?);''', (user, nameofuser, pword, typeofuser))
                conn.commit()
                cur.close()
                tkinter.messagebox.showinfo('Info', 'Account successfully created')
            cur.close()
            userName.set('')
            userPass.set('')

        except sqlite3.Error as error:
            tkinter.messagebox.showerror('Error', error)


def addproduct():
    product_name = productname.get()
    product_unit = units.get()
    product_qty = productqty.get()
    product_rate = productrate.get()

    if len(product_name) == 0 or product_qty == 0 or product_rate == 0:
        tkinter.messagebox.showerror('Empty Fields', 'Fields not filled properly')
    else:
        product_qty = int(product_qty)
        product_rate = float(product_rate)
        try:
            # x = datetime.datetime.now()
            conn = sqlite3.connect('udyog.db')
            cur = conn.cursor()

            cur.execute('''CREATE TABLE IF NOT EXISTS Inventory (
                            ItemName VARCHAR,
                            Unit CHAR(50),
                            Qty INT,
                            Rate FLOAT,
                            TotalCost FLOAT,
                            Date DATE
                            );''')
            cur.execute('''INSERT INTO Inventory (ItemName, Unit, Qty, Rate, TotalCost, Date)
                            VALUES (?,?,?,?,?,?);''', (product_name, product_unit, product_qty, product_rate, product_rate*product_qty, x.date()))
            conn.commit()
            cur.close()
            tkinter.messagebox.showinfo('Info', 'Product added to inventory')
            productname.set('')
            productqty.set('0')
            productrate.set('0.0')

        except sqlite3.Error as error:
            tkinter.messagebox.showerror('Error', error)


def getstocks():
    stocklist.delete(0, 'end')
    stocklist.insert(END, 'ItemName' + ' '*42 + 'Unit' + ' '*46 + 'Qty' + ' '*47 + 'Rate' + ' '*46)
    try:
        conn = sqlite3.connect('udyog.db')
        cur = conn.cursor()
        cur.execute('''SELECT ItemName, Unit, Qty, Rate FROM Inventory''')
        records = cur.fetchall()
        for i in range(len(records)):
            itemname = str(records[i][0])
            units = str(records[i][1])
            quantity = str(records[i][2])
            rate = str(records[i][3])
            if len(itemname) != 50:
                itemname = itemname + ' '*(50 - len(itemname))
            if len(units) != 50:
                units = units + ' '*(50 - len(units))
            if len(quantity) != 50:
                quantity = quantity + ' '*(50 - len(quantity))
            if len(rate) != 50:
                rate = rate + ' '*(50 - len(rate))
            stocklist.insert(END, '  ' + itemname + units + quantity + rate)
        cur.close()
    except sqlite3.Error as error:
        tkinter.messagebox.showerror('Error', error)


def addtocart():
    global selections
    selections = shoplist.curselection()
    if len(selections) != 0:
        wishlist()
        swappanebuyer(wishlistframe)
    else:
        tkinter.messagebox.showerror('Error', 'You have 0 products selected, please select products first')


def getqty():
    global itemrate, itemunit, slstvar, slistitems, slstitemsqty, selections
    try:
        conn = sqlite3.connect('udyog.db')
        cur = conn.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS Wishlist (
                        ItemName VARCHAR,
                        Unit VARCHAR,
                        Rate FLOAT,
                        Qty INT,
                        TotalCost FLOAT,
                        Date DATE
                        );''')

        cur.execute('''CREATE TABLE IF NOT EXISTS Sale (
                                            UserId VARCHAR,
                                            ItemName VARCHAR,
                                            Unit VARCHAR,
                                            Rate FLOAT,
                                            Qty INT,
                                            TotalCost FLOAT,
                                            Date DATE
                                            );''')

        for each in responce:
                alldata = each.split('-')
                itemname = str(alldata[0])
                itemunit = alldata[1]
                itemrate.append(float(alldata[2]))
                cur.execute('''INSERT INTO Wishlist (ItemName, Unit, Date)
                        VALUES (?,?,?);''', (itemname, itemunit, x.date()))
                conn.commit()

        for i in range(len(slistitems)):
            qty = slstitemsqty[i].get()
            cur.execute('''UPDATE Wishlist SET Qty = (?), TotalCost = (?), Rate = (?)
                         WHERE ItemName = (?);''', (int(qty), qty*itemrate[i], itemrate[i], slistitems[i]))
            conn.commit()
            cur.execute('''INSERT INTO Sale (UserId, ItemName, Unit, Rate, Qty, TotalCost, Date)
                        VALUES (?,?,?,?,?,?,?);''', (userid, slistitems[i], itemunit, itemrate[i], int(qty), qty*itemrate[i], x.date(),))
            conn.commit()

        for i in range(len(slistitems)):
            qty = slstitemsqty[i].get()
            cur.execute('''SELECT Qty FROM Inventory WHERE ItemName=(?);''', (slistitems[i],))
            qtyfrominventory = cur.fetchone()
            cur.execute('''UPDATE Inventory SET Qty = (?) WHERE ItemName=(?);''', (qtyfrominventory[0]-qty, slistitems[i]))
            cur.execute('''UPDATE Inventory SET TotalCost = (?) WHERE ItemName=(?);''', ((qtyfrominventory[0]-qty)*itemrate[i], slistitems[i]))
            conn.commit()

        cur.execute('''SELECT SUM(TotalCost) FROM Wishlist;''')
        records = cur.fetchone()
        tkinter.messagebox.showinfo('Grand Total', 'Your cart value is - ' + str(records[0]))
        cur.execute('''DROP TABLE Wishlist;''')
        conn.commit()
        cur.close()
        responce.clear()
        slistitems.clear()
        slstitemsqty.clear()
        slstvar.clear()
        itemrate.clear()
        itemunit = ''
        selections = tuple()

    except sqlite3.Error as error:
        tkinter.messagebox.showerror('Error', error)


def signup():
    global signupcount
    if signupcount:
        signup_frame.pack()
    else:
        greet_label = Label(signup_frame, text='Create An Account For UDYOG', bg=bgcolor, fg='#00A3F9', font=('poppins', 50))
        greet_label.pack(side=TOP, anchor='n')

        # rules
        rules = Label(signup_frame, text='''
        1. Username must be between 5 to 15 characters.
        2. must have letter and numbers.
        3. should not contain any special characters (for example: %, #, @).
        5. password must be greater than 7 characters.''', justify=LEFT, bg=bgcolor, fg='grey', font=('helvetica', 20))
        rules.pack()

        signcontainer = Frame(signup_frame, bg=bgcolor)
        signcontainer.pack()

        # Full name of user
        nameLabel = Label(signcontainer, text='Full Name', bg=bgcolor, fg='black', font=('poppins', 18))
        nameLabel.grid(row=1, column=1)
        nameEntry = Entry(signcontainer, textvariable=name, bg=bgcolor, borderwidth=2, font=('poppins', 18))
        nameEntry.grid(row=1, column=2, pady=5)

        # username
        userNameLabel = Label(signcontainer, text='User ID', bg=bgcolor, fg='black', font=('poppins', 18))
        userNameLabel.grid(row=2, column=1)
        userNameEntry = Entry(signcontainer, textvariable=userName,bg=bgcolor, font=('poppins', 18), borderwidth=2)
        userNameEntry.grid(row=2, column=2, pady=5)

        # pass
        userPassLabel = Label(signcontainer, text='Password', bg=bgcolor, fg='black', font=('poppins', 18))
        userPassLabel.grid(row=3, column=1)
        userPassEntry = Entry(signcontainer, textvariable=userPass, show='*', bg=bgcolor, font=('poppins', 18))
        userPassEntry.grid(row=3, column=2, pady=5)


        # user type
        OPTIONS = ["CONSUMER", "SELLER"]
        usertype.set(OPTIONS[0])
        usertypelabel = Label(signcontainer, text='You are - ', bg=bgcolor, fg='black', font=('poppins', 18))
        usertypelabel.grid(row=4, column=1)
        w = OptionMenu(signcontainer, usertype, *OPTIONS)
        w.grid(row=4, column=2, pady=5)

        # buttons
        signupbutton = Button(signcontainer, image=signupbuttonimg, command=validatesignup)
        signupbutton.grid(row=5, column=2, pady=8)
        backtologin = Button(signcontainer, image=existingimg, command=reloginwindow)
        backtologin.grid(row=6, column=2, pady=8)
        signup_frame.pack()
        signupcount = True


def loginWindow():
    global logincount
    if logincount:
        loginframe.pack(expand=TRUE, fill='both')
    else:
        greeting = Label(loginframe, text='''Welcome To UDYOG''', bg='white', fg='#7229F7', font=('poppins', 130))
        greeting.pack(side=TOP, anchor=N)

        logo = Label(loginframe, image=iconimg)
        logo.pack(pady=10)

        container = Frame(loginframe)
        container.pack()

        # username label and entry box
        userNameLabel = Label(container, text='User ID', bg='white', fg='black', font=('poppins', 18))
        userNameLabel.grid(row=1, column=1)
        userNameEntry = Entry(container, textvariable=userName, fg='black',
                              font=('poppins', 18), highlightbackground='lightgrey')
        userNameEntry.grid(row=1, column=2, padx=50, pady=15)

        # password label and entry box
        userPassLabel = Label(container, text='Password', bg='white', fg='black', font=('poppins', 18))
        userPassLabel.grid(row=2, column=1)
        userPassEntry = Entry(container, textvariable=userPass, fg='black', show="*",
                              font=('poppins', 18), highlightbackground='lightgrey')
        userPassEntry.bind("<Return>", (lambda event: validatelogin()))
        userPassEntry.grid(row=2, column=2)

        # Login &  button
        loginbutton = Button(container, image=loginbuttonimg, command=validatelogin)
        loginbutton.grid(row=3, column=2, pady=30)
        signupbutton = Button(container, image=signupbuttonimg, command=signupwindow)
        signupbutton.grid(row=4, column=2)
        loginframe.pack(expand=TRUE, fill='both')
        logincount = True


def seller():
    global sellercount
    if sellercount:
        sellerframe.pack(side='left', fill='both')
        sellerframe.propagate(0)
    else:
        inventory = Button(sellerframe, text='PRODUCTS', font=('poppins', 18), command=lambda: swappaneseller(productframe))
        inventory.pack(fill=BOTH, expand=1)

        stocks = Button(sellerframe, text='STOCKS', font=('poppins', 18), command=lambda: swappaneseller(stocksframe))
        stocks.pack(fill=BOTH, expand=1)

        sale = Button(sellerframe, text='SALE', font=('poppins', 18), command=lambda: swappaneseller(saleframe))
        sale.pack(fill=BOTH, expand=1)

        dailysheet = Button(sellerframe, text='DAILY SHEET', font=('poppins', 18), command=lambda: swappaneseller(dailyframe))
        dailysheet.pack(fill=BOTH, expand=1)

        monthlysheet = Button(sellerframe, text='MONTHLY SHEET', font=('poppins', 18), command=lambda: swappaneseller(monthlyframe))
        monthlysheet.pack(fill=BOTH, expand=1)

        sout = Button(sellerframe, text='SIGNOUT', font=('poppins', 18), command=signout)
        sout.pack(fill=BOTH, expand=1)

        # aboutlabel = Button(sellerframe, text='ABOUT VDYOG', font=('poppins', 18), command=lambda: swappaneseller(aboutframe))
        # aboutlabel.pack(fill=BOTH, expand=1)

        shut = Button(sellerframe, text='EXIT', font=('poppins', 18), command=shutdown)
        shut.pack(fill=BOTH, expand=1)

        sellerframe.pack(side='left', fill='both')
        sellerframe.propagate(0)
        sellercount = True


def products():
    global productcount
    if productcount:
        productframe.pack(side='right', fill='both')
        productframe.propagate(0)
    else:
        addproductlable = Label(productframe, text='Add Product In Inventory', bg='#A1A1A1', fg='white', font=('poppins', 40, 'normal'))
        addproductlable.pack(anchor=N, pady=30)

        productnamelabel = Label(productframe, text='Product Name', bg='#A1A1A1', fg='white', font=('poppins', 18))
        productnamelabel.place(x=290, y=180)
        productnameentry = Entry(productframe, textvariable=productname, bg='#A1A1A1', fg='white', font=('poppins', 18))
        productnameentry.place(x=550, y=180)

        unit = ['Kilogram', 'Litre', 'Bags', 'Bottles', 'Box', 'Dozens', 'Packs', 'Pieces', 'Tablets', 'Grams']
        productunitlabel = Label(productframe, text='Unit', bg='#A1A1A1', fg='white', font=('poppins', 18))
        productunitlabel.place(x=290, y=280)
        w = OptionMenu(productframe, units, *unit)
        units.set(unit[0])
        w.place(x=550, y=280)

        productqtylabel = Label(productframe, text='Quantity', bg='#A1A1A1', fg='white', font=('poppins', 18))
        productqtylabel.place(x=290, y=380)
        productqtyentry = Entry(productframe, textvariable=productqty, bg='#A1A1A1', fg='white', font=('poppins', 18))
        productqtyentry.place(x=550, y=380)

        productratelabel = Label(productframe, text='Rate Per Unit', bg='#A1A1A1', fg='white', font=('poppins', 18))
        productratelabel.place(x=290, y=480)
        productrateentry = Entry(productframe, textvariable=productrate, bg='#A1A1A1', fg='white', font=('poppins', 18))
        productrateentry.place(x=550, y=480)

        addproductbutton = Button(productframe, image=productbutton, bg='#A1A1A1', border=0, activebackground='#A1A1A1', command=addproduct)
        addproductbutton.place(x=550, y=580)

        productframe.pack(side='right', fill='both')
        productframe.propagate(0)
        productcount = True


def stocks():
    global stockscount
    if stockscount:
        stocksframe.pack(side='right', fill='both')
        stocksframe.propagate(0)
    else:
        stockslabel = Label(stocksframe, text='STOCKS', bg=bgcolor, fg='grey', font=('poppins', 40, 'normal'))
        stockslabel.pack(anchor=N, pady=30)
        getstocksbutton = Button(stocksframe, image=stocksbutton, bg=bgcolor, border=0, activebackground=bgcolor, command=getstocks)
        getstocksbutton.pack()
        stocklist.insert(END, 'ItemName' + ' '*42 + 'Unit' + ' '*46 + 'Qty' + ' '*47 + 'Rate' + ' '*46)
        stocklist.pack(side=LEFT, fill=BOTH, expand=TRUE)
        scrollbar.pack(side=RIGHT, fill=Y)
        scrollbar.config(command=stocklist.yview)

        stocksframe.pack(side='right', fill='both')
        stocksframe.propagate(0)
        stockscount = True


def sale():
    global salecount
    def grabsale():
        conn = sqlite3.connect('udyog.db')
        cur = conn.cursor()
        cur.execute('''SELECT SUM(TotalCost) FROM Sale WHERE Date=(?);''', [x.date()])
        record = cur.fetchone()
        salenumlabel.configure(text='₹ ' + str(record[0]))
        cur.close()

    if salecount:
        saleframe.pack(side='right', fill='both')
        saleframe.propagate(0)
    else:
        salelabel = Label(saleframe, text='''TODAY'S SALE''', bg='white', font=('Helvetica Neue', 80))
        salelabel.pack(anchor=N, pady=30)

        refreshlabel = Button(saleframe, text='REFRESH SALE', command=grabsale)
        refreshlabel.pack()

        salenumlabel = Label(saleframe, text='', bg='white', fg='#8900FF', font=('arial unicode ms', 200, 'bold'))
        salenumlabel.pack(anchor=N, pady=60)

        saleframe.pack(side='right', fill='both')
        saleframe.propagate(0)
        salecount = True


def daily():
    global dailycount, data

    def getdate():
        global data
        data = cal.get_date()
        conn = sqlite3.connect('udyog.db')
        cur = conn.cursor()
        cur.execute('''SELECT SUM(TotalCost) FROM Sale WHERE Date=(?);''', [data])
        record = cur.fetchone()
        salelabel.configure(text='₹ ' + str(record[0]))
        cur.close()

    if dailycount:
        dailyframe.pack(side='right', fill='both')
        dailyframe.propagate(0)
    else:
        cal = Calendar(dailyframe, seLectmode="month", year=x.year, month=x.month, day=x.day, date_pattern='y-mm-dd', font=('poppins', 20), selectforeground='red')
        cal.pack(fill=BOTH, expand=FALSE, pady=20)

        dailylabel = Label(dailyframe, text='''Select Day For Sale Records''', bg='white', font=('poppins', 20))
        dailylabel.pack(anchor=N)

        getdatebutton = Button(dailyframe, text='Get Sale', command=getdate)
        getdatebutton.pack(pady=5)

        salelabel = Label(dailyframe, text='', bg='white', fg='red', font=('arial unicode ms', 200, 'bold'))
        salelabel.pack(anchor=N, pady=5)

        dailyframe.pack(side='right', fill='both')
        dailyframe.propagate(0)
        dailycount = True


def monthly():
    global monthlycount, salemonth, saleyear

    def grabmonthsale():
        global salemonth, saleyear
        getmonth = salemonth.get()
        m = getmonth.split('-')
        mm = m[1]
        yyyy = saleyear.get()
        startdate = yyyy + '-' + mm + '-' + '01'
        enddate = yyyy + '-' + mm + '-' + '31'

        conn = sqlite3.connect('udyog.db')
        cur = conn.cursor()
        cur.execute('''SELECT SUM(TotalCost) FROM Sale WHERE Date >= (?) AND Date <= (?);''', (startdate, enddate))
        record = cur.fetchone()
        salenumlabel.configure(text='₹ ' + str(record[0]))
        cur.close()

    if monthlycount:
        monthlyframe.pack(side='right', fill='both')
        monthlyframe.propagate(0)
    else:
        salelabel = Label(monthlyframe, text='''MONTHLY SALE''', bg='white', font=('poppins', 50))
        salelabel.pack(anchor=N, pady=30)

        YEAR = ['2015', '2016', '2017', '2018', '2019', '2020', '2021']
        saleyear.set(YEAR[6])
        year = OptionMenu(monthlyframe, saleyear, *YEAR)
        year.pack(pady=10)

        MONTH = ['January-01', 'February-02', 'March-03', 'April-04', 'May-05', 'June-06', 'July-07', 'August-08',
                 'September-09', 'October-10', 'November-11', 'December-12']
        salemonth.set(MONTH[0])
        month = OptionMenu(monthlyframe, salemonth, *MONTH)
        month.pack(pady=10)

        getmonthbutton = Button(monthlyframe, text='Get Sale', command=grabmonthsale)
        getmonthbutton.pack(pady=10)

        salenumlabel = Label(monthlyframe, text='', bg='white', fg='#96CC39', font=('arial unicode ms', 200, 'bold'))
        salenumlabel.pack(anchor=N, pady=60)

        monthlyframe.pack(side='right', fill='both')
        monthlyframe.propagate(0)
        monthlycount = True


def buyer():
    global buyercount
    if buyercount:
        buyerframe.pack(side='left', fill='both')
        buyerframe.propagate(0)
    else:
        inventory = Button(buyerframe, text='SHOP PRODUCTS', font=('poppins', 18), command=lambda: swappanebuyer(shopframe))
        inventory.pack(fill=BOTH, expand=1)

        stocks = Button(buyerframe, text='', font=('poppins', 18))

        stocks.pack(fill=BOTH, expand=1)

        sign = Button(buyerframe, text='SIGNOUT', font=('poppins', 18), command=signout)
        sign.pack(fill=BOTH, expand=1)

        sale = Button(buyerframe, text='', font=('poppins', 18))
        sale.pack(fill=BOTH, expand=1)

        shut = Button(buyerframe, text='EXIT', font=('poppins', 18), command=shutdown)
        shut.pack(fill=BOTH, expand=1)

        buyerframe.pack(side='left', fill='both')
        buyerframe.propagate(0)
        buyercount = True


def shop():
    global shopcount

    def clearselect():
        shoplist.selection_clear(0, END)

    if shopcount:
        try:
            shoplist.delete(0, END)
            conn = sqlite3.connect('udyog.db')
            cur = conn.cursor()
            cur.execute('''SELECT ItemName, Unit, Rate FROM Inventory''')
            records = cur.fetchall()
            for i in range(len(records)):
                itemname = str(records[i][0])
                units = str(records[i][1])
                rate = str(records[i][2])
                shoplist.insert(END, itemname + '-' + units + '-' + rate)
            cur.close()
        except sqlite3.Error as error:
            tkinter.messagebox.showerror('Error', error)
        shopframe.pack(side='right', fill='both')
        shopframe.propagate(0)
    else:
        shopheadlabel = Label(shopframe, text='Select Products for shopping', bg=bgcolor, fg='grey', font=('poppins', 40))
        shopheadlabel.pack(anchor=N, pady=30)
        getshoplistbutton = Button(shopframe, image=addtocartbutton, bg=bgcolor, bd=5, anchor=CENTER, command=addtocart)
        getshoplistbutton.pack()
        clearselection = Button(shopframe, image=clearselectbutton, bg=bgcolor, bd=5, anchor=CENTER, command=clearselect)
        clearselection.pack()
        formatlabel = Label(shopframe, text='''List is displayed in following format (Itemname)-(Unit)-(Rate per unit)''', bg=bgcolor, fg='grey', font=('poppins', 20))
        formatlabel.pack()
        shoplist.delete(0, END)
        try:
            conn = sqlite3.connect('udyog.db')
            cur = conn.cursor()
            cur.execute('''SELECT ItemName, Unit, Rate FROM Inventory''')
            records = cur.fetchall()
            for i in range(len(records)):
                itemname = str(records[i][0])
                units = str(records[i][1])
                rate = str(records[i][2])
                shoplist.insert(END, itemname + '-' + units + '-' + rate)
            cur.close()
        except sqlite3.Error as error:
            tkinter.messagebox.showerror('Error', error)

        shoplist.pack(side=LEFT, fill=BOTH, expand=TRUE)
        scrollbar1.pack(side=RIGHT, fill=Y)
        scrollbar1.config(command=shoplist.yview)

        shopframe.pack(side=RIGHT, fill='both')
        shopframe.propagate(0)
        shopcount = True


def wishlist():
    global wishlistcount, selections, slstitems, slstitemsqty, slstvar
    selections = shoplist.curselection()

    if wishlistcount:
        wishlistframe.pack(side='left', fill='both')
        wishlistframe.propagate(0)
    else:
        for i in selections:
            entries = shoplist.get(i)
            responce.append(entries)
        for each in responce:
            alldata = each.split('-')
            slstitemsqty.append(alldata[0])
            slistitems.append(alldata[0])
            slstvar.append(alldata[0])

        for i in range(len(slstitemsqty)):
            slstitemsqty[i] = IntVar()

        selectquantitylabel = Label(wishlistframe, text='Select Quantity Of Each Products', bg=bgcolor, font=('poppins', 30))
        selectquantitylabel.pack(anchor=N, pady=30)

        for i in range(len(slistitems)):
            l1 = Label(wishlistframe, text=slistitems[i], bg=bgcolor, font=('poppins', 18))
            l1.pack()
            s1 = Scale(wishlistframe, variable=slstitemsqty[i], from_=1, to=50, orient=HORIZONTAL, bg=bgcolor, font=('poppins', 18), length=200)
            s1.pack()

        getqtybutton = Button(wishlistframe, image=gettotalbutton, bg=bgcolor, border=0, command=getqty)
        getqtybutton.pack(pady=50)
        scrollbar2.pack(side=RIGHT, fill=Y)
        scrollbar2.config(command=shoplist.yview)
        # wishlistframe.configure(yscrollcommand=scrollbar2.set)
        wishlistframe.pack(side='right', fill='both')
        wishlistframe.propagate(0)
        wishlistcount = True


def signout():
    res = tkinter.messagebox.askquestion('Sign Out', 'Do you really want to sign out ?')
    if res == 'yes':
        for x in flist:
            x.pack_forget()
        udyog.pack_forget()
        loginframe.pack(expand=TRUE, fill='both')
    else:
        pass


def shutdown():
    res = tkinter.messagebox.askquestion('Exit Application', 'Do you really want to exit')
    if res == 'yes':
        root.destroy()
    else: pass


def swappaneseller(frame):
    for x in framelist:
        x.pack_forget()
    udyog.pack_forget()
    if frame == saleframe:
        frame.update()
        frame.pack()
    else:
        frame.pack()


def swappanebuyer(frame):
    for x in framelist1:
        x.pack_forget()
    udyog.pack_forget()
    if frame == wishlistframe:
        frame.update()
        frame.pack()
    else:
        frame.pack()


def onseller():
    loginframe.pack_forget()
    seller()
    stocks()
    products()
    sale()
    daily()
    monthly()
    stocksframe.pack_forget()
    productframe.pack_forget()
    saleframe.pack_forget()
    dailyframe.pack_forget()
    monthlyframe.pack_forget()
    udyog.pack(side=RIGHT, anchor=CENTER)


def onbuyer():
    loginframe.pack_forget()
    buyer()
    shop()
    shopframe.pack_forget()
    udyog.pack(side=RIGHT, anchor=CENTER)


def signupwindow():
    loginframe.pack_forget()
    signup()


def reloginwindow():
    signup_frame.pack_forget()
    loginWindow()


loginWindow()
root.mainloop()
