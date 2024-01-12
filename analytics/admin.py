from django.contrib import admin

from .models import (
    GlobalAnalytics, CalorieAnalytics, RestrictionTagAnalytics,
    AllergiesTagAnalytics, IngredientTagAnalytics, TasteTagAnalytics,
    CookStyleAnalytics, OverallFilterAnalytics, MenuItemPerformanceAnalytics,
    AppSatisfactionAnalytics, LocalRestaurantAnalytics, OverallExclusionRecord, 
    AllergyTagExclusionRecord, RestrictionTagExclusionRecord,
    IngredientTagExclusionRecord, TasteTagExclusionRecord,
    LoginAnalytics, LoginRecord
)   


admin.site.register(GlobalAnalytics)
admin.site.register(CalorieAnalytics)
admin.site.register(RestrictionTagAnalytics)
admin.site.register(AllergiesTagAnalytics)
admin.site.register(IngredientTagAnalytics)
admin.site.register(TasteTagAnalytics)
admin.site.register(CookStyleAnalytics)
admin.site.register(OverallFilterAnalytics)
admin.site.register(MenuItemPerformanceAnalytics)
admin.site.register(AppSatisfactionAnalytics)
admin.site.register(LocalRestaurantAnalytics)
admin.site.register(OverallExclusionRecord)
admin.site.register(AllergyTagExclusionRecord)
admin.site.register(IngredientTagExclusionRecord)
admin.site.register(RestrictionTagExclusionRecord)
admin.site.register(TasteTagExclusionRecord)
admin.site.register(LoginAnalytics)
admin.site.register(LoginRecord)

