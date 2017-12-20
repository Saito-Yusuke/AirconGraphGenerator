## libraries
import sys
import pyodbc
import matplotlib.pyplot as plt

## initial setting
server = 'ECOLOGDB2016'
database = 'ECOLOGDBver3'
username = 'TOMMYLAB\saito'
password = ''

##DB connectionを定義
def dbConnection(sv=server, db=database, un=username, pw=password):
    # Windows認証
    con = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server}; SERVER='+sv+'; DATABASE='+db+'; Trusted_Connection=yes')
    return con

##まずはトリップを取ってくる
getTripQuery = "select TRIP_ID, START_TIME, END_TIME from TRIPS_LINKS_LOOKUP2 where TRIP_ID in (select distinct TRIP_ID from LEAFSPY_RAW2)"
cur = dbConnection().cursor()
cur.execute(getTripQuery)
tripRows = cur.fetchall()

for tripRow in tripRows:
    query = "select datediff(second, TRIPS_LINKS_LOOKUP2.START_TIME, LEAFSPY_RAW2.DATETIME) as ELAPSED_TIME, AC_PWR_250W * 250.0 / 1000.0 as AC_PWR_kW "\
    +"from LEAFSPY_RAW2 inner join TRIPS_LINKS_LOOKUP2 on LEAFSPY_RAW2.TRIP_ID = TRIPS_LINKS_LOOKUP2.TRIP_ID where TRIPS_LINKS_LOOKUP2.TRIP_ID = " + str(tripRow[0])

    cur.execute(query)
    result = list(cur.fetchall())

    elapsedTime = []
    acPwr = []

    for i in range(len(result)):
        elapsedTime.append(result[i][0])
        acPwr.append(result[i][1])

    plt.figure()
    plt.plot(elapsedTime, acPwr, label = "TRIP ID: "+ str(tripRow[0]))
    plt.legend()
    plt.title("TRIP ID: " + str(tripRow[0])+ " (" + tripRow[1].strftime('%Y-%m-%d %H:%M:%S') + " - " + tripRow[2].strftime('%Y-%m-%d %H:%M:%S') + ")")
    plt.xlabel("ELAPSED TIME [s]")
    plt.ylabel("AC POWER from LEAF SPY [kW]")
    plt.ylim(0, 6.0)

    filename = tripRow[1].strftime('%Y%m%d%H%M%S') + ".png"
    plt.savefig(filename)
    plt.close()
    print("TRIP ID: " + str(tripRow[0]) + " Graph has been saved.")
    elapsedTime.clear()
    acPwr.clear()

dbConnection().commit()
dbConnection().close()
print("\n正常終了. ")