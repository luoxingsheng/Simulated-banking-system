#coding=UTF-8
import pymysql

"""
初始化数据库连接
用户名 密码 端口 数据库 表名
"""
host = 'localhost'  # 主机名
user = 'root'  # 用户名
password = 'root'  # 密码
port = 3306  # 端口
database = 'lxs'  # 数据库
global conn
conn = pymysql.Connect(host=host, port=port, user=user, password=password, db=database, charset='utf8')

def add(sql):
    """增加语句"""
    global conn
    result = True
    try:
        conn = pymysql.Connect(host=host, port=port, user=user, password=password, db=database, charset='utf8')
        cur = conn.cursor()
        print("SQL语句为：", sql)
        cur.execute(sql)
        conn.commit()
        print("数据插入成功！")
        result = True
    except Exception as e:
        print("操作失败,失败信息为：", e)
        conn.rollback()  # 回滚
        result = False
    finally:
        conn.close()
        return result


def delete(sql):
    """删除语句"""
    global conn
    result = True
    try:
        conn = pymysql.Connect(host=host, port=port, user=user, password=password, db=database, charset='utf8')
        cur = conn.cursor()
        print("SQL语句为：", sql)
        cur.execute(sql)
        conn.commit()
        print("数据删除成功！")
        result = True
    except Exception as e:
        print("操作失败，失败信息为：", e)
        conn.rollback()
        result = False
    finally:
        return result
        conn.close()


def update(sql):
    """修改语句"""
    global conn
    result = True
    try:
        conn = pymysql.Connect(host=host, port=port, user=user, password=password, db=database, charset='utf8')
        cur = conn.cursor()
        print("SQL语句为：", sql)
        cur.execute(sql)
        conn.commit()
        print("更新数据成功！")
        result = True
    except Exception as e:
        result = False
        print("操作失败，失败信息为：", e)
        conn.rollback()
    finally:
        return result
        conn.close()


def query(sql):
    """查询语句"""
    global conn
    result = ()
    try:
        conn = pymysql.Connect(host=host, port=port, user=user, password=password, db=database, charset='utf8')
        cur = conn.cursor()
        print("SQL语句为：", sql)
        cur.execute(sql)
        result = cur.fetchall()
        print("数据查询成功！")
    except Exception as e:
        print("操作失败，失败信息为：", e)
    finally:
        return result
        conn.close()
