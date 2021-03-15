from django.db import models
from datetime import datetime, date

class Plans(models.Model) :
    name = models.CharField(
        verbose_name = 'プラン名',
        max_length = 50,
    )

    def __str__(self) :
        return f'{self.id} {self.name}'

class Users(models.Model) :

    plan = models.ForeignKey(Plans, on_delete=models.CASCADE, null=True, blank=True)

    first_name = models.CharField(
        verbose_name = '名前',
        max_length = 20,
    )

    last_name = models.CharField(
        verbose_name = '名字',
        max_length = 20
    )

    mail = models.EmailField(
        verbose_name = 'メールアドレス',
        unique = True,
    )

    password = models.CharField(
        verbose_name = 'パスワード',
        max_length = 30
    )

    created_at = models.DateTimeField(
        verbose_name = '作成日時',
        auto_now_add = True
    )

    updated_at = models.DateTimeField(
        verbose_name = '更新日時',
        auto_now = True
    )

    def __str__(self) :
        return f'{self.id} {self.last_name}{self.first_name}'

class Accounts(models.Model) :
    user = models.ForeignKey(Users, on_delete=models.CASCADE)

    user_name = models.CharField(
        verbose_name = 'ユーザーネーム',
        max_length = 50,
    )

    password = models.CharField(
        verbose_name = 'パスワード',
        max_length = 30
    )

    created_at = models.DateTimeField(
        verbose_name = '作成日時',
        auto_now_add = True
    )

    updated_at = models.DateTimeField(
        verbose_name = '更新日時',
        auto_now = True
    )

    def __str__(self) :
        return f'【{self.user_id}】{self.user_name}'

class Account_levels(models.Model) :
    name = models.CharField(
        verbose_name = 'レベル名',
        max_length = 30,
    )

    created_at = models.DateTimeField(
        verbose_name = '作成日時',
        auto_now_add = True,
    )

    updated_at = models.DateTimeField(
        verbose_name = '更新日時',
        auto_now = True,
    )

    def __str__(self) :
        return f'{self.name}'

class Template_types(models.Model) :
    name = models.CharField(
        verbose_name = 'テンプレートタイプ',
        max_length = 50,
    )

    def __str__(self) :
        return f'{self.name}'

class Templates(models.Model) :
    account = models.ForeignKey(Accounts, on_delete=models.CASCADE)

    account_level = models.ManyToManyField(Account_levels, blank=True)

    template_type = models.ForeignKey(Template_types, on_delete=models.CASCADE, null=True, blank=True)

    name = models.CharField(
        verbose_name = 'テンプレートネーム',
        max_length = 50,
    )

    start_date = models.DateField(
        verbose_name = '開始日',
        blank = True,
        null = True
    )

    end_date = models.DateField(
        verbose_name = '終了日',
        blank = True,
        null = True
    )

    created_at = models.DateTimeField(
        verbose_name = '作成日時',
        auto_now_add = True
    )

    updated_at = models.DateTimeField(
        verbose_name = '更新日時',
        auto_now = True
    )

    valid = models.BooleanField(
        verbose_name = '適用',
        default = True,
    )

    def __str__(self) :
        return f'【{self.account_id}】{self.name} {self.start_date}~{self.end_date}'

class Texts(models.Model) :
    template = models.ForeignKey(Templates, on_delete=models.CASCADE)

    content = models.CharField(
        verbose_name = 'メッセージ',
        max_length = 200,
    )

    number = models.IntegerField(
        verbose_name = '送信順番',
    )

    created_at = models.DateTimeField(
        verbose_name = '作成日時',
        auto_now_add = True
    )

    updated_at = models.DateTimeField(
        verbose_name = '更新日時',
        auto_now = True
    )

    def __str__(self) :
        return f'【{self.template_id}】{self.number}番目 {self.content[:10]}'

class Images(models.Model) :
    template = models.ForeignKey(Templates, on_delete=models.CASCADE)

    file_name = models.FileField(
        verbose_name = '画像',
        blank = True,
        null = True
    )

    number = models.IntegerField(
        verbose_name = '送信順番',
    )

    created_at = models.DateTimeField(
        verbose_name = '作成日時',
        auto_now_add = True,
    )

    updated_at = models.DateTimeField(
        verbose_name = '更新日時',
        auto_now = True,
    )

    def __str__(self) :
        return f'【{self.template_id}】{self.number}番目'


class Sended_accounts(models.Model) :
    account = models.ForeignKey(Accounts, on_delete=models.CASCADE)

    account_level = models.ForeignKey(Account_levels, on_delete=models.CASCADE)

    user_name = models.CharField(
        verbose_name = 'ユーザーネーム',
        max_length = 50,
    )

    created_at = models.DateTimeField(
        verbose_name = '作成日時',
        auto_now_add = True,
    )

    updated_at = models.DateTimeField(
        verbose_name = '更新日時',
        auto_now = True,
    )

    def __str__(self) :
        return f'【{self.account_id}】{self.account_level_id }{self.user_name}'


class Sended_templates(models.Model) :
    sended_account = models.ForeignKey(Sended_accounts, on_delete=models.CASCADE)

    template = models.ForeignKey(Templates, on_delete=models.CASCADE)

    answer = models.BooleanField(
        default = False,
    )

    visit = models.BooleanField(
        default = False,
    )

    created_at = models.DateTimeField(
        verbose_name = '作成日時',
        auto_now_add = True,
    )

    updated_at = models.DateTimeField(
        verbose_name = '更新日時',
        auto_now = True,
    )

    def __str__(self) :
        return f'【{self.template_id}】{self.sended_account_id}'

class Messages(models.Model) :

    account = models.ForeignKey(Accounts, on_delete=models.CASCADE)

    message = models.CharField(
        verbose_name = 'メッセージ',
        max_length = 100,
    )

    link = models.CharField(
        verbose_name = 'リンク先',
        max_length = 100,
        null = True,
        blank = True,
    )

    created_at = models.DateTimeField(
        verbose_name = '作成日時',
        auto_now_add = True,
    )

    updated_at = models.DateTimeField(
        verbose_name = '更新日時',
        auto_now = True,
    )

    def __str__(self) :
        return f'{self.account_id} {self.message}'
