from django.contrib import admin
from user_statistics.models import UserStatistics, UserScores

admin.site.register(UserStatistics)
admin.site.register(UserScores)
