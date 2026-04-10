# Sound Gear Inventory System. 
The system will be able to allow users to log in, save their details, and give them access to different parts of the system depending on their roles.
The roles will be. 
1. Cage manager(Manager). There can be more than one CM, but not more than 4. 
2. Community alums(Users)(infinity)
3. Guest. ??

   The CM will be able to :
   1. Add and remove items from the inventory system. (Primary role) (CRUD operations)
   2. Change prices of items and the duration they can be borrowed.
  
   The users will be able to:
   1. Borrow/return items.
   2. 
      
I will be designing and implementing a RESTful API for an Inventory Management System. 

Build a Flask-based REST API

Implement core features such as:

User authentication (login/register) & Role-Based Access controls
1. Product management (CRUD operations)
2. Category and supplier management
3. Inventory tracking
4. Stock transactions (in/out)
5. Use proper HTTP methods and status codes
6. Structure your project clearly (models, routes, etc.)
7. Return data in JSON format






Endpoint                       Methods  Rule                   
-----------------------------  -------  -----------------------
auth.get_users                 GET      /auth/users                     CM
auth.login                     POST     /auth/login                     USER/PUBLIC
auth.register                  POST     /auth/register                  USER/PUBLIC
home                           GET      /                               USER/PUBLIC
items.create_item              POST     /items/                         CM
items.delete_item              DELETE   /items/<int:id>                 CM
items.get_items                GET      /items/                         PUBLIC/GUEST
items.update_item              PATCH    /items/<int:id>                 CM        
transactions.all_transactions  GET      /transactions/                  CM
transactions.borrow_item       POST     /transactions/borrow            USER
transactions.my_transactions   GET      /transactions/my                USER
transactions.return_item       POST     /transactions/return            USER