from django.db import models
from storages.backends.s3boto3 import S3Boto3Storage


class Corporation(models.Model):
    corp_name = models.CharField(max_length=100)
    ceo_name = models.CharField(max_length=100)
    corp_addr = models.CharField(max_length=100)
    corp_homepage = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    est_date = models.CharField(max_length=100)
    sales_revenue = models.CharField(max_length=100)
    operating_profit = models.CharField(max_length=100)
    stock_code = models.CharField(max_length=100, null=True)
    company_info = models.CharField(max_length=1000, null=True)

    def __str__(self):
        return f'{self.corp_name}'


class SmartLogistics(models.Model):
    tech_name = models.CharField(max_length=100, default='tech', primary_key=True)
    description = models.CharField(default=' ', max_length=10000)
    port_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='smart_logistics_images/', storage=S3Boto3Storage(), null=True, blank=True)

    def __str__(self):
        return self.tech_name


class Recruitment(models.Model):
    code = models.CharField(max_length=100)
    wantedAuthNo = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    salTpNm = models.CharField(max_length=255)
    sal = models.CharField(max_length=255)
    minSal = models.CharField(max_length=255)
    maxSal = models.CharField(max_length=255)
    region = models.CharField(max_length=255)
    holidayTpNm = models.CharField(max_length=255)
    minEdubg = models.CharField(max_length=255)
    career = models.CharField(max_length=255)
    regDt = models.CharField(max_length=255)
    closeDt = models.CharField(max_length=255)
    infoSvc = models.CharField(max_length=255)
    wantedInfoUrl = models.CharField(max_length=255)
    wantedMobileInfoUrl = models.CharField(max_length=255)
    smodifyDtm = models.CharField(max_length=255)
    zipCd = models.CharField(max_length=255)
    strtnmCd = models.CharField(max_length=255)
    basicAddr = models.CharField(max_length=255)
    empTpCd = models.IntegerField()
    jobsCd = models.IntegerField()

    def __str__(self):
        return f'{self.code} / {self.company}'


class News(models.Model):
    query = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    link = models.CharField(max_length=100)
    originalLink = models.CharField(max_length=100)
    description = models.CharField(max_length=10000)
    article = models.TextField(null=True)
    summary = models.CharField(max_length=1000, null=True)
    pubData = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.query} / {self.title}'


class Concern(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    google_user_id = models.CharField(max_length=255, default='null',unique=True)
    email = models.EmailField(unique=True, blank=True)
    name = models.CharField(max_length=255, blank=True)
    concerns = models.ManyToManyField(Concern, related_name='user_profiles', blank=True)

