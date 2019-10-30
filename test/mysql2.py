from database.mysql import Database as MySQL

db_config = {'host': 'localhost',
             'user': 'root',
             'password': '123456',
             'db': 'pj'
             }

db = MySQL(db_config)

print(db.get_jname_by_id(-1))
