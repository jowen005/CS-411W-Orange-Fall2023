
from django.contrib.auth import get_user_model
from datetime import timedelta
from django.utils import timezone
from ..models import LoginAnalytics, LoginRecord

User = get_user_model()

def driver(sim_datetime):
    login_data , current_datestamp = login_analysis(sim_datetime)
    for entry in login_data:
        # print(entry) #DEBUG
        obj = LoginAnalytics.objects.create(**entry, date_stamp=current_datestamp)
        print(obj)
    print('\n')


def login_analysis(sim_datetime):

    if sim_datetime is None:
        current_datestamp = timezone.now()
    else:
        current_datestamp = sim_datetime

    latest_datestamp = current_datestamp - timedelta(days=3)
    login_data = []

    users = User.objects.exclude(user_type = 'admin')
    login_set = LoginRecord.objects.all()

    for user in users:
        data = {}
        data['user'] = user
        data['total_logins'] = login_set.filter(user = user).count()

        data['logins_since'] = login_set.filter(user = user, date_stamp__gte=latest_datestamp).count()
        login_data.append(data)
    
    return login_data , current_datestamp

