from django.db.models import Avg
from django.utils import timezone

from feedback.models import AppSatisfaction
from ..models import AppSatisfactionAnalytics


def driver (sim_datetime):
    if sim_datetime is None:
        current_datestamp = timezone.now()
    else:
        current_datestamp = sim_datetime

    app_data = app_satisfaction_analysis()

    # print(f'App Satisfaction Analytics: {app_data}') #NOTE

    obj = AppSatisfactionAnalytics.objects.create(**app_data, date_stamp=current_datestamp)
    print(f'{obj}\n')


def app_satisfaction_analysis():
    app_data = {}

    ratings = AppSatisfaction.objects.all()

    app_data['number_of_rating_total'] = ratings.count()
    app_data['average_rating'] = ratings.aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0

    return app_data