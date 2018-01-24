import MySQLdb
def connection():
    conn = MySQLdb.connect(host="host",
                           user="user",
                           passwd="pass",
                           db="db")
    c=conn.cursor()

    return c,conn