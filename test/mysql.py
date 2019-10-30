import pymysql

db_config = {'host': 'localhost',
             'user': 'root',
             'password': '123456',
             'db': 'pj'
             }
'''
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='123456',
                             db='pj')
                             '''

connection = pymysql.connect(**db_config)

try:
    with connection.cursor() as cursor:
        query = """
                SELECT *
                FROM jid_name
                limit 10;
                """
        ret = cursor.execute('SELECT * FROM jid_name limit 10;');
        result = cursor.fetchall()
finally:
    connection.close()

print(result)
