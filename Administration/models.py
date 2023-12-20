from django.db import models
from Forum.models import Post

from django.contrib.auth import get_user_model

User = get_user_model()

class Report(models.Model):
    REPORT_TYPES = (
    ('spam', 'Spam'),  # 垃圾信息
    ('abuse', 'Abuse'),  # 滥用或骚扰
    ('offensive', 'Offensive Content'),  # 冒犯性内容
    ('false_info', 'False Information'),  # 虚假信息
    ('illegal_info', 'Illegal info'),  # 违法活动
    ('other', 'Other')  # 其他
)
    
    REPORT_STATUS = (
    ('pending', 'Pending'),
    ('accepted', 'Accepted'),
    ('rejected', 'Rejected'),
)


    post = models.ForeignKey(
        'Forum.Post',
        on_delete=models.SET_NULL,
        related_name='reports',
        null=True,  
        blank=True
    )
    report_type = models.CharField(max_length=50, choices=REPORT_TYPES)
    details = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    reporter = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='reports',
        null=True,
        blank=True
    )


    resolution_details = models.TextField(blank=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    report_status = models.CharField(max_length=50, choices=REPORT_STATUS, default='pending')
    
