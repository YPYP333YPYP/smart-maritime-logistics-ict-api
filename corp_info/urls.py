from django.urls import path, include
from .views import update_corp_info, CorporationDetailAPIView, SmartLogisticsViewSet, RecruitmentAPIView, \
    RecruitmentListAPIView, NewsAPIView, NewsListAPIView, \
    InterestNewsAPIView, SmartLogisticsAPIView, create_user_profile, UserProfileGetAPIView, ConcernDetailAPI, \
    ConcernListAPI, UserProfileConcernAPI, CorpNameListView

urlpatterns = [
    path('save_corp/<str:name>', update_corp_info, name='update_corp_info'),
    path('get_corp/<str:corp_name>/', CorporationDetailAPIView.as_view(), name='corporation'),
    path('get_smart_tech/<str:port_name>/', SmartLogisticsViewSet.as_view({'get': 'list'}), name='smart-detail'),
    path('save_recruit/<str:code>/', RecruitmentAPIView.as_view(), name='update_recruitment'),
    path('get_recruit/<str:code>/', RecruitmentListAPIView.as_view(), name='get_recruitment'),
    path('save_news/<str:query>/', NewsAPIView.as_view(), name='update_news'),
    path('get_news/<str:query>', NewsListAPIView.as_view(), name='get_news'),
    path('interest_news/',InterestNewsAPIView.as_view(), name='interest_news'),
    path('create_smart_logistics/', SmartLogisticsAPIView.as_view(), name='create_smart_logistics'),
    path('create_user_profile/', create_user_profile, name='create_user_profile'),
    path('get_user_profile/<str:google_user_id>', UserProfileGetAPIView.as_view(), name='get_user_profile'),
    path('concerns/', ConcernListAPI.as_view(), name='concern-list'),
    path('concerns/<str:name>/', ConcernDetailAPI.as_view(), name='concern-detail'),
    path('user_profile_concerns/', UserProfileConcernAPI.as_view(), name='userprofile_with_concern'),
    path('get_corp_name_list', CorpNameListView.as_view(), name='corp_name')
]
