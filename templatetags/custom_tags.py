from datetime import datetime, date, timedelta
from django import template
register = template.Library()

# 今日の日付を取得する
@register.filter
def getToday():
    return date.