import smtplib 
from menu import *
from config import *
def email(orderID,PrivateID,total,cus_name,tax,cus_email):
    EMAIL_ADDRESS="sender's email"
    EMAIL_PASSWORD='sender"s password'
    order_cur=db.coll2.order.find_one({"orderID":orderID})
    food_details_cur=db.coll3.orderDetails.find({"orderID":orderID})
    with smtplib.SMTP('smtp.gmail.com',587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(EMAIL_ADDRESS,EMAIL_PASSWORD)
        subject=f'Booking Confirmation on SR Foods\nOrder No. -{orderID}'
        body=f"Hi {cus_name}(User ID : {order_cur['customerID']}),\nCongratulations! Thank you for using SR foods's online Booking facility.\nYour booking details are indicated below.\n"
        body1=f"\nOrderID : {orderID}\nPrivateID : {order_cur['PID']}\n"
        body2=f"\nORDERED FOOD DETAILS :\n{'S.NO'.ljust(6,' ')}  {'ITEM ID'.ljust(6,' ')}  {'FOOD ITEM'.ljust(10,' ')}  {'QTY'.ljust(6,' ')}  {'PRICE'.ljust(6,' ')}\n"
        for i,food in enumerate(food_details_cur):
            body3+=f"{str(i+1).ljust(6,' ')}  {str(food.itemID).ljust(6,' ')}  {(food.fooditem).ljust(10,' ')}  {str(food.foodqty).ljust(6,' ')}  Rs.{str(food.foodprice).ljust(6,' ')}"
        body4=f"\nFARE DETAILS\n+SUB-TOTAL : {total-tax}\nTAX : {tax}\nTOTAL : {total}"
        body5=f"\n\n\nWarm Regards,\nCustomer Care\nInternet Booking\nSR Cafe\n"
        body6=f"\nAddress : \nNo.403,3rd Floor Brookefields Mall,Coimbatore-641001."
        msg=f'Subject:{subject}\n\n{body}\n{body1}\n{body2}{body3}\n{body4}\n{body5}\n{body6}'
        smtp.sendmail(EMAIL_ADDRESS,'rrr110800@gmail.com',msg)
