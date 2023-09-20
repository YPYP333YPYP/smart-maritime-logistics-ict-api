# smart-maritime-logistics-ict-api

# 프로젝트 설명
https://www.hanium.or.kr/portal/smart/businessOverview.do
스마트해상물류 ICT 멘토링 참여 프로젝트
일반인들을 위한 스마트해상물류 기술 알림 챗봇 서비스

# 백엔드 아키텍처
![작품구성도](https://github.com/YPYP333YPYP/smart-maritime-logistics-ict-api/assets/57821687/38e79e8e-2e31-4ec6-a1f1-fdd74c7f0787)


# API 명세서
|Method|URI|Description|
|------|---|---|
|GET|/save_corp/{name}|상장 기업 정보 저장|
|GET|/get_corp/{name}|상장 기업 정보 검색|
|GET|/get_corp_name_list|상장 기업 리스트 검색|
|GET|/save_recruit/{code}|직종 코드별 채용정보 저장|
|GET|/get_recruit/{code}|직종 코드별 채용정보 검색|
|DELETE|/get_recruit/{code}|직종 코드별 채용정보 삭제|
|GET|/save_news/{query}|뉴스 정보 저장|
|GET|/get_news/{query}|뉴스 정보 검색|
|DELETE|/get_news/{query}|뉴스 정보 삭제|
|POST|/interest_news|관심사별 뉴스 정보 검색|
|POST|/create_smart_logistics|스마트해상물류기술 정보 저장|
|GET|/get_smart_tech|스마트해상물류기술 정보 검색|
|POST|/create_user_profile|google oauth를 통한 유저프로필 생성|
|GET|/get_user_profile/{google_user_id}|유저프로필 검색|
|GET|/concerns|관심사 정보 리스트 검색|
|POST|/concerns|관심사 정보 저장|
|GET|/concerns/{name}|관심사 정보 검색|
|DELETE|/concerns/{name}|관심사 정보 삭제|
|POST|/user_profile_concerns|유저프로필에 관심사 추가|
|DELETE|/user_profile_concerns|유저프로필에 관심사 삭제|
