from django.contrib import admin

from .models import Users, Accounts, Account_levels, Templates, Texts, Images, Sended_accounts, Sended_templates, Plans, Template_types, Messages

admin.site.register(Users)
admin.site.register(Accounts)
admin.site.register(Account_levels)
admin.site.register(Templates)
admin.site.register(Texts)
admin.site.register(Images)
admin.site.register(Sended_accounts)
admin.site.register(Sended_templates)
admin.site.register(Plans)
admin.site.register(Template_types)
admin.site.register(Messages)
