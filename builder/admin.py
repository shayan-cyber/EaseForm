from django.contrib import admin
from . models import *
# Register your models here.

admin.site.register(Profile)
admin.site.register(FormParent)
admin.site.register(FormDesign)
admin.site.register(FormObject)
admin.site.register(FormCharacterField)
admin.site.register(FormBigTextField)
admin.site.register(FormIntegerField)
admin.site.register(FormFileField)
admin.site.register(MCQField)
admin.site.register(Choice)

