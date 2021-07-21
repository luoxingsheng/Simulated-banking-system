#coding=UTF-8
import bank as bank
import mysql_tool as conn
from datetime import datetime
import email_tool as  email
import numpy as np
import re

def create_check_code():
    """生成一个六位的随机数"""
    check_codes = np.random.randint(0, 10, 6)
    check_str = ''
    for code in check_codes:
        check_str += str(code)
    return check_str

def email_format_check(email_str):
    """验证是否是QQ邮箱格式"""
    """
    QQ邮箱指QQ号+@qq.com结尾
　　 分析：1.QQ最短5位最长11位数
　　　　　 2.以@qq.com结尾
　　　　　　3.不能以0开头
    """
    str1 = '邮箱格式合法:'
    str2 = '邮箱格式不合法:'
    ex_email = re.compile(r'^[1-9][0-9]{4,10}@qq\.com')
    result = ex_email.match(email_str)
    if result:
        print(str1 + email_str)
    else:
        print(str2 + email_str)
    return result

def password_format_check(passwd):
    """用户密码格式验证"""
    result_passws = re.compile(r'^(?=.*\d)(?=.*[a-zA-Z]).{6,20}$')  # 必须包含大写或小写字母和数字的组合，可以使用特殊字符，长度在6-20之间
    # result_passws = re.compile(r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])[a-zA-Z0-9]{6,20}$')  # 必须包含大小写字母和数字的组合，不可以使用特殊字符，长度在6-20之间
    # result_passws = re.compile(r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,10}$')  # 必须包含大小写字母和数字的组合，可以使用特殊字符，长度在6-20之间

    result = False
    if not result_passws.match(passwd):
        print('密码格式错误')
        result = False
    else:
        print('密码格式正确')
        result = True
    return result

def register_check(username,password,email_str):
    """检查用户名是否重复，无重复时将注册信息写入数据库"""
    result = False
    sql = f"select username from user where username = '{username}'"
    res = conn.query(sql)
    if len(res) == 0:
        result = True
        sql = f"insert into user(username,password,email) values('{username}','{password}','{email_str}')"
        result = conn.add(sql)
    return result

def register():
    """注册流程验证"""
    email_str = input("请输入邮箱：")
    if email_str == 'q':
        main()
    if email_format_check(email_str):
        username = input("请输入用户名：")
        password = input('请输入密码: ')
        password_check = input("请再次输入密码：")
        if password == password_check:
            # 密码格式验证项目比较简单没必要
            # if not(password_format_check(password)):
            #     register()
            result = register_check(username, password, email_str)
            if result:
                print("注册成功！")
            else:
                print("用户名重复，注册失败！")
                register()
        else:
            print("两次密码不一致，请重新输入！")
            register()
    else:
        register()


def login_check(username,password):
    """登陆检查用户名密码是否正确，获取用户的id和balance"""
    str = f"select id,balance from user where username = '{username}' and password = '{password}'"
    result = conn.query(str)
    return result

def query_logs(user_id):
    """获取当前用户的操作日志"""
    sql = f"select datetime,summary,money,currency,balance from bank_log " \
          f"where user_id = '{user_id}'"
    result = list(conn.query(sql))
    for res in result:
        log = list(res)
        bank.operate_log.append(log)

def login():
    """登陆操作"""
    username = input("请输入用户名：")
    if username == 'q':
        main()
    password = input("请输入密码：")
    result = login_check(username,password)
    if len(result) == 1:
        bank.user_id = str(result[0][0])
        bank.user_balance = float(result[0][1])
        print("登陆成功")
        query_logs(bank.user_id)
        bank.main_menu()
    else:
        print("用户名或密码错误，请检查后重新登陆")
        login()

def check_email(username):
    """查询用户输入的邮箱地址是否正确"""
    sql = f"select email from user where username = '{username}'"
    result = conn.query(sql)
    if (len(result) > 0):
        return result[0][0]
    else:
        print("邮箱地址错误！")

def send_check_code(email_str):
    """发送验证码"""
    check_str = create_check_code()
    subject = "模拟银行系统重置密码"  # 主题
    content = f"重置密码，验证码为：{check_str}"  # 正文
    result = email.send_email(email_str,subject,content)
    if not(result):
        check_str = ''
    return check_str

def update_password(username,password):
    """修改密码"""
    sql = f"update user set password = '{password}' where username = '{username}'"
    result = conn.update(sql)
    return result

def reset_check_code(check_str,username,password):
    """重新验证验证码"""
    print(check_str)
    check_code = input("请输入重置邮件中的验证吗：")
    if check_code == check_str:
        result = update_password(username, password)
        if result:
            print("重置密码成功，请登陆！")
            login_menu()
        else:
            print("修改密码失败！")
            reset_password()
    else:
        print("验证码输入错误，请确认后重新输入！")
        reset_check_code(check_str,username,password)


def reset_password():
    """重置密码"""
    username = input("请输入用户名：")
    password = input("请输入密码：")
    password_check = input("请再次输入密码：")
    if password == password_check:
        email_str = input("请输入注册时的邮箱地址：")
        if email_str == check_email(username):
            check_str = send_check_code(email_str)
            if (check_str == ''):
                print("验证码发送失败")
                reset_password()
            check_code = input("请输入重置邮件中的验证吗：")
            if check_code == check_str:
                result = update_password(username,password)
                if result:
                    print("修改密码成功，请登陆！")
                    login_menu()
                else:
                    print("修改密码失败！")
                    reset_password()
            else:
                print("验证码输入错误，请确认后重新输入！")
                reset_check_code(check_str,username,password)
        else:
            print("邮箱地址或用户名错误，请检查后重新输入！")
            reset_password()
    else:
        print("两次密码不一致，请重新输入！")
        reset_password()

def show_error():
    """错误操作日志"""
    print("请确认输入的编号正确再进行操作！")

def login_menu():
    """登陆界面"""
    print("""
登陆界面：
0:退出
1：登陆
2：注册
3：忘记密码
    """)
    operate()

def operate():
    """登陆操作响应"""
    flag = input("请根据菜单输入操作编号：")
    if flag == '0':
        quit()
    elif flag == '1':
        login()
        login_menu()
    elif flag == '2':
        register()
        login_menu()
    elif flag == '3':
        reset_password()
        login_menu()
    else:
        show_error()
        login_menu()

def main():
    """程序入口"""
    login_menu()


if __name__ == '__main__':
    main()