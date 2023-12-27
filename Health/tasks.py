from celery import shared_task
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
import requests
from datetime import datetime, timedelta
import pytz 

Beijing_time = pytz.timezone('Asia/Shanghai')

User = get_user_model() 
send_message_url = "https://wxpusher.zjiecode.com/api/send/message"
app_token = "AT_6HJxIZU3rx6eDm5l2zrta6IsnqoDpZZO"


@shared_task
def send_message_task():
    print("loop all users and sending messages...") 
    all_users = User.objects.all() 
    time_point = datetime.now(Beijing_time)
    today = datetime.now(Beijing_time).date().strftime("%Y-%m-%d")
    for user in all_users: 
        if user.uid is not None: 
            content = "您好！亲爱的" + user.username + ": \n"
            content += "今天是 " + time_point.strftime("%Y年%m月%d日 %H:%M")
            content += "您有如下的药物: \n\n"
            all_medicine = user.medicine_set.filter(start_date__lte=today, finish_date__gte=today)
            if all_medicine is None: 
                print(f"No match medicine for user {user.username}, continue for next user...")
                continue 
            medicine_content = "---- ---- ---- ----\n"
            for medicine in all_medicine:
                medicine_time_list = medicine.select_time.split(',') if medicine else []
                if medicine_time_list is []:
                    continue 
                for medicine_time in medicine_time_list: 
                    medicine_time_obj = datetime.strptime(medicine_time, "%H:%M").time() 
                    combined_time = datetime.combine(datetime.now(Beijing_time).date(), medicine_time_obj) 
                    time_difference = Beijing_time.localize(combined_time) - time_point
                    if 0 <= time_difference.total_seconds() <= timedelta(minutes=3).total_seconds():
                        medicine_content += "药物：" + medicine.name + " \n"
                        medicine_content += "服用时间: " + medicine_time_obj.strftime("%H:%M") + " \n"
                        medicine_content += "服用剂量: " + medicine.amount + " " + medicine.unit + " \n\n"
            if medicine_content == "---- ---- ---- ----\n": 
                print(f"No match medicine time form user {user.username}, continue for next user...")
                continue
            content += medicine_content
            content += "---- ---- ---- ----\n"
            content += "记得按时吃药哦～"
            print(user.username)
            print("user message content is ", content)  
            send_message_response = requests.post(send_message_url, json={
                "content": content, 
                "appToken": app_token, 
                "summary": "记得按时吃药哦～", 
                "contentType": 1, 
                "uids": [user.uid], 
                "verifyPay": False 
            },headers={'Content-Type': 'application/json'})
            response_data = send_message_response.json()
            print(response_data)
            print(f"Message sent for user {user.username}, continue for next user") 
            continue
        else:
            print(user.username, "uid is none , continue for next user ...")
            continue
    return "Message sent..."

@shared_task
def send_email_task(): 
    print("Mail sending.......")
    subject = 'HeartFriend Group Daily Log Info'
    message = "Dear Developer: \n\n"
    message += "---- ---- ---- ----\n"
    message += "    DateTime : " + datetime.now(Beijing_time).strftime("%Y-%m-%d %H:%M") + "\n"
    message += "    Registered user number : " + str(User.objects.count()) + "\n" 
    message += "    Server's state : Normal\n"
    message += "    Nice day! \n"
    message += "\n\n" 
    message += "                            HeartFriend Backend EmailSender..."

    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['incredible749@163.com', ]
    send_mail( subject, message, email_from, recipient_list )
    return "Mail has been sent........"
