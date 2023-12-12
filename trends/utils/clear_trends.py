from django.utils import timezone
from datetime import datetime

from ..models import *


TREND_MODELS = [CalorieTrends, RestrictionTagTrends, AllergyTagTrends,
                IngredientTagTrends, TasteTagTrends, CookStyleTagTrends,
                MenuItemPerformanceTrends, AppSatisfactionTrends]


def driver(lower_bound=None):
    if lower_bound is None:
        lower_bound = timezone.make_aware(datetime(1970, 1, 1)) # An arbitrarily low datetime

    for TrendModel in TREND_MODELS:
        TrendModel.objects.filter(date_stamp__gte=lower_bound).delete()
