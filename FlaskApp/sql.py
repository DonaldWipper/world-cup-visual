import MySQLdb
 
'''
db = MySQLdb.connect(host="localhost",    # your host 
                     user="root",         # username
                     passwd="111",  # password
                     db="tinderdb")
 '''
# Create a Cursor object to execute queries.
'''
#cur = db.cursor()

str = "CREATE TABLE IF NOT EXISTS PROFILES ("  
str += "id varchar(50), "
str += "id_pair varchar(50), " 
str = str + "name varchar(50), " 
str = str + "birth_date datetime, " 
str = str + "distance_mi int, " 
str = str + "jobs text, " 
str = str + "bio text, " 
str = str + "text text, "
str = str + "common_interests text, "
str = str + "profile_instagram text, "
str = str + "profile_vk varchar(50), "
str = str + "profile_fb varchar(50), "
str += "profile_photo1 text,"
str += "profile_photo2 text,"
str += "profile_photo3 text,"
str += "profile_photo4 text,"
str += "profile_photo5 text,"
str += "profile_photo6 text,"
str += "inst_photo1  text,"
str += "inst_photo2  text,"
str += "inst_photo3  text,"
str += "inst_photo4  text,"
str += "inst_photo5  text,"
str += "inst_photo6  text,"
str += "PRIMARY KEY (id) ); "
--DateOfAdded datetime
--text_json text

#str = 'ALTER database tinderdb CHARACTER SET utf8 COLLATE utf8_general_ci'
str = 'SELECT 1 FROM PROFILES WHERE id = '5a805b6a12c0389c16f16209'

print(str)
# Select data from table using SQL query.
cur.execute(str)
 '''


class database:
    def __init__(self, host_, user_, passwd_, db_):
        self.host = host_
        self.user = user_
        self.passwd = passwd_
        self.db_ = db_
        self.db = MySQLdb.connect(host=host_,    # your host 
                     user=user_,                 # username
                     passwd=passwd_,             # password
                     db=db_)                     # name of the database
        self.db.set_character_set('utf8mb4')
        
    def __repr__(self):
        return "DB(host='%s', name='%s')" % (self.host, self.name)
        
    def __str__(self):
        return "<%s dv named %s>" % (self.host, self.name)
        
    def insert_values (self, table_name, headers, values):
        cur = self.db.cursor()
        size = len(headers)
        if size != len(values):
            return -1
        query = 'INSERT INTO ' +  table_name +  " ("
        last = size
        i = 0
        for header in headers:
            i += 1
            if i != last:
                query += header + ","
            else:
                query =  query + header + ")"
        query += " VALUES ("
        i = 0
        for value in values:
            i += 1
            if value == None or value == '':
                value = 'NULL'       
            if i != last: 
                if value != 'NULL': 
                    query = query + "'" + str(value).replace("'", "") + "',"
                else:
                    query = query +  str(value).replace("'", "") + ","
            else:
                if value != 'NULL': 
                    query = query + "'" + str(value).replace("'", "") + "')"
                else:
                    query = query  + str(value).replace("'", "") + ")"
        cur.execute(query)
        self.db.commit()       

    def show_top(self, table_name, count):
        cur = self.db.cursor()
        query = 'SELECT * FROM ' + table_name + ' limit ' + str(count)  
        cur.execute(query)
        for row in cur.fetchall() :
            for field in row:
                print (field, end= " | ")
            print("\n") 
     
    def check_if_exists(self, table_name, column, value):
        res = -1
        cur = self.db.cursor()
        query = 'SELECT id FROM ' + table_name + ' WHERE '+ column  + " = '" + str(value).replace("'", "") + "'"
        print(query)
        cur.execute(query)
        for row in cur.fetchall() :
            for field in row:
                return 1
        return res
 
    def delete_elem(self, table_name, column, value):
        res = -1
        cur = self.db.cursor()
        query = 'DELET FROM ' + table_name + ' WHERE '+ column  + " = '" + str(value).replace("'", "") + "'"
        print(query)
        cur.execute(query)
        self.db.commit()  

 
    def search_by_values(self, table_name, column, value, precise = False):
        res = -1
        cur = self.db.cursor()
        cur.execute(query)
        query = 'SELECT * FROM ' + table_name + ' WHERE '+ column  + " = '" + str(value).replace("'", "") + "'"
        for row in cur.fetchall() :
            for field in row:
                return 1
            print() 
        return res
        self.db.commit() 
   
    
    def get_count(self, table_name):
        cur = self.db.cursor()
        query = 'SELECT COUNT(*) FROM ' + table_name   
        cur.execute(query)
        for row in cur.fetchall() :
            for field in row:
                print (field, end = " ")
            print() 
        self.db.commit()
 
    def drop_table(self, table_name):
        cur = self.db.cursor()
        query = 'DROP TABLE ' + table_name   
        cur.execute(query)
        self.db.commit() 
                  
db = database("localhost", "root", "111", "tinderdb")   
#db.check_if_exists("PROFILES", "id", "6adbb44d-be67-4e59-b8db-84982829a370")
#db.drop_table("PROFILES")
#db.insert_values("PROFILES", ("id", "name", "bio"), ("3", "al", "5j5j5k"))
#db.insert_values("PROFILES", ("id", "name", "bio"), ("2", "al2", "rj4j"))
#db.show_top("PROFILES", 100)
db.get_count("PROFILES")
    









