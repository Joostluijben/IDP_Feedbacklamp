import mysql.connector
cnx = mysql.connector.connect(user='root', password='idp',
                              host='127.0.0.1',
                              database='idp_project')
cnx.close()
