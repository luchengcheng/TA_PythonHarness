import pymssql


def conn(serverName, userName, password, db):
    connect = pymssql.connect(serverName, userName, password, db)  # 服务器名,账户,密码,数据库名
    if connect:
        print("connect db successfully!")
    return connect


def execSQL(sqlQuery, connect):
    cursor = connect.cursor()
    try:
        cursor.execute(sqlQuery)
        results = cursor.fetchall()
        print(results)
    except:
        print("some error in db")
    connect.close()


def main():
    serverName = '(local)'
    userName = 'sa'
    password = 'pass'
    db = 'MSQ46906_afterUpgrade'
    sqlQuery = "select * from version"
    connect = conn(serverName, userName, password, db)
    execSQL(sqlQuery, connect)


if __name__ == '__main__':
    main()
