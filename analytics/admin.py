from django.contrib import admin

# Register your models here.
from .models import GlobalAnalytics
admin.site.register(GlobalAnalytics)

from .models import CalorieAnalytics
admin.site.register(CalorieAnalytics)

from .models import RestrictionTagAnalytics
admin.site.register(RestrictionTagAnalytics)

from .models import AllergiesTagAnalytics
admin.site.register(AllergiesTagAnalytics)

from .models import IngredientTagAnalytics
admin.site.register(IngredientTagAnalytics)

from .models import TasteTagAnalytics
admin.site.register(TasteTagAnalytics)

from .models import CookStyleAnalytics
admin.site.register(CookStyleAnalytics)

from .models import OverallFilterAnalytics
admin.site.register(OverallFilterAnalytics)

from .models import MenuItemPerformanceAnalytics
admin.site.register(MenuItemPerformanceAnalytics)

from .models import AppSatisfactionAnalytics
admin.site.register(AppSatisfactionAnalytics)

from .models import LocalRestaurantAnalytics
admin.site.register(LocalRestaurantAnalytics)

from .models import OverallExclusionRecord
admin.site.register(OverallExclusionRecord)

from .models import AllergyTagExclusionRecord
admin.site.register(AllergyTagExclusionRecord)

from .models import IngredientTagExclusionRecord
admin.site.register(IngredientTagExclusionRecord)

from .models import RestrictionTagExclusionRecord
admin.site.register(RestrictionTagExclusionRecord)

from .models import TasteTagExclusionRecord
admin.site.register(TasteTagExclusionRecord)

from .models import LoginAnalytics
admin.site.register(LoginAnalytics)

from .models import LoginRecord
admin.site.register(LoginRecord)