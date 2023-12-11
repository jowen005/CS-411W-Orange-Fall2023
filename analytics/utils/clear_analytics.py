from django.utils import timezone
from datetime import datetime

from ..models import *


ANALYTIC_MODELS = [GlobalAnalytics, CalorieAnalytics, RestrictionTagAnalytics,
                    AllergiesTagAnalytics, IngredientTagAnalytics, TasteTagAnalytics,
                    CookStyleAnalytics, OverallFilterAnalytics, MenuItemPerformanceAnalytics,
                    AppSatisfactionAnalytics, LocalRestaurantAnalytics, LoginAnalytics, 
                    LoginRecord]


def driver(lower_bound=None):
    if lower_bound is None:
        lower_bound = timezone.make_aware(datetime(1970, 1, 1))

    for AnalyticModel in ANALYTIC_MODELS:
        AnalyticModel.objects.filter(date_stamp__gte=lower_bound).delete()

