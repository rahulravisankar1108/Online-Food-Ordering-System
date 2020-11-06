import hashlib
from random import randint
from pprint import pprint
from config import *
from menu import *
from report1 import *
i=randint(1,1000)
print('#'*10+' WELCOME '+'#'*10)
def checkUser(email):
    try:
        while True:
            cur=db.coll.login.count_documents({"email":email})
            if(cur==0):
                return 
            else:
                print("\nUser Already Exists!!\n")
            email=input("Enter E-mail address or press E to exit: ")
        if(email.lower()=='e'):
            main()
    except Exception:
        print("\nError occured...\n")
        main()

def encryptPassword(Password):
    en=hashlib.sha256(Password.encode()).hexdigest()
    return en

def SignUp():
    name=input("\nEnter Full Name : ")
    userName=input("\nEnter User Name (should consist atleast one alphabet and number): ")
    email=input("\nEnter E-Mail Address : ")    
    checkUser(email)
    mobileNo=input("\nEnter Mobile Number : ")
    password=input("\nEnter Password : ")
    encryptPass=encryptPassword(password)
    address=input("\nEnter Address : ")
    rec={
        "_id":i,
        'name':name,
        'email':email,
        'userName':userName,
        'password':encryptPass,
        'mobileNo':mobileNo,
        'address':address
    }
    try:
        db.coll.login.insert_one(rec)
    except Exception as e:
        print(e)
        main()
    print('\n'+'Sign Up Successful'.center(40,'*'),'\n')
    #mainFn(name,email)
    main()
def ValidateEmail(email):
    try:
        while True:
            cur=db.coll.login.count_documents({"email":email})
            if(cur==0):
                print('\nUser Does not exist!!\n')
            else:
                return email
            email=input("\nEnter E-mail ID or press E to exit : ")
            if(email.lower()=='e'):
                main()
    except:
        print("\nError Occured VE!!!\n")
        main()

def ValidatePassword(password,email):
    try:
        ctn=5
        while True:
            user=db.coll.login.find_one({'email':email})
            if(user and user['password']==password):
                return
            ctn-=1
            print("\nPassword Incorrect!\n",ctn,"attempt(s) more.\n")
            if ctn>0:
                pwd=input("\nEnter Password : ")
                password=encryptPassword(pwd)
            else:
                break
        main()
    except Exception as e:
        print('\nError Occured VP\n',e)
        main()

def getUserName(email):
    try:
        cur=db.coll.login.find_one({"email":email},{"name":1,"_id":0})
        if(cur!=None):
            return cur["name"]
        else:
            print("name not found")
    except:
        print("\nError occured USERNAME\n")
        main()

def Login():
    while True:
        email=input("\nEnter E-mail ID : ")
        email=ValidateEmail(email)
        password=input("\nEnter Password : ")
        pwd=encryptPassword(password)
        ValidatePassword(pwd,email)
        name=getUserName(email)
        print("\n"+'*'*5+" Login Successful "+name+"  "+'*'*5+'\n')
        mainFn(name,email)
        main()
def Admin_Food_management():
    y=1
    while y!=-1:
        print("\n"+" ADMIN FOOD MANAGEMENT PAGE ".center(60,'*'))
        print("\n"+' '*5+'1.Add Food items\n'+' '*5+'2.Update any items price\n'+' '*5+'3.Update any items quantity\n'+' '*5+'4.View Added items list\n'+' '*5+'5.Delete ONE Item\n'+' '*5+'6.Delete ALL items from list\n'+' '*5+'7.Exit\n')
        ch=int(input("Enter an option (1-7): "))
        if(ch==1):
            n=int(input("\nEnter Number of food items : "))
            for i in range(n):
                print("Enter "+str(i+1)+" Food item : ",end="")
                fitem=input()
                print("Enter "+fitem+" Food price : ",end="")
                fprice=int(input())
                print("Enter "+fitem+" Food Qty : ",end="")
                fqty=int(input())
                key=randint(1001,9999)
                record={
                    "_id":key,
                    'fooditem':fitem,
                    'foodprice':fprice,
                    'foodqty':fqty
                }
                try:
                    db.coll1.food.insert_one(record)
                    print("Food item ",(i+1)," added successfully!!\n")
                except Exception as e:
                    print(e)
                    main()       
        elif(ch==2):
            print("Enter the item name to update the price of that : ",end="")
            fitem=input()
            filter={'fooditem':fitem}
            print("Enter the new price for "+fitem)
            fprice=int(input())
            try:
                db.coll1.food.update_one(filter,{"$set":{'foodprice':fprice}})
            except Exception as e:
                print(e)
        elif(ch==3):
            print("Enter the item name to update the quantity of that : ",end="")
            fitem=input()
            filter={'fooditem':fitem}
            print("Enter the new quantity for "+fitem)
            fqty=int(input())
            try:
                db.coll1.food.update_one(filter,{"$set":{'foodqty':fqty}})
            except Exception as e:
                print(e)
        elif(ch==4):
            if(db.coll1.food.count_documents({})==0):
                print("\nNo items in the list!!\n\n\t ADD ITEM TO VIEW THE LIST\n")
            else:
                cur=db.coll1.food.find()
                for food in cur:
                    pprint(food)
        elif(ch==5):
            print("Enter the item name to Delete : ",end="")
            fitem=input()
            cur=db.coll1.food.find_one_and_delete({'fooditem':fitem})
            print("Deleted Food details : ")
            pprint(cur)
        elif(ch==6):
            try:
                db.coll1.food.delete_many({})
                db.coll2.order.delete_many({})
                db.coll3.orderDetails.delete_many({})
                db.coll4.report.delete_many({})
                print("Food items list deleted successfully!!!\n")
            except Exception as e:
                print(e)
                main()      
        else:
            print("Food list added.\n THANK YOU") 
            y=-1 
            main()  

def Admin_Monitor(admin_orderID):
    print("\n"+" Admin Monitor ".center(60,"*")+"\n")
    print("\n\n"+"S.No".center(6," ")+"Item ID".center(10," ")+"Food Item".center(20," ")+"Food Qty".center(20," ")+'\t\t')
    i=1
    try:
        cur=db.coll3.orderDetails.find({'orderID':int(admin_orderID)})
        for obj in cur:
            print("\n"+str(i).center(6," ")+str(obj['itemID']).center(10," ")+str(obj['fooditem']).center(20," ")+str(obj['foodqty']).center(20," ")+'\t\t')
            i+=1
    except Exception as e:
        print(e) 
    return

def Admin_Counter():
    while True:
        print("\n"+" Admin Counter ".center(60,"*")+"\n")
        print("\n\n"+"Order ID : ",end=" ")
        admin_orderID=int(input())
        print("\n\n"+"Private ID : ",end=" ")
        admin_Private_ID=input()
        cur=db.coll2.order.find({'orderID':admin_orderID})
        if(cur):
            for obj in cur:
                if(obj['PID']==admin_Private_ID):
                    cur1=db.coll.login.find({"_id":obj['customerID']})
                    for obj1 in cur1:
                        print("\n\n"+"Customer Name : "+obj1['name'].ljust(20," ")+"\nCustomer ID : "+str(obj['customerID']).ljust(20," "))
                    print("\nTotal :",obj['Total']) 
                    Admin_Monitor(int(admin_orderID))
        print("\nAre more customers waiting Y/N: ",end=" ")
        ch=input()
        if(ch.upper()=='Y'):
            continue
        else:
            Admin_portal()

def Admin_portal():
    y=1
    while y!=-1:
        print("\n"+"1.Admin Food management Page\n2.Admin Counter\n3.Log Out")
        ch=int(input("Enter a number between (1 and 3) : "))
        if(ch==1):
            Admin_Food_management()
        elif(ch==2):
            Admin_Counter()
        elif(ch==3):
            print("\n"+" Admin Log Out Successful ".center(40,'*')+"\n")
            main()
        else:
            print("\nEnter Valid Data between (1 and 3)!!\n")

def AdminLogin():
    uname=input("Enter admin username : ")
    while True:
        ctn1=5
        if(uname=="SRCafe" ):
            upass=input("Enter admin password : ")
            ctn=5
            if( upass=="Qazwsxedc123!@#"):
                print("\n"+"WELCOME ADMIN".center(30,'*'))
                print("\n What you would like to do? : ")
                Admin_portal()
            else:
                ctn-=1
                print("\nPassword Incorrect! ",ctn," attempt(s) more.\n")
                if ctn>0:
                    upass=input("\nEnter Password : ")
                else:
                    break
        else:
            ctn1-=1
            print("\nUsername Incorrect! ",ctn1," attempt(s) more.\n")
            if ctn1>0:
                uname=input("\nEnter Admin Username : ")
            else:
                break
    main()

def main():
    i=1
    while(i==1):
        print("\n"+' '*5+'1.Sign Up\n'+' '*5+'2.Login\n'+' '*5+'3.Admin login\n'+' '*5+'4.Exit\n')
        choice=input("Enter an option : ")
        if(choice=='1'):
            SignUp()
        elif(choice=='2'):
            Login()
        elif(choice=='3'):
            AdminLogin()
        else:
            print('#'*5+"  Thank you for choosing our Cafe"+'!'*5+"\nHope you enjoyed our food!!!\n"+'#'*5)
            i=-1
            quit()

main()