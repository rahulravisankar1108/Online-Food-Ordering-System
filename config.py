from pymongo import MongoClient
from pprint import pprint
conn=MongoClient('localhost',27017)
db=conn.RSrestaurant
coll=db.login #login
coll1=db.food #food list
coll2=db.order #customer's ordered list
coll3=db.orderDetails #inner monitor,order ID,foodID,foodname,qty,time
coll4=db.report
 
#for obj in db.coll3.orderDetails.find({}):
    #pprint(obj)


