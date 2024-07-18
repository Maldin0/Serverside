from zoneinfo import ZoneInfo
from datetime import datetime, timedelta
from django.utils import timezone

dt1 = timezone.now()
print(dt1)
print(timezone.is_aware(dt1))

dt1_local = timezone.localtime(dt1)
print(dt1_local)

dt2 = dt1_local + timedelta(days=500)
print(dt2.weekday())