from django.urls import path
from .views import ReportCreateView, UserReportsView, AllReportsView, PendingReportsView, ResolvedReportsView, ReportUpdateView

urlpatterns = [
    path('reports/', ReportCreateView.as_view(), name='report'),
    path('reports/user/', UserReportsView.as_view(), name='user_reports'),
    path('reports/manage/all/', AllReportsView.as_view(), name='all_reports'),
    path('reports/manage/pending/', PendingReportsView.as_view(), name='pending_reports'),
    path('reports/manage/resolved/', ResolvedReportsView.as_view(), name='resolved_reports'),
    path('reports/manage/<int:pk>/', ReportUpdateView.as_view(), name='manage_report'),
]
