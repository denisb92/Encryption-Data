import Tkinter
import tkMessageBox
from Tkinter import *
import MySQLdb
from ttk import*
import re
import base64


#Login Form Sets the format of the form 

top = Tk()
top.title("Login")
top.geometry('{}x{}'.format(300, 300))
top.resizable(0,0)
#Adds Entry fields for the user to enter the username and password 
Login = Label(top,text = "Login Page").grid(row =0,column = 1, padx = 10, pady = 10)
username = Label(top,text = "Username").grid(row =1)

password = Label(top, text = "Password").grid(row=2)


EUSER = Entry(top)
EPASS = Entry(top,show = "*")


EUSER.grid(row= 1, column = 1,padx = 10, pady=10)
EPASS.grid(row=2,column = 1,padx = 10, pady =10)



def access():
   #Sets up the connection to the database
    
    name = EUSER.get()
    Pass = EPASS.get()
    db = MySQLdb.connect(host="localhost",   
                     user="root",         
                     passwd="",  
                     db="pythondata")
      
    cur = db.cursor()
    #sql to find out if the username and password are correct for the user 
    sql = "SELECT SecurityQuestion FROM data WHERE Username= '"+name+"' AND Password = '"+Pass+"'"
   
    
    #executes the sql query  
    cur.execute(sql)
    #If the Username/Password is incorrect an error message pops up otherwise the infopage function is called
    if cur.fetchone() == None:
         tkMessageBox.showerror("Error", "Incorrect Username/Password")
    else:
         infopage()

    #closes the database connection 
    EUSER.delete(0,'end')
    EPASS.delete(0,'end')
    db.close()

def decrypt(key,info):
    #Simple algorithmn for decrypting the encrypted Data for the user
    decoded_chars = []
    info = base64.urlsafe_b64decode(info)
    for i in xrange(len(info)):
        key_c = key[i%len(key)]
        decoded_c = chr(abs(ord(info[i]) - ord(key_c) %256))
        decoded_chars.append(decoded_c)
    decoded_string = "".join(decoded_chars)
    return decoded_string

def encrypt(key, info):
    #Simple algorithmn that encrypts the Data for the user
    encoded_chars = []
    for i in xrange(len(info)):
        key_c = key[i%len(key)]
        encoded_c = chr(ord(info[i]) + ord(key_c) %256)
        encoded_chars.append(encoded_c)
    encoded_string = "".join(encoded_chars)
    return base64.urlsafe_b64encode(encoded_string)

def saveInfo(topinfo,info,name):
    #This function receives the information that the user has entered , encrypts it , and sends it to the database
    #Sets up the connection for the database
    db = MySQLdb.connect(host="localhost",   
                     user="root",       
                     passwd="",  
                     db="pythondata")
     
    cur = db.cursor()
    #Calls the encrypt function which takes the information entered and encrypts it 
    encrypted= encrypt('12224321',info)
    #sql request to update the Data for the Users account
    #Updates, informs the user and closes the window , error shows up if the save was not able to be made 
    try:

        sql = "UPDATE data SET DataString = '"+encrypted+"' WHERE Username = '"+name+"'"
        cur.execute(sql)
        db.commit()
        tkMessageBox.showinfo("Success", "Save Complete")
        db.close()
        topinfo.destroy()
    except:
        tkMessageBox.showerror("Error", "Unable To Save")



def infopage():
    #This function asks the database for the Users Data , decrypts it and displays it to the user in a textfield so they can edit/add to it
    #Sets up the database connection 
    db = MySQLdb.connect(host="localhost",    
                     user="root",         
                     passwd="",  
                     db="pythondata")
       
    cur = db.cursor()
    user = EUSER.get()
    #sql request to receive the data for the current user logged in 
    sql = "SELECT DataString FROM data WHERE Username = '"+EUSER.get()+"'"
    cur.execute(sql)
    data = cur.fetchall()
    #Calls the decrypt function to decrypt the data
    decrypted = decrypt('12224321',str(data))
    #Sets up the format for the form displayed
    topinfo = Toplevel()
    topinfo.geometry('{}x{}'.format(400, 400))
    topinfo.title("Hello " + EUSER.get())
    topinfo.resizable(0,0)
    field = Text(topinfo,height = 20, width = 50)
    field.insert(INSERT,decrypted)
    field.grid(row =0)
    db.close()
    #Button that saves the new Data
    save = Button(topinfo, text = "Save", command = lambda: saveInfo(topinfo,field.get('1.0','end'),user)).grid(row = 1,pady = 5)
    
def retrieve(top2, U,  SQ):  
    #Retrieves the Forgotten Password and displays it to the user after they entered their username and answer the Security question 
     db = MySQLdb.connect(host="localhost",   
                     user="root",         
                     passwd="",  
                     db="pythondata")
       
     cur = db.cursor()
    #sql query to retrieve the password for the user 
     sql = "SELECT Password FROM data WHERE Username= '"+U+"' AND SecurityQuestion = '"+SQ+"'"
     cur.execute(sql)
     #Displays a messagebox with the password , or returns an error box if the security question was answered incorrectly
     accData = cur.fetchall()
     if(len(accData) != 0):
        tkMessageBox.showinfo("The Password", accData)
        db.close()
        top2.destroy()
     else:
        tkMessageBox.showerror("Error", "Incorrect Answer")
     return 
def VerifyUser(top1,U):
    #This function verifys if the Username that the user entered exists in the database
     db = MySQLdb.connect(host="localhost",   
                     user="root",         
                     passwd="", 
                     db="pythondata")
       
     cur = db.cursor()
     #sql query to show the security question that the user needs to answer
     sql = "SELECT SecurityQuestionQ FROM data WHERE Username= '"+U+"'"
     cur.execute(sql)
     #Calls the function to display the Security question or an error message that the user doesnt exist in the database
     SQ = cur.fetchall()
     if(len(SQ) != 0):
         ForgotPass2(U, SQ)
         top1.destroy()
         db.close()
     else:
         tkMessageBox.showerror("Error", "User Doesnt Exist")
     return
def ForgotPass2(U,SQ):
    #This function displays the security question the user has to answer and the form format for it 
     top2 = Tk()
     top2.geometry('{}x{}'.format(360,100))
     top2.title("Forgot Password: Security Question")
     header = Label(top2,text= "Answer the Security Question").grid(row =0,column = 1)
     security = Label(top2, text = SQ).grid(row = 2)
     top2.resizable(0,0)
     eSecurity = Entry(top2)
     #Calls the retrieve function after the user enters the question 
     eSecurity.grid(row= 2, column = 1,padx = 10, pady=10)
     submit = Button(top2, text = "Submit" ,command = lambda: retrieve(top2,U,eSecurity.get())).grid(row = 3,column =1)
     return 

def ForgotPass1():
    #Asks the user for their username in order to retrieve their password , format for the form 
     top1 = Tk()
     top1.geometry('{}x{}'.format(360,100))
     top1.title("Forgot Password: Username")
     header = Label(top1,text= "Enter in the Username").grid(row =0,column = 1)
     user = Label(top1,text = "Username").grid(row = 1,padx = 10, pady = 10)
     top1.resizable(0,0)
     
     eUser = Entry(top1)
    
     eUser.grid(row= 1, column = 1,padx = 10, pady=10)
    #Submitting the username enters the verifyUser function 
     submit = Button(top1, text = "Submit" ,command = lambda: VerifyUser(top1,eUser.get())).grid(row=2,column = 1)
     return
def PasswordStrength(Password):
    Upper=len(set(re.findall(r'[A-Z]',Password)))
    Lower=len(set(re.findall(r'[a-z]',Password)))
    Nums=len(set(re.findall(r'[0-9]',Password)))
    Symb=len(set(re.findall(r'[~!@#$%^&\*()_+=-`]',Password)))
    Strength = Nums + Symb 
    if(Upper < 1 or Nums < 1 or Symb < 1):
        tkMessageBox.showerror("Error", "Password must have atleast one Upper Case , Number, and Special Symbol")
    elif(Strength < 5):
        Ok = tkMessageBox.askyesno("Unsecure Password" ,"The password is Weak, Continue?", icon = "warning")
        if(Ok == True):
            return 1
        else:
            return 2


   

def check(top1, USER, PASS1, PASS2 , Q,A):
    #This function checks all the fields if the AddAccount function and makes sure everything is entered properly
    db = MySQLdb.connect(host="localhost",    
                     user="root",        
                     passwd="",  
                     db="pythondata")
       
    cur = db.cursor()
    #sql query to ask for the username that was entered to check if it already exists or not 
    sqlcheck = "SELECT Username FROM data WHERE Username = '"+USER+"'"
    cur.execute(sqlcheck)
    data = cur.fetchall()
    answer= PasswordStrength(PASS1)
    if len(data) != 0:
        #Error that shows the username already exists
        tkMessageBox.showerror("Error", "Username exists")
    elif (len(PASS1) < 8 ):
         tkMessageBox.showerror("Error", "Password must be atleast 8 characters long")
         
    elif (PASS1 != PASS2):
        #Error that shows the Password and Password confirm do not match 
        tkMessageBox.showerror("Error", "Passwords do not match")
    elif(USER == "" or PASS1 == "" or PASS2 == "" or Q == ""):
        #Error to show that one or more of the fields are empty and need to be entered
        tkMessageBox.showerror("Error", "Please Fill In Every Field")
    elif(answer ==2):
        tkMessageBox.showerror("Error", "Please enter in a new password")
    else:
        
        
            
        #If everything is entered properly an sql is run to add the new user into the database
        try:
            sql = "INSERT INTO data(Username, Password, SecurityQuestionQ, SecurityQuestion, DataString)VALUES('"+USER+"' , '"+PASS1+"' , '"+Q+"' , '"+A+"', '  ')" 
            cur.execute(sql)
            db.commit()
            db.close()
            #adds the new User along with an empty Data String which the user will add to as their info 
            tkMessageBox.showinfo("Created", "Account has been created")
            top1.destroy()
        except:
            #Error if the account was not able to be created
            tkMessageBox.showerror("Error", "Account has not been created")
        return 1
          


    
def AddAccount():
    #This function is the format for the form for the user to create a new account 
     top1 = Toplevel()
     top1.geometry('{}x{}'.format(350,300))
     top1.title("Add Account")
     top1.focus_set

     #They have to enter a Username , Password , Confirm Password and pick and answer a security question from the list 
     user = Label(top1,text = "Username").grid(row = 0,padx = 10, pady = 10)
     top1.resizable(0,0)
     Password = Label(top1, text = "Password").grid(row = 1)
     Password2 = Label(top1,text ="Confirm Password").grid(row = 2)
     Questions = Tkinter.StringVar()
     SecurityQ = Label(top1,text = "Security Question").grid(row = 3,padx = 20, pady = 10)
     Security = Combobox(top1, textvariable = Questions,state = 'readonly')
     Security['values'] = ("First Pet's Name", "First School Attended", "Favorite Movie", "Favorite Book")
     Security.current(0)
     Security.grid(row = 4 ,padx = 10)
   

     eUser = Entry(top1)
     ePass = Entry(top1)
     ePass2 = Entry(top1)
     eSecurityQ = Entry(top1)
     eUser.delete(0, 'end')
     ePass.delete(0,'end')
     ePass2.delete(0,'end')
     eSecurityQ.delete(0,'end')
     eUser.grid(row= 0, column = 1,padx = 10, pady=10)
     ePass.grid(row = 1, column= 1,padx = 10 , pady = 10)
     ePass2.grid(row = 2, column= 1,padx = 10 , pady = 10)
     eSecurityQ.grid(row= 4, column = 1,padx = 20, pady=20)
     Create = Button(top1, text = "Create Account" , command = lambda:  check(top1, eUser.get(), ePass.get(),ePass2.get(),Security.get(), eSecurityQ.get())).grid(row = 5, pady = 5,padx = 5)
    
     return
#The Buttons for the user to Login, Retrieve Password, and add a new account 
Login = Button(top, text = "Login", command = access).grid(row = 3, column = 1 , pady = 5)
FgPass = Button(top,text = "Forgot Password", command = ForgotPass1).grid(row =6, column = 1, pady = 5)
Add = Button(top, text = "Add account", command = AddAccount).grid(row =9,column = 1 , pady=5)



top.mainloop()