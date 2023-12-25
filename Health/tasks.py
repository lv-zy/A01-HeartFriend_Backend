from celery import shared_task
from django.conf import settings
from django.contrib.auth import get_user_model
import requests
import datetime

User = get_user_model() 
send_message_url = "https://wxpusher.zjiecode.com/api/send/message"
app_token = "AT_6HJxIZU3rx6eDm5l2zrta6IsnqoDpZZO"


@shared_task
def send_message_task():
    print("loop all users and sending messages...") 
    all_users = User.objects.all() 
    today = datetime.now().date() 
    for user in all_users: 
        if user.uid is not None: 
            content = "您好！亲爱的" + user.username + ": \n"
            content += "今天是 " + today + ", "
            content += "您有如下的药物: \n\n"
            all_medicine = user.medicine_set.filter(start_date__lte=today, finish_date__gte=today)  
            for medicine in all_medicine:
                content += "药物：" + medicine.name + " \n"
                content += "服用时间: " + medicine.select_time + " \n"
                content += "服用计量: " + medicine.amount + " " + medicine.unit + " \n"
                content += "\n"
            content += "记得按时吃药哦～" 
            send_message_response = requests.post(send_message_url, json={
                "content": content, 
                "appToken": app_token, 
                "summary": "记得按时吃药哦～", 
                "contentType": 1, 
                "uids": [user.uid], 
                "verifyPay": False 
            },headers={'Content-Type': 'application/json'})
            response_data = send_message_response.json() 
            # TODO check sending status 
            pass 
        else:
            pass
    
    return "Message sent..."