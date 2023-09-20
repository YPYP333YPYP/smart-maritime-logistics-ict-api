import os
import sys
import logging
from django.core.wsgi import get_wsgi_application
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from corp_info.information import Information
from corp_info.models import Corporation

# 루트 디렉터리 설정
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# scheduler.log 파일에 로그 데이터 저장
logging.basicConfig(filename='scheduler.log', level=logging.INFO)


# 일주일에 한번씩 기업 정보 저장
def schedule_update_corp_info():
    # 해운 기업 리스트
    company_list = ['HMM', '흥아해운', '태웅로직스','와이엔텍','KSS해운','웰바이오텍','팬오션']
    info = Information()
    for company in company_list:
        corp_info = info.get_corp_information(company, info.appkey)
        corp_fin = info.get_corp_finance(company, info.appkey)
        corp_company_info = info.get_company_info(company)
        try:
            corporation = Corporation.objects.get(corp_name=company)
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

        except Corporation.DoesNotExist:

            corporation = Corporation(
                corp_name=company,
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

        logging.info(f"{company} 정보가 업데이트되었습니다. {str(datetime.now())}")

# 스케줄러 작동 테스트
#schedule_update_corp_info()

# 스케줄러 작동
scheduler = BackgroundScheduler()
scheduler.add_job(schedule_update_corp_info, "interval", weeks=1)
scheduler.start()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ict_api.settings')

application = get_wsgi_application()
