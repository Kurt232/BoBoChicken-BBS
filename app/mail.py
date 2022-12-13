import smtplib
from email.mime.text import MIMEText
import random as rd
def postmailnum(mailnum):
    mail_host = 'smtp.163.com'  
    mail_user = 'Tennineee'  
    mail_pass = 'FDAQPSYNHRZZLOWU'   
    sender = 'Tennineee@163.com'  
    receivers = [str(mailnum)] 
    num = rd.randint(100000,1000000)
    type = rd.randint(0,3)
    if type==0:
        message = MIMEText("钵钵鸡BBS验证码："+str(num),'plain','utf-8')  
        message['Subject'] = "此邮件为验证码"
    elif type==1:
        message = MIMEText("钵钵鸡BBS欢迎您\n验证码："+str(num),'plain','utf-8')  
        message['Subject'] = "钵钵鸡BBS欢迎您"
    elif type==2:
        message = MIMEText("Hello world!\n钵钵鸡BBS验证码："+str(num),'plain','utf-8')  
        message['Subject'] = "Hello world!"
    message['From'] = sender 
    message['To'] = receivers[0]  
    try:
        smtpObj = smtplib.SMTP() 
        #连接到服务器
        smtpObj.connect(mail_host,25)
        #登录到服务器
        smtpObj.login(mail_user,mail_pass) 
        #发送
        smtpObj.sendmail(
            sender,receivers,message.as_string()) 
        #退出
        smtpObj.quit() 
        print('success')
    except smtplib.SMTPException as e:
        print('error',e) #打印错误
    return str(num)