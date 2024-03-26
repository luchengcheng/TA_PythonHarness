

def conn(serverName, userName, password, db):
    connect = pymssql.connect(serverName, userName, password, db)  # 服务器名,账户,密码,数据库名
    if connect:
        print("连接成功!")
    return connect


def main():
    serverName = '(local)'
    userName = 'sa'
    password = 'pass'
    db = 'MSQ46906_afterUpgrade'
    conn(serverName, userName, password, db)


if __name__ == '__main__':
    main()