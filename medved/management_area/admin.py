from django.contrib import admin
from .models import PrivacyPolicy

# Register your models here.
class PrivacyPolicyAdmin(admin.ModelAdmin):
    list_display = [field.name for field in PrivacyPolicy._meta.fields]
    class Meta:
        model = PrivacyPolicy
        fields = '__all__'

admin.site.register(PrivacyPolicy, PrivacyPolicyAdmin)