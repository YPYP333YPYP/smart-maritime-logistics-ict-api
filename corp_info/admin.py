from django.contrib import admin
from .models import Corporation, SmartLogistics,  Recruitment, News, Concern, UserProfile

admin.site.register(Corporation)
admin.site.register(SmartLogistics)
admin.site.register(Concern)
admin.site.register(Recruitment)
admin.site.register(News)
admin.site.register(UserProfile)
