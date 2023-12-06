
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta
from django.utils import timezone
from ..models import LoginAnalytics, LoginRecord

User = get_user_model()

def driver():
    login_data , current_datestamp = login_analysis()
    for entry in login_data:
        # print(entry)
        obj = LoginAnalytics.objects.create(**entry, date_stamp=current_datestamp)
        print(obj)
        print('\n')


def login_analysis():
    current_datestamp = timezone.now()
    latest_datestamp = timezone.now() - timedelta(days=3)
    login_data = []

    users = User.objects.exclude(user_type = 'admin')
    # login_records = LoginRecord.objects.filter(date_stamp__gte=latest_datestamp)
    login_set = LoginRecord.objects.all()
    for user in users:
        data = {}
        data['user'] = user
        data['total_logins'] = login_set.filter(user = user).count()

        data['logins_since'] = login_set.filter(user = user, date_stamp__gte=latest_datestamp).count()
        login_data.append(data)
    # for record in login_records:
    #     user_id = record.user.id

    #     # Update total logins
    #     if user_id in login_data:
    #         login_data[user_id]['total_logins'] += 1
    #     else:
    #         login_data[user_id] = {'total_logins': 1, 'logins_since': 0}

    #     # Update logins since within the last day
    #     login_data[user_id]['logins_since'] = LoginRecord.objects.filter(
    #        user = user_id, date_stamp__gte=latest_datestamp
    #     ).count
    return login_data , current_datestamp
