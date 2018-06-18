import MySQLdb
import json
import urllib
import csv

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
#get settings
def read_params(fn): 
    d ={} 
    try:
        with open(fn, 'r',encoding="utf-8") as file: 
            d = json.load(file) 
    except FileNotFoundError:
         print ("Error. Can't find file " + fn)
         d = {}
    return d 





class database:
    def __init__(self, host_, user_, passwd_, db_):
        self.host = host_
        self.user = user_
        self.passwd = passwd_
        self.db_ = db_
        self.db = MySQLdb.connect(host=host_,    # your host 
                     user=user_,                 # username
                     passwd=passwd_,             # password
                     db=db_
                     

                     )                     # name of the database
        self.db.set_character_set('utf8mb4')
        
    def __repr__(self):
        return "DB(host='%s', name='%s')" % (self.host, self.name)
        
    def __str__(self):
        return "<%s dv named %s>" % (self.host, self.name)
    
    def get_dbs_info(self):
        cur = self.db.cursor()
        query = 'SHOW DATABASES;'
        cur.execute(query)      

    def create_table(self, dic, table_name):
        cur = self.db.cursor()
        query = 'CREATE TABLE IF NOT EXISTS ' +  table_name +  " ("
        length = len(dic)
        i = 0
        for value in dic:
            query += value + " " + dic[value]  
            if i != length - 1:
                query += ", "
            else:
                query += ") "
            i += 1
        print(query)
        cur.execute(query)
        self.db.commit() 
    

    def insertDataIntoTableFromCSV(self, name, table_name, key_field = None):
        #csvfile = requests.get(name).csv
        csvfile = open(name)
        reader = csv.DictReader(csvfile)
        for row in reader:   
            print(row)  
            if key_field != None:
                if self.check_if_exists(table_name, key_field, row[key_field]) == -1:
                    self.insert_values(table_name, row.keys(), row.values())
                else:
                    return False  
            else:
                self.insert_values(table_name, row.keys(), row.values()) 
        return True

    def getDictFromQueryRes(self, table_name, condition = None, result_fields = None):
        #csvfile = requests.get(name).csv
        cur = self.db.cursor(MySQLdb.cursors.DictCursor)

        query = "SELECT "
        if result_fields == None:
            query += "*"
        else:
            for r  in result_fields:
                query += r + ","
            query += "+"
            query = query.strip().replace(",+", "")
        query += " FROM " + table_name
        if condition != None:
            query += " WHERE "
            for q in condition:
                query += " " + str(q) + " = " + str(condition[q]) + " AND"
            query += "="
            query = query.strip().replace("AND=", "")
        print(query)
        cur.execute(query)
        return list (cur.fetchall())
    
    def updateTableFromConditions(self, table_name, condition = None, update_fields = None):
        #csvfile = requests.get(name).csv
        cur = self.db.cursor(MySQLdb.cursors.DictCursor)

        query = "UPDATE " + table_name
        if update_fields == None:
            return
        else:
            query += " SET "
            for r in update_fields:
                s = str(r) + " = '" + str(update_fields[r]) + "',"
                if r not in ["date", "status"]:
                    s = s.strip().replace("'", "")
                query += s 
            query += "+"
            query = query.strip().replace(",+", "")
        if condition != None:
            query += " WHERE "
            for q in condition:
                qr = " " + str(q) + " = '" + str(condition[q]) + "' AND "
                if q not in ["date", "status"]:
                    qr = qr.replace("'", "")
                query += qr 
            query += "="
            query = query.strip().replace("AND =", "")
        print(query)
        cur.execute(query)
        self.db.commit() 
   
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
        print(query)
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
        query = 'DELETE FROM ' + table_name + ' WHERE '+ column  + " = '" + str(value).replace("'", "") + "'"
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


#settings  = read_params("settings2.json")
#print(settings['sql_host'])
#url = 'mysql://b1df3776b2b56c:8b4b450a@us-cdbr-iron-east-04.cleardb.net/heroku_0c1d0ea4e380413?reconnect=true'
#result=  urllib.urlparse(url)

#db = database(settings['sql_host'],  settings['sql_user'],  settings['sql_passwd'], settings['sql_db'])   


#dict_groups = {"stadium":"text","city":"text","homeTeam":"text","awayTeam":"text","shortHomeTeam":"text","shortAwayTeam":"text"} 
#db.create_table(dict_groups, "games_fifa")
#db.insertDataIntoTableFromCSV("games_wc.csv", "games_fifa")


#print(db.getDictFromQueryRes("teams_wc"))
#dict_teams = {"id":"int", "name":"text","shortName":"text", "crestUrl":"text", "squadMarketValue":"text"}
#dict_teams = #{"goalsAgainst":"int","points":"int","goals":"int","teamId":"int","crestURI":"text","rank":"int","team":"text","playedGames":"int","group":"text","goalDifference":"int"}
#dict_games = {"competitionId":"int", "date":"text" ,"status":"text", "homeTeamId":"text", "awayTeamId":"text", "goalsHomeTeam":"text", "goalsAwayTeam":"text", "CityId":"int"}
#db.create_table(dict_games, "games")
#db.insertDataIntoTableFromCSV("matches2.csv", "games")
#dict_tournaments = {"lastUpdated":"text","numberOfTeams":"int","league":"text","caption":"text","id":"int","year":"int","numberOfGames":"int","numberOfMatchdays":"int","currentMatchday":"int"}
#db.create_table(dict_tournaments, "tournaments")
#db.insertDataIntoTableFromCSV("tournaments.csv", "tournaments")
#dict_places = {"id":"int","short_name":"text","stadium":"text","capacity":"int","city":"text"} 
#db.create_table(dict_places, "places")
#db.insertDataIntoTableFromCSV("places.csv", "places")


#dict_rounds = {"id":"int", "competitionId":"int", "title":"text", "start_at":"text", "end_at":"text"} 
#db.create_table(dict_rounds, "rounds")
#db.insertDataIntoTableFromCSV("rounds.csv", "rounds")

#dict_groups = {"id":"int", "title":"text", "competitionId":"text"} 
#db.create_table(dict_groups, "groups")
#db.insertDataIntoTableFromCSV("groups.csv", "groups")

#dict_stand = #{"goalsAgainst":"int","points":"int","goals":"int","teamId":"int","crestURI":"text","rank":"int","team":"text","playedGames":"int","group_":"text","goalDifference":"int", "CompetitionId":"int"}
#db.create_table(dict_stand, "standings")
#db.insertDataIntoTableFromCSV("standings.csv", "standings")


#competitionId,date,status,homeTeamId,awayTeamId,goalsHomeTeam,goalsAwayTeam
#378,1930-07-12T23:00:00Z,FINISHED,771,805,3,0


#dict_stages = {"id":"int","competitionId":"int","title":"text"}
#db.create_table(dict_stages, "stages")
#db.insertDataIntoTableFromCSV("stages.csv", "stages", "id")




#db.check_if_exists("PROFILES", "id", "6adbb44d-be67-4e59-b8db-84982829a370")
#db.drop_table("PROFILES")
#db.insert_values("PROFILES", ("id", "name", "bio"), ("3", "al", "5j5j5k"))
#db.insert_values("PROFILES", ("id", "name", "bio"), ("2", "al2", "rj4j"))
#db.show_top("PROFILES", 100)
#db.get_count("PROFILES")
    









