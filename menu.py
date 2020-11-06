from config import * 
#from main import *
from pprint import pprint
from random import randint
import random
import string
from report1 import *
from email import *
#initializaion
food_list=[]
ordered_list=[]
customer=''
class Customer:
    def __init__(self,cid,email,cname,mobno):
        self.cid=cid
        self.email=email
        self.cname=cname
        self.mobno=mobno
class Food:
    def __init__(self,fid,name,price,qty):
        self.fid=fid 
        self.name=name 
        self.price=int(price)
        self.quantity=int(qty)
class Order:
    def __init__(self,fid,name,price,qty):
        self.fid=fid
        self.name=name
        self.qty=qty
        self.price=price
def getCustomerDetails(email):
    try:
        global customer
        cur=db.coll.login.find_one({'email':email})
        customer=Customer(cur['_id'],cur['name'],cur['mobileNo'],cur['email'])
    except Exception as e:
        print(e)
        print('\nError occured getCUSTDET\n')
def load_food():
    try:
        global food_list
        cur=db.coll1.food.find({})
        for i in cur:
            obj=Food(i["_id"],i['fooditem'],i['foodprice'],i['foodqty'])
            food_list.append(obj)
    except Exception:
        print("\nError Occured load food\n")
def menu():
    while True:
        print('\n'*3)
        print(' MAIN MENU '.center(60,'*')+'\n\n\t(O)Order Food\n\t(C)View Cart\n\t(R)Report\n\t(E)Exit\n'+'_'*60+'\n')
        option = input('Select an Option: ').upper()
        if option=='O':
            order_food()
        if option=='C':
            view_cart()
        if option=='E':
            exit_menu()
        if option=='R':
            view_report(customer.cid)
        else:
            print('Invalid option, Enter Again!!!')
def order_food():
    while True:
        global ordered_list
        print('\n'*2)
        print(' ORDER FOOD '.center(80,'*'))
        print('\n'+'\t'+'|NO|'.center(6,' ')+' |FOOD ID| '.center(10,' ')+' |FOOD NAME| '.center(20,' ')+' |AVAILABLE QUANTITY| '.center(20,' ')+'  |PRICE| '.center(10,' '))
        for i,food in enumerate(food_list):
            print('\t{:^6}{:^10}{:^20}{:^20}  Rs.{:^7}'.format(i+1,food.fid,food.name,food.quantity,food.price))
        print('\n'+'(C)Choose Food '+' '*10+'(M)Main Menu'+' '*10+'(E)Exit')
        print('_'*80+'\n')
        fid=input('Select Your Option: ')
        print()
        if fid.upper()=='C':
            while True:
                order_quantity=input('Enter the number of foods that you want within (1-20) : ')
                if order_quantity.isdigit():
                    order_quantity=int(order_quantity)
                    break
                else:
                    print('\nEnter valid data!!!\n')
            for i in range(order_quantity):
                print("Enter the food ID from the above list which you want to order : ",end=" ")
                ofid=int(input())
                print("Enter the number of unit of ",ofid," you want : ",end=" ")
                oqty=int(input())
                for obj in food_list:
                    if ofid==obj.fid:
                        name=obj.name
                        ordered_list.append(Order(ofid,name,obj.price,oqty))
                        if(obj.quantity>0):
                            actualqty=int(obj.quantity-oqty)
                            db.coll1.food.update_one({"_id":ofid},{"$set":{"foodqty":actualqty}})
                        else:
                            print("\nThe food item(s)"+ str(obj.fid)+"has quantity : "+str(obj.quantity)+"\nChoose another item\n")
            print("\nYour Foods has been added to the cart!\n\tView Cart to see summary!!\n\n")
        elif fid.upper()=='E':
            exit_menu() 
        elif fid.upper()=='M':
            menu()
        else:
            print('Invalid option,Enter Again!!!')
def view_cart():
    while 1:
        order_total=0
        print('\n'*5)
        print(' MANAGE ORDERS AND CART '.center(80,'*')+'\n')
        if ordered_list:
            print('\t|NO| '.center(5,' ')+' |ITEM ID| '.center(10,' ')+' |FOOD NAME| '.ljust(15,' ')+'  |PRICE x QUANTITY = TOTAL|'+'\n')
            for i,food in enumerate(ordered_list):
                amt=food.qty*food.price
                print('\t{:^5}{:^10}{:^15}{:^10}x   {:<5} =  Rs.{:<4}'.format(i+1,food.fid,food.name,food.price,food.qty,amt))
                order_total+=amt
            print('\t'+'-'*60)
            tax1=order_total*0.04
            tax=round(tax1,2)
            order_total+=(tax*2)
            ot=round(order_total,3)
            print('\tCGST.    '+('Rs. '+str(tax)).rjust(50,' '))
            print('\tSGST.    '+('Rs. '+str(tax)).rjust(50,' '))
            print('\t'+'-'*60)
            print('\tTotal    '+('Rs. '+str(ot)).rjust(50,' '))
            print('\n(M) Main Menu'+' '*3+'(UI) Update Existing Items'+' '*3+'(DO) Delete ONE ITEM From List'+' '*3+'(DA) Delete ALL ITEMS From List'+' '*3+'(O) Order More Food'+'\n'+' '*5+"(P) Payment"+' '*5+'(E)Exit')
            print('_'*60+'\n')
            option=input("Enter an option: ").upper()
            if option=='O':
                order_food()
            if option=='M':
                menu()
            elif option=='P':
                payment(order_total,tax)
            elif option=='E':
                exit_menu()
            elif option=='UI':
                update_existing()
            elif option=='DO':
                delete_one()
            elif option=='DA':
                delete_all()
            else:
                print('Invalid option, Enter Again!!!')
        else:
            print('\n'+'Cart is empty'.center(60,'-'))
            menu()

def update_existing():
    i=1
    while i==1 or ch=='Y':
        print("Enter the food ID from your list which you want to update : ",end=" ")
        ofid=int(input())
        print("Enter the quantity that you need to update : ",end=" ")
        uqty=int(input())
        for obj in ordered_list:
            if(obj.fid==ofid):
                bqty=obj.qty
                obj.qty=uqty
        print("\nThe item ID ",ofid," has been updated with quantity from ",bqty," to ",uqty)
        print("\nDo you want to update more items from your list? (Y/N) : ")
        ch=input("Enter Y for YES or N for NO : ")
        i=-1
    else:
        view_cart()
def delete_one():
    option = input('\nEnter Number to Remove: ')    
    if option.isalpha() or int(option) >  len(ordered_list):
            print('Invalid Input!!!')
    else:
            item = ordered_list.pop(int(option)-1)
            print(item.name+' Removed...')
def delete_all():
    clear_data()
    print("\nAll items has been deleted from the list.")

def payment(total,tax):
    tax=tax
    if ordered_list:
        global orderid
        orderid=randint(100000,999999)
        PrivateID=''
        PrivateID+=''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        report(orderid,PrivateID,total,ordered_list,tax,customer)
        email(orderID,PrivateID,total,customer.cname,tax,customer.email)
        print('\nTotal amount: Rs. ',total)
        print('\n'+'Payment Successful!!!\n')
        #rep=db.coll4.report.find({'CID':customer.cid},{'report_data':1})
        if(db.coll4.report.count_documents({'CID':customer.cid})>0):
            print(report_data)
    else:
        print(' Cart is empty '.center(40,"-"))
    menu()

def clear_data():
    global ordered_list
    ordered_list = []

def exit_menu():
    print("Logout Successfull")
    print('#'*50+"\nThank you for choosing our Store"+'!'*5+"\nHope you have enjoyed our food!!!\n"+'#'*50)
    #clear_data()
    main()

def mainFn(name,email):
    try:
        if name and email:
            getCustomerDetails(email)
            load_food()
            menu()
        else:
            print('Session Expired')
    except Exception as e:
        print(e)
        print('Error Occured mainfn\n')
        menu()  


"""
clear_data()
        db.coll2.order.delete_many({"orderID":orderid})
        db.coll3.orderDetails.delete_many({"orderID":orderid})
        db.coll4.report.delete_many({"orderID":orderid})
        print('*-'*50+"\nThank you for choosing our Store"+'!'*5+"\nHope you have enjoyed our food!!!\n"+'#'*50)
        quit()
        global username, ordered_list
        username = ''
        ordered_list = []
"""