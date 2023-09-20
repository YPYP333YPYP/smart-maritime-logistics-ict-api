import requests
import xml.etree.ElementTree as ET
from ict_api.settings import WORKNET_KEY
from corp_info.models import Recruitment


def get_recruit(code):
    url = 'http://openapi.work.go.kr/opi/opi/opia/wantedApi.do'

    params = {
        "authKey": WORKNET_KEY,
        "callTp": "L",
        "returnType": "xml",
        "startPage": 1,
        "display": 10,
        "occupation": code
    }

    response = requests.get(url, params=params)
    response_text = response.content.decode('utf-8')

    root = ET.fromstring(response_text)

    wantedAuthNo_list = []
    company_list = []
    title_list = []
    salTpNm_list = []
    sal_list = []
    minSal_list = []
    maxSal_list = []
    region_list = []
    holidayTpNm_list = []
    minEdubg_list = []
    career_list = []
    regDt_list = []
    closeDt_list = []
    infoSvc_list = []
    wantedInfoUrl_list = []
    wantedMobileInfoUrl_list = []
    smodifyDtm_list = []
    zipCd_list = []
    strtnmCd_list = []
    basicAddr_list = []
    empTpCd_list = []
    jobsCd_list = []

    for wanted in root.iter('wanted'):
        wantedAuthNo_list.append(wanted.find('wantedAuthNo').text)
        company_list.append(wanted.find('company').text)
        title_list.append(wanted.find('title').text)
        salTpNm_list.append(wanted.find('salTpNm').text)
        sal_list.append(wanted.find('sal').text)
        minSal_list.append(wanted.find('minSal').text)
        maxSal_list.append(wanted.find('maxSal').text)
        region_list.append(wanted.find('region').text)
        holidayTpNm_list.append(wanted.find('holidayTpNm').text)
        minEdubg_list.append(wanted.find('minEdubg').text)
        career_list.append(wanted.find('career').text)
        regDt_list.append(wanted.find('regDt').text)
        closeDt_list.append(wanted.find('closeDt').text)
        infoSvc_list.append(wanted.find('infoSvc').text)
        wantedInfoUrl_list.append(wanted.find('wantedInfoUrl').text)
        wantedMobileInfoUrl_list.append(wanted.find('wantedMobileInfoUrl').text)
        smodifyDtm_list.append(wanted.find('smodifyDtm').text)
        zipCd_list.append(wanted.find('zipCd').text)
        strtnmCd_list.append(wanted.find('strtnmCd').text)
        basicAddr_list.append(wanted.find('basicAddr').text)
        empTpCd_list.append(wanted.find('empTpCd').text)
        jobsCd_list.append(wanted.find('jobsCd').text)

    data = {
        'code' : code,
        'wantedAuthNo': wantedAuthNo_list,
        'company': company_list,
        'title': title_list,
        'salTpNm': salTpNm_list,
        'sal': sal_list,
        'minSal': minSal_list,
        'maxSal': maxSal_list,
        'region': region_list,
        'holidayTpNm': holidayTpNm_list,
        'minEdubg': minEdubg_list,
        'career': career_list,
        'regDt': regDt_list,
        'closeDt': closeDt_list,
        'infoSvc': infoSvc_list,
        'wantedInfoUrl': wantedInfoUrl_list,
        'wantedMobileInfoUrl': wantedMobileInfoUrl_list,
        'smodifyDtm': smodifyDtm_list,
        'zipCd': zipCd_list,
        'strtnmCd': strtnmCd_list,
        'basicAddr': basicAddr_list,
        'empTpCd': empTpCd_list,
        'jobsCd': jobsCd_list,
    }
    return data


def save_recruitment_data(data):
    for i in range(len(data['wantedAuthNo'])):
        recruitment = Recruitment.objects.create(
            code = data['code'],
            wantedAuthNo=data['wantedAuthNo'][i],
            company=data['company'][i],
            title=data['title'][i],
            salTpNm=data['salTpNm'][i],
            sal=data['sal'][i],
            minSal=data['minSal'][i],
            maxSal=data['maxSal'][i],
            region=data['region'][i],
            holidayTpNm=data['holidayTpNm'][i],
            minEdubg=data['minEdubg'][i],
            career=data['career'][i],
            regDt=data['regDt'][i],
            closeDt=data['closeDt'][i],
            infoSvc=data['infoSvc'][i],
            wantedInfoUrl=data['wantedInfoUrl'][i],
            wantedMobileInfoUrl=data['wantedMobileInfoUrl'][i],
            smodifyDtm=data['smodifyDtm'][i],
            zipCd=data['zipCd'][i],
            strtnmCd=data['strtnmCd'][i],
            basicAddr=data['basicAddr'][i],
            empTpCd=data['empTpCd'][i],
            jobsCd=data['jobsCd'][i],
        )
