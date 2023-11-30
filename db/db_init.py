import sqlite3
from datetime import datetime, timedelta
from decimal import Decimal

from models.Plane import Plane

DB_NAME = "fly-bot.sql"


departure = {
    1: "Варшава",
    2: "Берлін",
    3: "Краків",
    4: "Париж",
    5: "Барселона",
    6: "Дублін",
    7: "Варшава",
    8: "Дублін",
    9: "Харків",
    10: "Берлін"
}

arrival = {
    1: "Берлін",
    2: "Варшава",
    3: "Париж",
    4: "Краків",
    5: "Дублін",
    6: "Барселона",
    7: "Дублін",
    8: "Варшава",
    9: "Берлін",
    10: "Харків"
}

departure_date_time = {
    1: datetime(year=2023, month=12, day=16, hour=12, minute=15),
    2: datetime(year=2023, month=12, day=18, hour=8, minute=10),
    3: datetime(year=2023, month=12, day=17, hour=6, minute=00),
    4: datetime(year=2023, month=12, day=20, hour=17, minute=30),
    5: datetime(year=2023, month=12, day=24, hour=14, minute=00),
    6: datetime(year=2023, month=12, day=25, hour=11, minute=10),
    7: datetime(year=2023, month=12, day=26, hour=20, minute=20),
    8: datetime(year=2023, month=12, day=27, hour=8, minute=00),
    9: datetime(year=2023, month=12, day=28, hour=7, minute=45),
    10: datetime(year=2023, month=12, day=29, hour=18, minute=35),
}

duration = {
    1: 1.2,
    2: 1.2,
    3: 2.20,
    4: 2.20,
    5: 2.45,
    6: 2.45,
    7: 5.10,
    8: 5.10,
    9: 4.35,
    10: 4.35
}

arrival_date_time = {
    1: departure_date_time[1] + timedelta(hours=int(duration[1]), minutes=int(Decimal(f"{Decimal(f"{duration[1]}") - int(duration[1])}") * 100)),
    2: departure_date_time[2] + timedelta(hours=int(duration[2]), minutes=int(Decimal(f"{Decimal(f"{duration[2]}") - int(duration[2])}") * 100)),
    3: departure_date_time[3] + timedelta(hours=int(duration[3]), minutes=int(Decimal(f"{Decimal(f"{duration[3]}") - int(duration[3])}") * 100)),
    4: departure_date_time[4] + timedelta(hours=int(duration[4]), minutes=int(Decimal(f"{Decimal(f"{duration[4]}") - int(duration[4])}") * 100)),
    5: departure_date_time[5] + timedelta(hours=int(duration[5]), minutes=int(Decimal(f"{Decimal(f"{duration[5]}") - int(duration[5])}") * 100)),
    6: departure_date_time[6] + timedelta(hours=int(duration[6]), minutes=int(Decimal(f"{Decimal(f"{duration[6]}") - int(duration[6])}") * 100)),
    7: departure_date_time[7] + timedelta(hours=int(duration[7]), minutes=int(Decimal(f"{Decimal(f"{duration[7]}") - int(duration[7])}") * 100)),
    8: departure_date_time[8] + timedelta(hours=int(duration[8]), minutes=int(Decimal(f"{Decimal(f"{duration[8]}") - int(duration[8])}") * 100)),
    9: departure_date_time[9] + timedelta(hours=int(duration[9]), minutes=int(Decimal(f"{Decimal(f"{duration[9]}") - int(duration[9])}") * 100)),
    10: departure_date_time[10] + timedelta(hours=int(duration[10]), minutes=int(Decimal(f"{Decimal(f"{duration[10]}") - int(duration[10])}") * 100)),
}

cost_base = {
    1: 30,
    2: 30,
    3: 45,
    4: 45,
    5: 50,
    6: 50,
    7: 62,
    8: 62,
    9: 60,
    10: 60
}


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

    fill_planes()
    fill_flight()


def fill_planes():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM plane')

    all = cursor.fetchall()

    if not all:
        cursor.execute(f'INSERT INTO plane (model, passengers, layout) '
                       f'VALUES (?, ?, ?)',
                       ("Boing 737 800", 189, "boing_737_800.png"))

        cursor.execute(f'INSERT INTO plane (model, passengers, layout) '
                       f'VALUES (?, ?, ?)',
                       ("Airbus A320", 180, "airbus_a320.png"))

        cursor.execute(f'INSERT INTO plane (model, passengers, layout) '
                       f'VALUES (?, ?, ?)',
                       ("Cessna 172", 4, "cessna_172.png"))

        cursor.execute(f'INSERT INTO plane (model, passengers, layout) '
                       f'VALUES (?, ?, ?)',
                       ("Boing 737 800", 189, "boing_737_800.png"))

        cursor.execute(f'INSERT INTO plane (model, passengers, layout) '
                       f'VALUES (?, ?, ?)',
                       ("Airbus A320", 180, "airbus_a320.png"))

        cursor.execute(f'INSERT INTO plane (model, passengers, layout) '
                       f'VALUES (?, ?, ?)',
                       ("Cessna 172", 4, "cessna_172.png"))

        cursor.execute(f'INSERT INTO plane (model, passengers, layout) '
                       f'VALUES (?, ?, ?)',
                       ("Boing 737 800", 189, "boing_737_800.png"))

        cursor.execute(f'INSERT INTO plane (model, passengers, layout) '
                       f'VALUES (?, ?, ?)',
                       ("Airbus A320", 180, "airbus_a320.png"))

        cursor.execute(f'INSERT INTO plane (model, passengers, layout) '
                       f'VALUES (?, ?, ?)',
                       ("Cessna 172", 4, "cessna_172.png"))

        cursor.execute(f'INSERT INTO plane (model, passengers, layout) '
                       f'VALUES (?, ?, ?)',
                       ("Airbus A320", 180, "airbus_a320.png"))

        conn.commit()

    cursor.close()
    conn.close()


def fill_flight():
    minutes = int(Decimal(f"{Decimal(f"{duration[1]}") - int(duration[1])}") * 100)
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM flight')

    flights = cursor.fetchall()

    if not flights:
        cursor.execute('SELECT * FROM plane')

        planes = cursor.fetchall()
        plane_models = [Plane.from_tuple(plane) for plane in planes]

        index = 1
        for plane in plane_models:
            cursor.execute(f'INSERT INTO flight (planeId, departure, arrival, departure_date_time, arrival_date_time,'
                           f'duration, cost_base, cost_regular, cost_plus) '
                       f'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                       (plane.id, departure[index], arrival[index], departure_date_time[index], arrival_date_time[index],
                        duration[index], cost_base[index], 15, 25))
            index += 1

        conn.commit()
    cursor.close()
    conn.close()
