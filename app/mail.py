import smtplib
from email.mime.text import MIMEText
import random as rd
def postmailnum(mailnum):
    mail_host = 'smtp.qq.com'  
    mail_user = '3517213049'  
    mail_pass = 'xlujvtzkpxrvchjj'   
    sender = '3517213049@qq.com'  
    receivers = [str(mailnum)] 
    num = rd.randint(100000,1000000)
    message = MIMEText("钵钵鸡BBS\n验证码:"+str(num)+"\n温馨提示：不要给其他人看哦~",'plain','utf-8')  
    message['Subject'] = '钵钵鸡BBS验证码' 
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