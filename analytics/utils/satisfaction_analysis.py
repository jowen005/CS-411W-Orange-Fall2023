from django.db.models import Avg

from feedback.models import AppSatisfaction
from ..models import AppSatisfactionAnalytics

def driver ():
    app_data = app_satisfaction_analysis()

    print(f'App Satisfaction Analytics: {app_data}') #NOTE

    AppSatisfactionAnalytics.objects.create(**app_data)


def app_satisfaction_analysis():
    app_data = {}

    ratings = AppSatisfaction.objects.all()

    app_data['number_of_rating_total'] = ratings.count()
    app_data['average_rating'] = ratings.aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0

    return app_data