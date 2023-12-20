# views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Report
from .serializers import ReportSerializer, UserReportSerializer, AdminReportSerializer, ReportUpdateSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsForumAdmin
from rest_framework.pagination import LimitOffsetPagination
from django.utils import timezone
from Forum.models import Post

class MyLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 40   
    limit_query_param = 'limit'  
    offset_query_param = 'offset' 
    max_limit = 40 

    def get_paginated_response(self, data):
        return Response({
            "count": self.count,  # 总条目数
            "next": self.get_next_link(),  # 下一页的 URL
            "previous": self.get_previous_link(),  # 上一页的 URL
            "limit": self.limit,  # 当前页的条目数
            "offset": self.offset,  # 当前页的偏移量
            "data": data  # 当前页的数据
        })
    


class ReportCreateView(APIView):
    permission_classes = [IsAuthenticated]

    

    def post(self, request, format=None):
        post_id = request.data.get('post')

        # 验证 post_id 是否存在且有效
        if post_id is None:
            return Response({"detail": "Post ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            post_id = int(post_id)
            post = Post.objects.get(pk=post_id)
        except (ValueError, TypeError):
            return Response({"detail": "Invalid post ID"}, status=status.HTTP_400_BAD_REQUEST)
        except Post.DoesNotExist:
            return Response({"detail": "Post not found"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ReportSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(post=post) 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class UserReportsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        reports = Report.objects.filter(reporter=request.user)
        paginator = MyLimitOffsetPagination()
        result_page = paginator.paginate_queryset(reports, request)
        serializer = UserReportSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)





    
class PendingReportsView(APIView):
    permission_classes = [IsForumAdmin]

    def get(self, request, format=None):
        unresolved_reports = Report.objects.filter(report_status='pending')
        paginator = MyLimitOffsetPagination()
        result_page = paginator.paginate_queryset(unresolved_reports, request)
        serializer = AdminReportSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

class ResolvedReportsView(APIView):
    permission_classes = [IsForumAdmin]

    def get(self, request, format=None):
        resolved_reports = Report.objects.exclude(report_status='pending')
        paginator = MyLimitOffsetPagination()
        result_page = paginator.paginate_queryset(resolved_reports, request)
        serializer = AdminReportSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

class AllReportsView(APIView):
    permission_classes = [IsForumAdmin]

    def get(self, request, format=None):
        all_reports = Report.objects.all()
        paginator = MyLimitOffsetPagination()
        result_page = paginator.paginate_queryset(all_reports, request)
        serializer = AdminReportSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class ReportUpdateView(APIView):
    permission_classes = [IsAuthenticated]  

    def put(self, request, pk, format=None):
        try:
            report = Report.objects.get(pk=pk)
        except Report.DoesNotExist:
            return Response({'message': 'Report not found'}, status=status.HTTP_404_NOT_FOUND)

        # 检查举报是否已经被处理过
        if report.report_status != 'pending':
            return Response({'message': 'This report has already been processed.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ReportUpdateSerializer(report, data=request.data)

        if serializer.is_valid():
            if serializer.validated_data.get('report_status') != 'pending':
                serializer.validated_data['resolved_at'] = timezone.now()
            else:
                return Response({'message': 'Cannot set the status to pending'}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



class SingleReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, format=None):
        try:
            report = Report.objects.get(pk=pk)
        except Report.DoesNotExist:
            return Response({'message': 'Report not found'}, status=status.HTTP_404_NOT_FOUND)

        # 如果用户是管理员，或者举报由该用户创建，则返回举报信息
        if request.user.is_forum_admin or report.reporter == request.user:
            serializer = UserReportSerializer(report)
            return Response(serializer.data)
        else:
            return Response({'message': 'You do not have permission to access this report'}, status=status.HTTP_403_FORBIDDEN)
        

        


from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def test_get_forum_admin(request):
    if settings.DEBUG:
        user = request.user
        user.is_forum_admin = not user.is_forum_admin  # 切换管理员状态
        user.save()  # 保存到数据库

        status_message = 'Now you are a forum admin' if user.is_forum_admin else 'Now you are not a forum admin'
        return Response(status_message)
    else:
        return Response('This is not a debug environment')
