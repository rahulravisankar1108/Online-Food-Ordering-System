# Online-Food-Ordering-System
A console based application to signup/login by the customer to order food, view cart, manage cart and by the administrator to manage the food, quantity of food and price of the same daily.

The main aim of the project is to cut down the waiting time in the counter of fast food shops for instance Burger King, KFC. _Unlike the other food ordering application the customer will order food from a remote place, but here the customer will order and the customer will go and pick it up!_
___The difference is the customer need not to go to the shop and order the food after going to the shop as it leads to run out of time for the customers. Instead, the customer will order the food before the customer arrives to that shop to cut down the waiting time.___  
 
 The customer will have an ORDER ID and PRIVATE CODE in their confirmation Mail, after confirming the same, the ordered food can be given to the customer. 
 
 ## Requirements
 
  * [Python3](https://www.python.org/downloads/ "Python3")
 
  * [PyMongo] (https://pypi.org/project/pymongo/ "PyMongo")
  
  * [MongoDB Compass] (https://www.mongodb.com/try/download/community "MongoDB Compass")
  
  * [Hashlib] (https://docs.python.org/2/library/hashlib.html "Hashlib")
  
 
 ## Technology Stack
 
  1. Python
  
  2. MongoDB
  
 ## Project Flow
 
   ___1. Customer Flow___
    _1. Create Account
    2. Login 
    3. Order Food
    4. View Cart
    5. Manage Cart
        1. Delete Ordered Food
           1. Delete the One item from the Cart
           2. Delete ALL items from the Cart
        2. Update Existing Food item in the cart
        3. Order More
     6. Payment
     7. View Report(E-Bill Generation)
     8. LogOut_
     
   ___2. Administrator Flow___
     _1. Login
     2. Admin Action
        1. Admin Food Management List
            1. Add Food items
            2. Update any item's price 
            3. Update any item's quantity
            4. View Added item's list
            5. Delete One item the menu
            6. Delete ALL items from the menu
        2. Admin Counter (The counter for the                     administrator for User Query)
        3. Admin Monitor (To view the ordered food               list)
        4. LogOut_
