import sqlite3 as s
# global countCustomers

class Database:
    def __init__(self):
        pass

    @staticmethod
    def CreateTableAdmin():
        connection = s.connect("carSystem.db")
        cursor = connection.cursor()
        cursor.execute('''
        CREATE TABLE Admin(
        admin_id       int PRIMARY KEY ,
        admin_email    VARCHAR (30) ,
        admin_password VARCHAR (30)
        )
        ''')
        connection.commit()
        connection.close()

    @staticmethod
    def insertIntoAdmin(id, email, password):
        connection = s.connect("carSystem.db")
        cursor = connection.cursor()
        try:
            cursor.execute("INSERT INTO ADMIN VALUES (?,?,?)",
                        (id, email, password))
            connection.commit()
        except:
            connection.rollback()
        connection.close()

    @staticmethod
    def checkInAdmin(email, password):
        connection = s.connect("carSystem.db")
        cursor = connection.cursor()
        admins = cursor.execute("SELECT * from Admin")
        for admin in admins:
            if (email and password) in admin:
                return True
        return False

    @staticmethod
    def returnAdmins():
        connection = s.connect("carSystem.db")
        cursor = connection.cursor()
        admins = cursor.execute("SELECT * from Admin")
        return admins

    @staticmethod
    def CreateTableCustomer():
        connection = s.connect("carSystem.db")
        cursor = connection.cursor()
        cursor.execute('''
        CREATE TABLE Customers(
        customer_id    INTEGER PRIMARY KEY AUTOINCREMENT,
        phone_no       varchar (25),
        user_name      VARCHAR (30),
        first_name     VARCHAR (30),
        last_name      VARCHAR (30),
        password        VARCHAR (30),
        address        VARCHAR (100),
        email          VARCHAR (50),
        admin_id        int not null,
        FOREIGN KEY (ADMIN_ID) REFERENCES ADMIN(ADMIN_ID)
        )
        '''
                       )
        connection.commit()
        connection.close()

    @staticmethod
    def insertIntoCustomer(first_name, last_name, username, Useremail, Userpassword, phone, address):
        connection = s.connect("carSystem.db")
        cursor = connection.cursor()
        cursor.execute("pragma foreign_keys=on")
        cursor.execute("BEGIN TRANSACTION")
        try:
            cursor.execute('''INSERT INTO CUSTOMERS(phone_no,user_name,first_name,last_name,password,address,email,admin_id) VALUES
            (?,?,?,?,?,?,?,?)
            ''', (phone, username, first_name, last_name, Userpassword, address, Useremail, 1))
            connection.commit()
        except:
            connection.rollback()
        connection.close()

    # @staticmethod
    # def updateCustomerWithPayId(cus_id, pay_id):
    #     connection = s.connect("carSystem.db")
    #     cursor = connection.cursor()
    #     cursor.execute("pragma foreign_keys=on")
    #     cursor.execute(
    #         f"UPDATE Customers SET pay_id = '{pay_id}' WHERE customer_id = {cus_id}")
    #     connection.commit()
    #     connection.close()

    @ staticmethod
    def customerIdExists(id):
        connection = s.connect("carSystem.db")
        cursor = connection.cursor()
        customerCountList = cursor.execute(
            f"SELECT COUNT(*) FROM Customers WHERE customer_id = {id}").fetchone()
        return int(''.join([str(n) for n in customerCountList])) == 1

    @staticmethod
    def deleteCustomer(id):
        connection = s.connect("carSystem.db")
        cursor = connection.cursor()
        cursor.execute("pragma foreign_keys=on")
        cursor.execute("BEGIN TRANSACTION")
        try:
            cursor.execute(f"DELETE FROM Customers WHERE customer_id = {id}")
            connection.commit()
        except:
            connection.rollback()
        connection.close()

    @staticmethod
    def checkIfCustomerAlreadyExistForLogin(Useremail, Userpassword):
        connection = s.connect("carSystem.db")
        cursor = connection.cursor()
        Customers = cursor.execute("SELECT * from Customers")
        for customer in Customers:
            if (Useremail and Userpassword) in customer:
                return True
        return False
    
    @staticmethod
    def checkIfCustomerAlreadyExistForSignUp(Useremail, Userpassword):
        connection = s.connect("carSystem.db")
        cursor = connection.cursor()
        Customers = cursor.execute("SELECT * from Customers")
        for customer in Customers:
            if (Useremail and Userpassword) in customer:
                return True
            if (Useremail) in customer:
                return True
        return False

    @staticmethod
    def returnCustomerAccordingToSession(email, password):
        connection = s.connect("carSystem.db")
        cursor = connection.cursor()
        customer = cursor.execute(
            f"SELECT * from Customers where email = '{email}' and password = '{password}'")
        return customer

    @staticmethod
    def returnCustomers():
        connection = s.connect("carSystem.db")
        cursor = connection.cursor()
        customers = cursor.execute("SELECT * from Customers")
        return customers

    @staticmethod
    def CreateTablecar():
        connection = s.connect("carSystem.db")
        cursor = connection.cursor()
        cursor.execute('''
        CREATE TABLE car
    (
        car_no          INTEGER PRIMARY KEY AUTOINCREMENT ,
        car_image       VARCHAR(300) ,
        car_price       int,
        car_title       VARCHAR (100) ,
        car_description VARCHAR (500) ,
        admin_id         int NOT NULL,
        FOREIGN KEY (ADMIN_ID) REFERENCES ADMIN(ADMIN_ID)
    )

        ''')
        connection.commit()
        connection.close()

    @staticmethod
    def InsertIntocar(img, price, title, desc, admin_id):
        connection = s.connect("carSystem.db")
        cursor = connection.cursor()
        cursor.execute("pragma foreign_keys=on")
        cursor.execute("BEGIN TRANSACTION")
        try:
            cursor.execute('''
            INSERT INTO car(car_image,car_price,car_title,car_description,admin_id) VALUES
            (?, ?, ?, ?, ?)
            ''', (img, price, title, desc, admin_id))
            connection.commit()
        except:
            connection.rollback()
        connection.close()

    @staticmethod
    def deletecar(id):
        connection = s.connect("carSystem.db")
        cursor = connection.cursor()
        cursor.execute("pragma foreign_keys=on")
        cursor.execute("BEGIN TRANSACTION")
        try:
            cursor.execute(f"DELETE FROM car WHERE car_no = {id}")
            connection.commit()
        except:
            connection.rollback()
        connection.close()

    @staticmethod
    def updatecar(id, title, price, desc, img):
        connection = s.connect("carSystem.db")
        cursor = connection.cursor()
        cursor.execute("pragma foreign_keys=on")
        cursor.execute("BEGIN TRANSACTION")
        try:
            cursor.execute(
                f"UPDATE car SET car_title = '{title}' WHERE car_no = {id}")
            
            cursor.execute(
                f"UPDATE car SET car_price = '{price}' WHERE car_no = {id}")
            
            cursor.execute(
                f"UPDATE car SET car_description = '{desc}' WHERE car_no = {id}")
            
            cursor.execute(
                f"UPDATE car SET car_image = '{img}' WHERE car_no = {id}")
            connection.commit()

        except:
            connection.rollback()
        connection.close()

    @ staticmethod
    def carsFilterBy(filter):
        connection = s.connect("carSystem.db")
        cursor = connection.cursor()
        cars = cursor.execute("SELECT * FROM car ORDER BY " + filter)
        return cars

    @ staticmethod
    def returncarById(id):
        connection = s.connect("carSystem.db")
        cursor = connection.cursor()
        car = cursor.execute(f"SELECT * FROM car WHERE car_no = {id}")
        return car

    @ staticmethod
    def carIdExists(id):
        connection = s.connect("carSystem.db")
        cursor = connection.cursor()
        carcountList = cursor.execute(
            f"SELECT COUNT(*) FROM car WHERE car_no = {id}").fetchone()
        return int(''.join([str(n) for n in carcountList])) == 1

    @ staticmethod
    def returncars():
        connection = s.connect("carSystem.db")
        cursor = connection.cursor()
        cars = cursor.execute("SELECT * from car")
        return cars

    @staticmethod
    def deleteAllcars():
        connection = s.connect("carSystem.db")
        cursor = connection.cursor()
        cursor.execute("pragma foreign_keys=on")
        cursor.execute("BEGIN TRANSACTION")
        try:
            cursor.execute(f"DELETE FROM car")
            connection.commit()
        except:
            connection.rollback()
        connection.close()

    @ staticmethod
    def CreateTableOrdered():
        connection = s.connect("carSystem.db")
        cursor = connection.cursor()
        cursor.execute('''
    CREATE TABLE Ordered (
        Order_Id        INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id	    int NOT NULL,
        car_no	        int NOT NULL,
        pay_id	        int NOT NULL,
        ordered_date	TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        quantity	    int DEFAULT 0,
        pay_amount	    int NOT NULL CHECK("pay_amount" > 0),
        order_status    VARCHAR(10) default 'Pending' CHECK(order_status='Pending' OR order_status='Delivered'),    
        FOREIGN KEY(pay_id) REFERENCES Payment(pay_id) on delete set NULL,
        FOREIGN KEY(car_no) REFERENCES car(car_no) on delete cascade,
        FOREIGN KEY(customer_id) REFERENCES CUSTOMERS(customer_id) on delete cascade
    )
        ''')
        connection.commit()
        connection.close()


    # @staticmethod
    # def InsertIntoORDERED(customerId, carno, quantity, payId, pay_amount):
    #     connection = s.connect("carSystem.db")
    #     cursor = connection.cursor()
    #     cursor.execute("pragma foreign_keys=on")
    #     try:
    #         cursor.execute('''
    #         INSERT INTO ORDERED(customer_id,car_no,quantity,pay_id, pay_amount) VALUES
    #         (?, ?, ?, ?, ?)
    #         ''', (customerId, carno, quantity, payId, pay_amount))
    #         cursor.execute("ROLLBACK TO SAVEPOINT restart_from_payment")
    #         connection.commit()
    #     except:
    #         cursor.execute("ROLLBACK TO SAVEPOINT restart_from_payment")
    #     connection.close()

    @staticmethod
    def updateOrderStatusToDelivered(order_id):
        connection = s.connect("carSystem.db")
        cursor = connection.cursor()
        cursor.execute("pragma foreign_keys=on")
        try:
            cursor.execute(f"UPDATE ORDERED SET order_status = 'Delivered' where Order_Id = {order_id}")
            connection.commit()
        except:
            connection.rollback()
        connection.close()

    @staticmethod
    def deleteOrderWithOrderId(order_id):
        connection = s.connect("carSystem.db")
        cursor = connection.cursor()
        cursor.execute("pragma foreign_keys=on")
        try:
            cursor.execute(f"delete from ORDERED where Order_Id = {order_id}")
            connection.commit()
        except:
            connection.rollback()
        connection.close()

    @staticmethod
    def returnOrderDetailsOfCustomerWithJoins(customerId):
        connection = s.connect("carSystem.db")
        cursor = connection.cursor()
        orderDetails = cursor.execute(f'''
        SELECT ORDERED.Order_ID, car.car_title, car.car_price, car.car_image, ORDERED.ordered_date,
        ORDERED.quantity, ORDERED.pay_amount, Payment.pay_number, ORDERED.order_status FROM ORDERED
        INNER JOIN CUSTOMERS
        ON ORDERED.customer_id = CUSTOMERS.customer_id
        INNER JOIN PAYMENT
        ON ORDERED.pay_id = PAYMENT.pay_id
        INNER JOIN car
        ON ORDERED.car_no = car.car_no
        where CUSTOMERS.customer_id = '{customerId}'
        order by ORDERED.Order_ID DESC
        ''')
        return orderDetails

    @staticmethod
    def returnAllOrderDetailsOfCustomerWithJoins():
        connection = s.connect("carSystem.db")
        cursor = connection.cursor()
        orderDetails = cursor.execute(f'''
        SELECT Customers.first_name, Customers.last_name, ORDERED.Order_ID, car.car_title, car.car_price, car.car_image, ORDERED.ordered_date,
        ORDERED.quantity, ORDERED.pay_amount, Payment.pay_number, ORDERED.order_status FROM ORDERED
        INNER JOIN CUSTOMERS
        ON ORDERED.customer_id = CUSTOMERS.customer_id
        INNER JOIN PAYMENT
        ON ORDERED.pay_id = PAYMENT.pay_id
        INNER JOIN car
        ON ORDERED.car_no = car.car_no
        order by ORDERED.Order_ID DESC
        ''')
        return orderDetails

    @ staticmethod
    def OrderIdExists(id):
        connection = s.connect("carSystem.db")
        cursor = connection.cursor()
        OrderCountList = cursor.execute(
            f"SELECT COUNT(*) FROM Ordered WHERE Order_ID = {id}").fetchone()
        return int(''.join([str(n) for n in OrderCountList])) == 1

    @ staticmethod
    def returnORDERED():
        connection = s.connect("carSystem.db")
        cursor = connection.cursor()
        ORDERED = cursor.execute("SELECT * from ORDERED")
        return ORDERED

    @ staticmethod
    def CreateTablePayment():
        connection = s.connect("carSystem.db")
        cursor = connection.cursor()
        cursor.execute('''
        CREATE TABLE PAYMENT
    (
        pay_id                INTEGER PRIMARY KEY AUTOINCREMENT,
        pay_number            VARCHAR (15),
        customer_id           INT NOT NULL,
        FOREIGN KEY(customer_id) REFERENCES CUSTOMERS(customer_id) on delete cascade
    )
        ''')

        connection.commit()
        connection.close()

    # @staticmethod
    # def InsertIntoPayment(number, customer_id): #where customer_id = 1 last row id only
    #     connection = s.connect('carSystem.db')
    #     cursor = connection.cursor()
    #     cursor.execute("pragma foreign_keys=on")
    #     cursor.execute("BEGIN TRANSACTION")
    #     cursor.execute("SAVEPOINT restart_from_payment")
    #     try:
    #         cursor.execute(f'''
    #         insert into PAYMENT (pay_number, customer_id)
    #         select '{number}', '{customer_id}'
    #         where not EXISTS (SELECT 1 from PAYMENT p where (p.customer_id <> {customer_id} or p.customer_id = {customer_id}) and p.pay_number = '{number}')
    #         ''')
    #         already = cursor.execute(f'''
    #         SELECT 'already'
    #         where EXISTS (SELECT 1 from PAYMENT p where p.customer_id <> {customer_id} and p.pay_number = '{number}')  
    #         ''')
    #         connection.commit()
    #     except:
    #         connection.rollback()
    #     cursor2 = connection.cursor()
    #     pay_id = cursor2.execute(f"SELECT pay_id from payment where pay_number = '{number}' and customer_id = {customer_id} limit 1")

    #     return already, pay_id

    @staticmethod
    def insertIntoPaymentThenOrders(number, customer_id, carno, quantity, pay_amount):
        connection = s.connect('carSystem.db')
        # cursor = connection.cursor()
        connection.execute("pragma foreign_keys=on")
        connection.execute("BEGIN TRANSACTION")
        try:
            connection.execute(f'''
            insert into PAYMENT (pay_number, customer_id)
            select '{number}', '{customer_id}'
            where not EXISTS (SELECT 1 from PAYMENT p where (p.customer_id <> {customer_id} or p.customer_id = {customer_id}) and p.pay_number = '{number}')
            ''')
            already = connection.execute(f'''
            SELECT 'already'
            where EXISTS (SELECT 1 from PAYMENT p where p.customer_id <> {customer_id} and p.pay_number = '{number}')  
            ''')
            connection.commit()
            # cursor2 = connection.cursor()
            pay_id = connection.execute(f"SELECT pay_id from payment where pay_number = '{number}' and customer_id = {customer_id} limit 1")
            StorePay_id = pay_id.fetchone()
            StoreAlready = already.fetchone()
            
            if StoreAlready == None:
                # cursor2 = connection.cursor()
                connection.execute("pragma foreign_keys=on")
                connection.execute('''
                INSERT INTO ORDERED(customer_id,car_no,quantity,pay_id, pay_amount) VALUES
                (?, ?, ?, ?, ?)
                ''', (customer_id, carno, quantity, StorePay_id[0], pay_amount))
                connection.commit()
            return StoreAlready, StorePay_id
        except s.Error as e:
            print(e.with_traceback)
            connection.rollback()

    @ staticmethod
    def CreateTableReviews():
        connection = s.connect("carSystem.db")
        cursor = connection.cursor()
        cursor.execute('''
        CREATE TABLE Reviews
    (
        review_id             INTEGER PRIMARY KEY AUTOINCREMENT,
        review_rate           DECIMAL (2,2) NOT NULL,
        review_description    VARCHAR (500) NOT NULL,
        Order_ID              int NOT NULL UNIQUE,
        FOREIGN KEY (Order_ID) REFERENCES ORDERED(Order_ID) ON DELETE CASCADE
    )
        ''')

        connection.commit()
        connection.close()
    @staticmethod
    def InsertIntoReviews(rate, revDesc, ord_id):
        connection = s.connect("carSystem.db")
        cursor = connection.cursor()
        cursor.execute("pragma foreign_keys=on")
        cursor.execute("BEGIN TRANSACTION")
        try:
            cursor.execute('''
            INSERT INTO Reviews(review_rate, review_description, Order_ID) VALUES
            (?, ?, ?)
            ''', (rate, revDesc, ord_id))
            connection.commit()
        except s.IntegrityError as error:
            print("Can't insert more reviews for 1 customer", error)
            connection.close()
            return False
        except s.Error as error:
            print("There is a problem while insertion, rolling back.", error)
            connection.rollback()
        # connection.commit()
        # lastId = cursor.lastrowid
        connection.close()
        return True
        # return lastId

    @staticmethod
    def returnAllReviewsOfcar_noWithJoins(car_no):
        connection = s.connect("carSystem.db")
        cursor = connection.cursor()
        reviews = cursor.execute(f'''
            SELECT c.first_name, c.last_name, r.review_rate, r.review_description from Reviews r
            inner join Ordered o
            on o.Order_Id = r.Order_Id
            INNER join Customers c
            on o.customer_id = c.customer_id
            inner join car f
            on o.car_no = f.car_no
            where f.car_no = '{car_no}'
        ''')
        return reviews

    @staticmethod
    def returnAllReviewsRatesAndcar_nos():
        connection = s.connect("carSystem.db")
        cursor = connection.cursor()
        reviews = cursor.execute(f'''
            SELECT f.car_no, avg(r.review_rate), count(*) from Reviews r
            inner join Ordered o
            on o.Order_Id = r.Order_Id
            INNER join Customers c
            on o.customer_id = c.customer_id
            inner join car f
            on o.car_no = f.car_no
            GROUP by f.car_no
        ''')
        return reviews

    @staticmethod
    def returnReviewsOfcar_noWithJoins(car_id):
        connection = s.connect("carSystem.db")
        cursor = connection.cursor()
        reviews = cursor.execute(f'''
            SELECT avg(r.review_rate), count(*) from Reviews r
            inner join Ordered o
            on o.Order_Id = r.Order_Id
            INNER join Customers c
            on o.customer_id = c.customer_id
            inner join car f
            on o.car_no = f.car_no
            GROUP by f.car_no
            having f.car_no = '{car_id}'
        ''')
        return reviews

    @staticmethod
    def carsFilterByOrderRatings():
        connection = s.connect("carSystem.db")
        cursor = connection.cursor()
        cars = cursor.execute('''
            SELECT f.car_no, f.car_image, f.car_price,f.car_title, f.car_description, f.admin_id
            from car f left join Ordered o
            on f.car_no = o.car_no
            left join Reviews r
            on r.Order_Id = o.Order_Id
            group by f.car_no
            order by avg(review_rate) desc;
        ''')
        return cars

    @ staticmethod
    def returnTable(table):
        connection = s.connect("carSystem.db")
        cursor = connection.cursor()
        tableTuples = cursor.execute(f"SELECT * from {table}")
        return tableTuples

    @staticmethod
    def testing(number,customer_id):
        connection = s.connect("carSystem.db")
        cursor = connection.cursor()
        cursor.execute('''
        INSERT INTO Payment(pay_number, customer_id) VALUES
        (?, ?)
        ''', (number, customer_id))
        connection.commit()
        pay_id = cursor.execute(f"SELECT pay_id from payment where pay_number = '{number}' and customer_id = '{customer_id}'")
        cursor2 = connection.cursor()
        count = cursor2.execute("select count(*) from payment")
        return pay_id, count

    # @staticmethod
    # def testing2(number,customer_id):
    #     connection = s.connect("carSystem.db")
    #     cursor = connection.cursor()
    #     cursor.execute(f'''
    #     insert into PAYMENT (pay_number, customer_id)
    #     select {number}, {customer_id}
    #     where not EXISTS (SELECT 1 from PAYMENT p where (p.customer_id <> {customer_id} or p.customer_id = {customer_id}) and p.pay_number = {number})
    #     ''')
    #     already = cursor.execute(f'''
    #     SELECT 'User with this  already exists'
    #     where EXISTS (SELECT 1 from PAYMENT p where p.customer_id <> {customer_id} and p.pay_number = {number})  
    #     ''')
    #     connection.commit()
    #     cursor2 = connection.cursor()
    #     pay_id = cursor2.execute(f"SELECT pay_id from payment where pay_number = {number} and customer_id = {customer_id} limit 1")

    #     return already, pay_id

try:
    Database.returnAllReviewsRatesAndcar_nos()
    Database.CreateTableReviews()
except:
    pass

# import sqlite3 as s

# connection = s.connect("carSystem.db")
# cursor = connection.cursor()

# # Get schema of 'Ordered' table
# cursor.execute('PRAGMA table_info(Ordered)')
# schema = cursor.fetchall()

# # Print schema info
# print("Schema of 'Ordered' table:")
# for column in schema:
#     # column format: (cid, name, type, notnull, dflt_value, pk)
#     print(f"Column: {column[1]}, Type: {column[2]}, Not Null: {bool(column[3])}, Primary Key: {bool(column[5])}")

# connection.close()
