import pymysql

def scraper_insert(table, stock, strike, direction, date, entry_price):
    """inserts stock option information to primary databse based on table name"""
    HOST = # dabase endpoint
    USER = # databse admin username
    PASS = # databse admin password
    DATABASE = # name of database

    connection = pymysql.connect(host = HOST, user = USER, password=PASS, database= DATABASE)
    with connection:
        with connection.cursor() as cursor:
            sql = f"INSERT INTO `{table}` (`stock`, `strike`, `direction`, `exp_date`, `entry_price`) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (stock, int(strike), direction, date, float(entry_price)))
        connection.commit()

def scraper_add_exit(table, stock, strike, direction, date, exit_price):
    """inserts the exit price on an option to primary database based on table name"""
    HOST = # dabase endpoint
    USER = # databse admin username
    PASS = # databse admin password
    DATABASE = # name of database
    
    connection = pymysql.connect(host = HOST, user = USER, password=PASS, database= DATABASE)
    with connection:
        with connection.cursor() as cursor:
            sql = f"UPDATE `{table}` SET `exit_price`=%s WHERE `stock`=%s AND `strike`=%s AND `direction`=%s AND `exp_date`=%s"
            cursor.execute(sql, (float(exit_price), stock, int(strike), direction, date))
        connection.commit()
