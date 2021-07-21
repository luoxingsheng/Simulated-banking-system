#coding=UTF-8
from datetime import datetime
import csv_tool
import mysql_tool as conn

user_id = ''
user_balance = 0.0
operate_log = [['交易日期', '摘要', '金额', '币种', '余额']]
# hearder=['datetime','summary','money','currency','balance']

def main_menu():
    """显示主菜单界面"""
    print(f"""
当前余额：{user_balance}
操作菜单：
0：退出
1：存款
2：取款
3：打印交易详情
    """)
    operate()

def quit_operate():
    """退出登陆时，清空内存"""
    global user_id,user_balance,operate_log
    user_id = ''
    user_balance = 0.0
    operate_log = [['交易日期', '摘要', '金额', '币种', '余额']]

def operate():
    """用户操作响应"""
    flag = input("请根据菜单输入操作编号：")
    if flag == '0':
        quit_operate()
        quit()
    elif flag == '1':
        deposit()
        main_menu()
    elif flag == '2':
        withdrawl()
        main_menu()
    elif flag == '3':
        show_log()
        main_menu()
    else:
        show_error()
        main_menu()

def quit():
    """退出程序"""
    print("谢谢使用！")

def deposit():
    """存款操作"""
    global user_balance
    money = float(input("请输入需要存款的金额："))
    balance = user_balance + money
    if update_balance(balance):
        user_balance = balance
        add_log('0',money)
        print(f'存款{money}成功,当前余额为{user_balance}')

def withdrawl():
    """取款操作"""
    global user_balance
    money = float(input("请输入需要取款的金额："))
    balance = user_balance - money
    if balance < 0:
        print(f"余额不足,当前余额为{user_balance}")
    else:
        if update_balance(balance):
            user_balance = balance
            add_log('1', money)
            print(f'取款{money}成功,当前余额为{user_balance}')

def show_log():
    """操作日志"""
    global operate_log
    for log in operate_log:
        print(log)
    save_csv()

def show_error():
    """错误操作日志"""
    print("请确认输入的编号正确再进行操作！")

def add_log(flag,money):
    """增加操作日志"""
    """
    flag为0代表存款，
    money代表操作的金额
    """
    log = []
    now = str(datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S %f'))
    summary = ''
    currency = '人民币'
    money_str = '+' + str(money)
    if flag == '0':
        summary = '存款'
    elif flag == '1':
        summary = '取款'
    log = [now,summary,money_str,currency,str(user_balance)]
    operate_log.append(log)
    sql = f"""insert into bank_log(user_id,datetime,summary,money,currency,balance)  """ \
          f"""values('{user_id}','{now}','{summary}','{money}','{currency}','{user_balance}')"""
    conn.add(sql)

def save_csv():
    """日志保存到csv文件中"""
    now = datetime.now().strftime('%Y-%m-%d')
    filename = f"{now}.csv"
    hearder=['交易日期','摘要','金额','币种','余额']
    datas = operate_log[1:]
    csv_tool.create_csv(filename, hearder, datas)

def update_balance(balance):
    """更新账户余额"""
    sql = f"update user set balance = {balance} where id = '{user_id}'"
    result = conn.update(sql)
    if result:
        pass
    else:
        print("账户余额更新失败！")
    return result

