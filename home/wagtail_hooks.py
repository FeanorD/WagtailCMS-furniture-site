from wagtail.contrib.modeladmin.options import (
    ModelAdmin, ModelAdminGroup, modeladmin_register)

from home.models import FooterText, HomePageSlides

class FooterTextAdmin(ModelAdmin):
    model = FooterText

class SlidesAdmin(ModelAdmin):
    model = HomePageSlides

class FeatureModelAdminGroup(ModelAdminGroup):
    menu_label = 'Слайдшоу и футер'
    menu_icon = 'fa-cutlery'  # change as required
    menu_order = 300  # will put in 4th place (000 being 1st, 100 2nd)
    items = (SlidesAdmin, FooterTextAdmin)

modeladmin_register(FeatureModelAdminGroup)