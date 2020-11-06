from datetime import datetime 
from pytz import timezone
import json
from menu import *
from config import *
from random import randint
import random
import string
report_data=''
def UpdateOrder(orderID,PrivateID,Total,ordered_list,customer):
    try:
        ordid=''
        ordid+=''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        rec={
            "_id": ordid,
            'customerID':customer.cid,
            'orderID':orderID,
            'PID':PrivateID,
            'Total':Total
        }
        db.coll2.order.insert_one(rec)
        for i,food in enumerate(ordered_list):
            id1=randint(100,999)
            rec1={
                "_id":id1,
                'orderID':orderID,
                'itemID':food.fid,
                'fooditem':food.name,
                'foodqty':food.qty,
                'foodprice':food.price
            }
            db.coll3.orderDetails.insert_one(rec1)
    except Exception as e:
        print(e)
        print('\nError occured in updateOrder\n')

def report(orderID,PrivateID,total,ordered_list,tax,customer):
    global report_data
    UpdateOrder(orderID,PrivateID,total,ordered_list,customer)
    report_data = '\n' + '\t\t' + '*'*40 + '\n'

    now = datetime.now()
    date = '-'.join(list(map(str,[now.day,now.month,now.year])))

    now_utc = datetime.now(timezone('UTC'))
    time = now_utc.astimezone(timezone('Asia/Kolkata'))
    time = time.strftime("%I:%M:%S %p" )
    report_data = '\n' + '\t\t' + '.'*60 + '\n'
    report_data+='\n\t\t'+ 'SR CAfe'.center(60," ")+'\t\t'
    report_data += '\n' + '\t\t' + '.'*60 + '\n'
    report_data+='\n\t\t'+'BG (P)LTD-SR DIVN'.center(60," ")
    report_data+='\n\t\t'+ 'No.324,Brookefields Mall'.center(60," ")+'\t'
    report_data+='\n\t\t'+' '*1+'Coimbatore-641001'.center(60," ")+'\t'
    report_data+='\n\t\t'+' '*1+'Ph.0422-2448666'.center(60," ")+'\t'
    report_data += '\n' + '\t\t' + '.'*60 + '\n'
    report_data +='\n'+'Booking Date : '.rjust(31," ")+date.rjust(5,' ')+' '*2+time
    report_data+='\n'+'CUSTOMER ID '.rjust(28," ")+':'.center(3," ")+str(customer.cid).ljust(10," ")+'\n'+'ORDER ID '.rjust(28," ")+':'.center(3," ")+str(orderID).ljust(10," ")+'\n'+'PRIVATE ID '.rjust(28," ")+':'.center(3," ")+str(PrivateID).ljust(10," ")+'\n'+'CUSTOMER NAME '.rjust(28," ")+':'.center(3," ")+customer.cname + '\n' + 'CUST EMAIL '.rjust(28," ")+':'.center(3," ") + customer.email+'\n\n'
    report_data +='\t\t' + '.'*60 + '\n\n' 
    report_data+='\t\t|NO| '.center(5,' ')+' |ITEM ID| '.center(10,' ')+' |FOOD NAME| '.ljust(15,' ')+'  |PRICE x QUANTITY = TOTAL|'
    for i,item in enumerate(ordered_list):
        amt=item.price*item.qty
        temp = '\n\t\t{:^5}{:^10}{:^15}{:^10}x   {:<5} =  Rs.{:<4}'.format(i+1,item.fid,item.name,item.price,item.qty,amt)
        report_data += temp
    report_data += '\n\t\t' + '.'*60+'\n'+'\t\t'+'CGST.'.rjust(45,' ')+ ' '*8+('Rs.'+str(tax)).ljust(5," ") + '\n'
    report_data += '\t\t'+'SGST.'.rjust(45,' ')+ ' '*8+('Rs.'+str(tax)).ljust(5," ") + '\n\n'
    report_data += '\t\t' + '.'*60 + '\n' + '\t\t' + '  TOTAL'.rjust(45," ") +' '*8+ ('Rs.'+str(total)).ljust(5," ") + '\n\n'
    report_data +='\t\t' + '.'*60 + '\n\n' 
    report_data += '\n\n\t\t'+'Thank you for choosing our Store!!!'.center(60," ")+'\t\t' 
    report_data +="\n\t\t"+"Hope you have enjoyed our food!!!".center(60," ")+'\t\t' 
    report_data +="\n\t\t"+"Visit Again.".center(58," ")+'\n\n' 
    report_data += '\t\t' + '.'*60 + '\n\n' 
    key=randint(2000,8000)   
    """         
    record={
        "_id":key,
        'orderID': orderID,
        'CID': customer.cid,
        #'report_data': 1,
    }
    db.coll4.report.insert_one(record)"""
def view_report(customerid):
    try:
        #rep=db.coll4.report.find({'CID':customerid},{'report_data':1})
        if(db.coll4.report.count_documents({'CID':customerid})>0):
            print(report_data)
            #print(rep['report_data'])
        else:
            print('\nOrder is not placed!\n')
    except Exception as e:
        print(e)
        print("\nError Occured view report\n")


#CUSTOMER ID : '+str(customer.cid).ljust(20," ")