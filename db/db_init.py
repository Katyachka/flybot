import sqlite3


DB_NAME = "fly-bot.sql"


# Ініціалізація бази даних


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('CREATE TABLE IF NOT EXISTS userinfo ('
                   'id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,'
                   'name varchar(100) NOT NULL,'
                   'surname varchar(100) NOT NULL,'
                   'gender char NOT NULL,'
                   'phone varchar(13) NOT NULL,'
                   'email varchar(200) NOT NULL'
                   ')')

    cursor.execute('CREATE TABLE IF NOT EXISTS users ('
                   'id INTEGER PRIMARY KEY NOT NULL,'
                   'userInfoId INTEGER REFERENCES userinfo(id),'
                   'saveInfo BOOLEAN'
                   ')')

    cursor.execute('CREATE TABLE IF NOT EXISTS plane ('
                   'id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,'
                   'model varchar(100) NOT NULL,'
                   'passengers INTEGER NOT NULL,'
                   'layout varchar NOT NULL'
                   ')')

    cursor.execute('CREATE TABLE IF NOT EXISTS flight ('
                   'id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,'
                   'planeId INTEGER NOT NULL REFERENCES plane(id),'
                   'departure varchar(100) NOT NULL,'
                   'arrival varchar(100) NOT NULL,'
                   'departure_date_time DATETIME NOT NULL,'
                   'arrival_date_time DATATIME NOT NULL,'
                   'duration FLOAT NOT NULL,'
                   'cost_base FLOAT NOT NULL,'
                   'cost_regular FLOAT NOT NULL,'
                   'cost_plus FLOAT NOT NULL' 
                   ')')

    cursor.execute("CREATE TABLE IF NOT EXISTS seat ("
                   "id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,"
                   "number varchar(10) NOT NULL,"
                   "userInfoId INTEGER NOT NULL REFERENCES userinfo(id),"
                   "flightId INTEGER NOT NULL REFERENCES flight(id)"
                   ")")

    cursor.execute('CREATE TABLE IF NOT EXISTS ticket ('
                   'id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,'
                   'flightId INTEGER NOT NULL REFERENCES flight(id),'
                   'planeId INTEGER NOT NULL REFERENCES plane(id),'
                   'seatId INTEGER NOT NULL REFERENCES seat(id)'
                   ')')

    cursor.execute('CREATE TABLE IF NOT EXISTS user_ticket ('
                   'id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,'
                   'userId INTEGER NOT NULL REFERENCES users(id),'
                   'ticketId INTEGER NOT NULL REFERENCES ticket(id)'
                   ')')

    conn.commit()

    cursor.close()
    conn.close()