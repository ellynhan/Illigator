import mysql.connector
isTableEmpty = False

mydb = mysql.connector.connect(
    host="host",
    user="user",
    password="password"
)

mycursor = mydb.cursor()


def create_database(db_name):
    is_db_exist = False
    mycursor.execute("SHOW DATABASES")
    for name in mycursor:
        if name[0] == db_name:
            is_db_exist = True

    if not is_db_exist:
        mycursor.execute(f"CREATE DATABASE {db_name}")


def create_table(db_name, table_name, sql):
    is_table_exist = False
    mycursor.execute(f"USE {db_name}")
    mycursor.execute("SHOW TABLES")
    for tables in mycursor:
        if tables[0] == table_name:
            is_table_exist = True

    if not is_table_exist:
        mycursor.execute(f"CREATE TABLE {table_name} {sql}")


def insert_to_table(db_name, table_name, sql):
    mycursor.execute(f"USE {db_name}")
    mycursor.execute(f"INSERT INTO {table_name} {sql}")
    mydb.commit()


def select_from_table(db_name, table_name, attr_target, option_sql):
    mycursor.execute(f"USE {db_name}")
    mycursor.execute(f"SELECT {attr_target} FROM {table_name} {option_sql}")
    result = mycursor.fetchall()
    return result
