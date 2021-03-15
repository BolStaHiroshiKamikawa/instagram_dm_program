from .models import Users, Accounts, Templates, Texts, Images
from django import forms

class SignupForm(forms.ModelForm) :
    #
    password = forms.CharField(
        label = 'パスワード',
        max_length = 30,
        required = True,
        widget = forms.PasswordInput()
    )

    class Meta :
        model = Users
        fields = ('last_name', 'first_name', 'mail', 'password')

class SignupPasswordAgainForm(forms.Form) :
    password2 = forms.CharField(
        label = 'パスワード（再入力）',
        required = True,
        widget = forms.PasswordInput,
        error_messages = {
            'required': 'パスワード（再入力）は必須です。'
        }
    )

class LoginForm(forms.Form) :
    mail = forms.EmailField(
        label = 'メールアドレス',
        required = True,
        error_messages = {
            'required': 'メールアドレスは必須です。'
        }
    )

    password = forms.CharField(
        label = 'パスワード',
        max_length = 30,
        required = True,
        widget = forms.PasswordInput,
        error_messages = {
            'required': 'メールアドレスは必須です。',
            'max_length': 'パスワードは30文字以内です。'
        }
    )

class AccountAddForm(forms.ModelForm) :

    password = forms.CharField(
        label = 'パスワード',
        max_length = 30,
        required = True,
        widget = forms.PasswordInput(),
    )

    class Meta :
        model = Accounts
        fields = ('user_name', 'password')

    def save(self, user_id, commit=True) :
        topic = super().save(commit=False)
        topic.user = user_id
        if commit :
            topic.save()
        return topic

class AccountPasswordAgainForm(forms.Form) :
    password2 = forms.CharField(
        label = 'パスワード（再入力）',
        required = True,
        widget = forms.PasswordInput,
        error_messages = {
            'required': 'パスワード（再入力）は必須です。'
        }
    )

class TemplateCampaignAddForm(forms.ModelForm) :

    class Meta :
        model = Templates
        fields = ('account_level', 'name', 'start_date', 'end_date', 'valid')

    def save(self, account_id, template_type_id, commit=True) :
        topic = super().save(commit=False)
        topic.account_id = account_id
        topic.template_type_id = template_type_id
        if commit :
            topic.save()
        return topic

class TemplateStaticAddForm(forms.ModelForm) :
    class Meta :
        model = Templates
        fields = ('name', 'valid')

    def save(self, account_id=None, template_type_id=None, commit=True) :
        topic = super().save(commit=False)
        if account_id :
            topic.account_id = account_id
        if template_type_id :
            topic.template_type_id = template_type_id
        if commit :
            topic.save()
        return topic

class TemplateAddTextForm(forms.ModelForm) :

    content = forms.CharField(
        label = '内容',
        widget = forms.Textarea
    )

    class Meta :
        model = Texts
        fields = ('content',)

    def save(self, template_id=None, number=None, commit=True) :
        topic = super().save(commit=False)
        if template_id :
            topic.template = template_id
        if number :
            topic.number = number
        if commit :
            topic.save()
        return topic

class TemplateAddFileForm(forms.ModelForm) :
    class Meta :
        model = Images
        fields = ('file_name',)

    def save(self, template_id=None, number=None, commit=True) :
        topic = super().save(commit=False)
        if template_id :
            topic.template = template_id
        if number :
            topic.number = number
        if commit :
            topic.save()
        return topic
