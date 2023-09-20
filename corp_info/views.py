from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, viewsets, status
from rest_framework.exceptions import NotFound
from rest_framework.decorators import api_view, action, permission_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from google.oauth2 import id_token
from google.auth.transport import requests
from ict_api import settings
from .serializers import CorporationSerializer, SmartLogisticsSerializer, RecruitmentSerializer, NewsSerializer, \
    UserProfileSerializer, ConcernSerializer, CorporationNameSerializer
from .models import Corporation, SmartLogistics, Recruitment, News, UserProfile, Concern
from .information import Information
from .recruitment import get_recruit, save_recruitment_data
from .news import get_news, save_news, UsageExceededException, UsingApiException


# 기업 정보를 직접 저장할 수 있는 GET API
@api_view(['GET'])
def update_corp_info(request, name):
    if request.method == 'GET':
        info = Information()
        try:
            corp_info = info.get_corp_information(name, info.appkey)
            corp_fin = info.get_corp_finance(name, info.appkey)
            corp_company_info = info.get_company_info(name)
        except ValueError:
            raise NotFound("정상적이지 않은 값이 입력되었습니다.")
    try:
        corporation = Corporation.objects.get(corp_name=name)
        corporation.ceo_name = corp_info['ceo_name']
        corporation.corp_addr = corp_info['corp_addr']
        corporation.corp_homepage = corp_info['corp_homepage']
        corporation.phone_number = corp_info['phone_number']
        corporation.est_date = corp_info['est_date']
        corporation.sales_revenue = corp_fin['sales_revenue']
        corporation.operating_profit = corp_fin['operating_profit']
        corporation.stock_code = corp_info['stock_code']
        corporation.company_info = corp_company_info
        corporation.save()

        return Response({'message': '기업 정보가 업데이트되었습니다.'}, status=200)

    except Corporation.DoesNotExist:

        corporation = Corporation(
            corp_name=name,
            ceo_name=corp_info['ceo_name'],
            corp_addr=corp_info['corp_addr'],
            corp_homepage=corp_info['corp_homepage'],
            phone_number=corp_info['phone_number'],
            est_date=corp_info['est_date'],
            sales_revenue=corp_fin['sales_revenue'],
            operating_profit=corp_fin['operating_profit'],
            stock_code=corp_info['stock_code'],
            company_info=corp_company_info
        )
        corporation.save()

        return Response({'message': '기업 정보가 업데이트되었습니다.'}, status=200)


# 기업 정보를 조회할 수 있는 GET API
class CorporationDetailAPIView(generics.RetrieveAPIView):
    queryset = Corporation.objects.all()
    serializer_class = CorporationSerializer
    lookup_field = 'corp_name'

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        corp_name = self.kwargs['corp_name']
        try:
            obj = queryset.get(corp_name=corp_name)
            return obj
        except Corporation.DoesNotExist:
            return Response({'error': '일치하는 기업이 없습니다.'}, status=404)


# 모든 기업의 이름만 조회하는 GET API
class CorpNameListView(generics.ListAPIView):
    queryset = Corporation.objects.all()
    serializer_class = CorporationNameSerializer


class SmartLogisticsAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request):
        serializer = SmartLogisticsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


# 스마트해상물류 기술을 조회할 수 있는 GET API
class SmartLogisticsViewSet(viewsets.ModelViewSet):
    serializer_class = SmartLogisticsSerializer
    queryset = SmartLogistics.objects.all()
    lookup_field = 'port_name'

    def get_queryset(self):
        port_name = self.kwargs['port_name']
        queryset = SmartLogistics.objects.filter(port_name=port_name)
        return queryset

    @action(detail=False, methods=['get'], url_path='<str:port_name>/')
    def get_by_port_name(self, request, port_name=None):
        queryset = self.get_queryset()
        instance = get_object_or_404(queryset, port_name=port_name)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


# 직업코드 별 채용정보를 저장할 수 있는 GET API
class RecruitmentAPIView(APIView):
    def get(self, request, code):
        data = get_recruit(code)

        if data:
            save_recruitment_data(data)
            return Response({'message': code + '채용정보에 대한 채용정보가 업데이트 되었습니다.'})
        else:
            return Response({'error': '채용정보가 정상적으로 업데이트 되지 않았습니다.'}, status=500)


# 직업코드에 따른 채용정보 리스트를 불러올 수 있는 GET API
class RecruitmentListAPIView(APIView):
    def get(self, request, code):
        recruitments = Recruitment.objects.filter(code=code)

        if not recruitments.exists():
            return Response({"error": "검색하신 채용정보가 없습니다."}, status=404)

        serializer = RecruitmentSerializer(recruitments, many=True)
        return Response(serializer.data)

    def delete(self, request, code):
        recruitments_to_delete = Recruitment.objects.filter(code=code)

        if not recruitments_to_delete.exists():
            return Response({"error": "삭제할 채용정보가 없습니다."}, status=404)

        recruitments_to_delete.delete()
        return Response({"message": "채용정보가 삭제되었습니다."}, status=200)


# 검색조건에 따라 뉴스를 저장하는 GET API
class NewsAPIView(APIView):
    def get(self, request, query):
        data = get_news(query)

        if data:
            try:
                save_news(query, data)
            except UsageExceededException as ue:
                return JsonResponse({"error": ue}, status=500)

            except UsingApiException as ae:
                return JsonResponse({"error": ae}, status=500)

            return Response({'message': query + '검색어에 대한 뉴스정보가 업데이트 되었습니다.'})
        else:
            raise NotFound('뉴스정보가 정상적으로 업데이트 되지 않았습니다')


# 검색어 따라 뉴스를 제공하는 GET API
class NewsListAPIView(APIView):
    def get(self, request, query):
        news = News.objects.all()

        if query:
            news = news.filter(query__icontains=query)

        if not news.exists():
            return Response({"error": "검색하신 뉴스가 없습니다."}, status=404)

        serializer = NewsSerializer(news, many=True)

        return Response(serializer.data)

    def delete(self, request, query):
        if not query:
            return Response({"error": "삭제할 뉴스를 지정해주세요."}, status=400)

        news_to_delete = News.objects.filter(query__icontains=query)

        if not news_to_delete.exists():
            return Response({"error": "삭제할 뉴스가 없습니다."}, status=404)

        news_to_delete.delete()
        return Response({"message": "검색하신 뉴스가 삭제되었습니다."})


# 관심사에 따른 뉴스를 조회하는 POST API
class InterestNewsAPIView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'query_list': openapi.Schema(type=openapi.TYPE_STRING),
            }
        )
    )
    def post(self, request):
        query_list = request.data.get('query_list', [])
        if not query_list:
            return Response({"error": "관심사 리스트가 비어있습니다."}, status=404)

        query_list = query_list.split(',')  # 구분 문자로 구분하여 리스트로 변환

        results = News.objects.filter(query__in=query_list)

        if not results:
            return Response({"error": "일치하는 뉴스가 없습니다."}, status=404)

        serializer = NewsSerializer(results, many=True)
        return Response(serializer.data)


# google login api를 통한 UserProfile 생성 POST API
@api_view(['POST'])
def create_user_profile(request):
    token = request.data.get('google_access_token')
    if not token:
        return Response({'error': 'Google token이 필요합니다..'}, status=400)

    try:
        id_info = id_token.verify_oauth2_token(token, requests.Request(), settings.GOOGLE_CLIENT_ID)
        if id_info['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError('Invalid issuer.')

        google_user_id = id_info['sub']
        email = id_info['email']
        name = id_info.get('name', '')

        user_profile, created = UserProfile.objects.get_or_create(google_user_id=google_user_id,
                                                                  defaults={'email': email, 'name': name})

        serializer = UserProfileSerializer(user_profile)
        return Response(serializer.data, status=201 if created else 200)

    except ValueError as e:
        return Response({'error': str(e)}, status=400)


# UserProfile 조회하는 GET API
class UserProfileGetAPIView(APIView):
    def get(self, request, google_user_id):
        try:

            user_profile = UserProfile.objects.get(google_user_id=google_user_id)
        except UserProfile.DoesNotExist:
            return Response({'error': '해당하는 UserProfile이 없습니다'}, status=404)

        serializer = UserProfileSerializer(user_profile)
        return Response(serializer.data, status=200)


# Concern 조회 및 생성 API
class ConcernListAPI(APIView):
    def get(self, request):
        concerns = Concern.objects.all()
        serializer = ConcernSerializer(concerns, many=True)
        return Response(serializer.data)


    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING),
                'type': openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['name', 'type'],
        ),
        responses={201: ConcernSerializer()},
    )
    def post(self, request):
        serializer = ConcernSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response({'error':'정상적으로 생성되지 않았습니다.'}, status=400)


# Concern 단일 조회 및 삭제 API
class ConcernDetailAPI(APIView):
    def get_object(self, name):
        try:
            return Concern.objects.get(name=name)
        except Concern.DoesNotExist:
            raise NotFound('매칭되는 concern이 존재하지 않습니다.')

    def get(self, request, name):
        concern = self.get_object(name)
        serializer = ConcernSerializer(concern)
        return Response(serializer.data)

    def delete(self, request, name):
        concern = self.get_object(name)
        concern.delete()
        return Response(status=204)


# UserProfile에 Concern을 추가하고 삭제하는 API
class UserProfileConcernAPI(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'google_user_id': openapi.Schema(type=openapi.TYPE_STRING),
                'concern_name': openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['google_user_id', 'concern_name'],
        ),
        responses={200: UserProfileSerializer()},
    )
    def post(self, request):
        google_user_id = request.data.get('google_user_id')
        concern_name = request.data.get('concern_name')

        try:
            user_profile = UserProfile.objects.get(google_user_id=google_user_id)
        except UserProfile.DoesNotExist:
            return Response({'error': '해당하는 UserProfile이 존재하지 않습니다.'}, status=404)

        try:
            concern = Concern.objects.get(name=concern_name)
        except Concern.DoesNotExist:
            return Response({'error': '해당하는 Concern이 존재하지 않습니다.'}, status=404)

        user_profile.concerns.add(concern)
        serializer = UserProfileSerializer(user_profile)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                 'google_user_id': openapi.Schema(type=openapi.TYPE_STRING),
                 'concern_name': openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['google_user_id', 'concern_name'],
        ),
        responses={200: UserProfileSerializer()},
    )
    def delete(self, request):
        google_user_id = request.data.get('google_user_id')
        concern_name = request.data.get('concern_name')

        try:
            user_profile = UserProfile.objects.get(google_user_id=google_user_id)
        except UserProfile.DoesNotExist:
            return Response({'error': '해당하는 UserProfile이 존재하지 않습니다.'}, status=404)

        try:
            concern = Concern.objects.get(name=concern_name)
        except Concern.DoesNotExist:
            return Response({'error': '해당하는 Concern이 존재하지 않습니다.'}, status=404)

        if user_profile.concerns is not None:
            user_profile.concerns.remove(concern)

        serializer = UserProfileSerializer(user_profile)
        return Response(serializer.data)
