from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import SignupForm, SignupPasswordAgainForm, LoginForm, AccountAddForm, AccountPasswordAgainForm, TemplateCampaignAddForm, TemplateAddTextForm, TemplateAddFileForm, TemplateStaticAddForm
from .models import Users, Accounts, Templates, Texts, Images, Template_types, Sended_accounts, Messages
from django.views.decorators.http import require_GET
from django.views.decorators.http import require_POST

def index(request) :
    return redirect('mypage')

def mypage(request) :
    if not request.session.get('user_id', None) :
        return redirect('login')
    accounts = Accounts.objects.filter(user_id = request.session.get('user_id', None))
    user = Users.objects.get(id = request.session.get('user_id', None))
    if len(accounts) == 0 :
        return redirect('account_add_first')
    if not request.session.get('account_id', None) :
        account_id = accounts[0].id
        request.session['account_id'] = account_id
    messages = Messages.objects.filter(account_id = request.session.get('account_id', None))
    templates = Templates.objects.filter(account_id = request.session.get('account_id', None))
    account_id = request.session.get('account_id', '')
    main_account = get_object_or_404(Accounts, pk=account_id)
    sended_follower = Sended_accounts.objects.filter(account_id = request.session.get('account_id', None), account_level = 1).count()
    sended_fun = Sended_accounts.objects.filter(account_id = request.session.get('account_id', None), account_level = 2).count()
    sended_guest = Sended_accounts.objects.filter(account_id = request.session.get('account_id', None), account_level = 3).count()
    sended_repeater = Sended_accounts.objects.filter(account_id = request.session.get('account_id', None), account_level = 4).count()

    return render(request, 'mypage/home.html', {
        'user': user,
        'main_account': main_account,
        'accounts': accounts,
        'messages': messages,
        'templates': templates,
        'sended_follower': sended_follower,
        'sended_fun': sended_fun,
        'sended_guest': sended_guest,
        'sended_repeater': sended_repeater,
    })

def mypage_process(request, account_id=None) :
    if not request.session.get('user_id', None) :
        return redirect('login')
    accounts = Accounts.objects.filter(user_id = request.session.get('user_id', None))
    ids = []
    for account in accounts :
        ids.append(account.id)
    if account_id :
        if account_id in ids :
            request.session['account_id'] = account_id
            return redirect('mypage')
    return redirect('mypage')

def signup(request) :
    form = SignupForm()
    form_sub = SignupPasswordAgainForm()
    return render(request, 'mypage/signup.html', {
        'page': 'first_form',
        'form': form,
        'form_sub': form_sub,
        'message': request.session.get('message', '')
    })

@require_POST
def signup_process(request) :
    form = SignupForm(request.POST)
    form_sub = SignupPasswordAgainForm(request.POST)
    if form.is_valid() and form_sub.is_valid():
        try :
            user = Users.objects.get(mail = form.cleaned_data['mail'])
            request.session['message'] = 'このメールアドレスは既に使われています。'
            return redirect('signup')
        except :
            if form.cleaned_data['password'] == form_sub.cleaned_data['password2'] :
                request.session['message'] = 'あなたのアカウントが作成されました。ログインして下さい。'
                form.save()
                return redirect('login')
            else :
                request.session['message'] = 'パスワードが一致しません。もう一度入力してください。'
                return redirect('signup')

    else :
        request.session['message'] = ''
        return redirect('signup')

def login(request) :
    form = LoginForm()
    return render(request, 'mypage/login.html', {
        'page': 'first_form',
        'page': 'first_form',
        'form': form,
        'message': request.session.get('message', '')
    })

@require_POST
def login_process(request) :
    form = LoginForm(request.POST)
    if form.is_valid() :
        try :
            user = Users.objects.get(mail = form.cleaned_data['mail'])
        except :
            request.session['message'] = 'メールアドレスが間違っています。'
            return redirect('login')
        if user.password == form.cleaned_data['password'] :
            request.session['user_id'] = user.id
            request.session['message'] = ''
            return redirect('mypage')
        request.session['message'] = 'パスワードが間違っています。'
        return redirect('login')
    else :
        request.session['message'] = ''
        return redirect('signup')

def logout(request) :
    request.session.clear()
    return redirect('index')

def account_add_first(request) :
    if not request.session.get('user_id', None) :
        return redirect('login')
    form = AccountAddForm()
    form_sub = AccountPasswordAgainForm()
    return render(request, 'mypage/account_add_first.html', {
        'page': 'first_form',
        'form': form,
        'form_sub': form_sub,
        'name': request.session.get('login_user_name', '')
    })

@require_POST
def account_add_first_proccess(request) :
    if not request.session.get('user_id', None) :
        return redirect('login')
    form = AccountAddForm(request.POST)
    form_sub = AccountPasswordAgainForm(request.POST)
    if form.is_valid() and form_sub.is_valid() :
        try :
            account = Accounts.objects.get(user_name = form.cleaned_data['user_name'])
            request.session['message'] = 'このインスタグラムアカウントは既に使われています。'
            return redirect('account_add_first')
        except :
            if form.cleaned_data['password'] == form_sub.cleaned_data['password2'] :
                user_id = request.session.get('user_id', '')
                form.save(Users.objects.get(id = user_id))
                request.session['message'] = 'インスタグラムアカウントが追加されました。'
                return redirect('index')
            else :
                request.session['message'] = 'パスワードが一致しません。もう一度入力してください。'
                return redirect('account_add_first')
    else :
        return redirect('account_add_first')

def account_add(request) :
    if not request.session.get('user_id', None) :
        return redirect('login')
    accounts = Accounts.objects.filter(user_id = request.session.get('user_id', None))
    form = AccountAddForm()
    form_sub = AccountPasswordAgainForm()
    main_account = get_object_or_404(Accounts, pk=request.session.get('account_id', None))
    user = Users.objects.get(id = request.session.get('user_id', None))
    return render(request, 'mypage/account_add.html', {
        'form': form,
        'form_sub': form_sub,
        'name': request.session.get('login_user_name', ''),
        'main_account': main_account,
        'accounts': accounts,
        'user': user,
    })

@require_POST
def account_add_proccess(request) :
    if not request.session.get('user_id', None) :
        return redirect('login')
    form = AccountAddForm(request.POST)
    form_sub = AccountPasswordAgainForm(request.POST)
    if form.is_valid() and form_sub.is_valid() :
        try :
            account = Accounts.objects.get(user_name = form.cleaned_data['user_name'])
            request.session['message'] = 'このインスタグラムアカウントは既に使われています。'
            return redirect('account_add')
        except :
            if form.cleaned_data['password'] == form_sub.cleaned_data['password2'] :
                user_id = request.session.get('user_id', '')
                form.save(Users.objects.get(id = user_id))
                request.session['message'] = 'インスタグラムアカウントが追加されました。'
                return redirect('index')
            else :
                request.session['message'] = 'パスワードが一致しません。もう一度入力してください。'
                return redirect('account_add')
    else :
        return redirect('account_add')

def template_index(request) :
    if not request.session.get('user_id', None) :
        return redirect('login')
    template_types = Template_types.objects.all()
    accounts = Accounts.objects.filter(user_id = request.session.get('user_id', None))
    main_account = get_object_or_404(Accounts, pk=request.session.get('account_id', None))
    templates = Templates.objects.filter(account_id = request.session.get('account_id', None))
    user = Users.objects.get(id = request.session.get('user_id', None))
    return render(request, 'mypage/template_index.html', {
        'main_account': main_account,
        'accounts': accounts,
        'template_types': template_types,
        'templates': templates,
        'user': user,
    })

def template_index_process(request, template_type_id) :
    if template_type_id == 1 :
        return redirect('template_follow_add')
    elif template_type_id == 2 :
        return redirect('template_guest_add')
    elif template_type_id == 3 :
        return redirect('template_repeater_add')
    else :
        return redirect('template_campaign_add')

def template_follow_add(request) :
    template_type = Template_types.objects.get(id=1)
    accounts = Accounts.objects.filter(user_id = request.session.get('user_id', None))
    template_add_form = TemplateStaticAddForm()
    template_add_text_form = TemplateAddTextForm()
    template_add_file_form = TemplateAddFileForm()
    main_account = get_object_or_404(Accounts, pk=request.session.get('account_id', None))
    user = Users.objects.get(id = request.session.get('user_id', None))
    return render(request, 'mypage/template_add.html', {
        'template_type': template_type,
        'template_add_form': template_add_form,
        'template_add_text_form': template_add_text_form,
        'template_add_file_form': template_add_file_form,
        'main_account': main_account,
        'accounts': accounts,
        'user': user,
    })

@require_POST
def template_follow_add_proccess(request) :
    if not request.session.get('user_id', None) :
        return redirect('login')
    template_form = TemplateStaticAddForm(request.POST)
    template_text_form = TemplateAddTextForm(request.POST)
    template_file_form = TemplateAddFileForm(request.POST, request.FILES)
    if template_form.is_valid() and template_text_form.is_valid() and template_file_form.is_valid() :
        user_id = request.session.get('user_id', '')
        account_id = request.session.get('account_id', '')
        template_form.save(account_id, 1)
        template_id = Templates.objects.get(name = template_form.cleaned_data['name'])
        template_text_form.save(template_id, 1)
        template_file_form.save(template_id, 2)
        return redirect('template_index')
    else :
        return render(request, 'mypage/template_add.html', {
            'form': form
        })

def template_static_edit(request, template_id) :
    template_static_obj = Templates.objects.get(pk = template_id)
    template_text_obj = Texts.objects.get(template_id = template_id)
    template_image_obj = Images.objects.get(template_id = template_id)
    template_add_form = TemplateStaticAddForm(instance = template_static_obj)
    template_add_text_form = TemplateAddTextForm(instance = template_text_obj)
    template_add_file_form = TemplateAddFileForm(instance = template_image_obj)
    template = Templates.objects.get(pk = template_id)
    main_account = get_object_or_404(Accounts, pk=request.session.get('account_id', None))
    accounts = Accounts.objects.filter(user_id = request.session.get('user_id', None))
    user = Users.objects.get(id = request.session.get('user_id', None))
    return render(request, 'mypage/template_edit.html', {
        'template_id': template_id,
        'template_add_form': template_add_form,
        'template_add_text_form': template_add_text_form,
        'template_add_file_form': template_add_file_form,
        'template': template,
        'main_account': main_account,
        'accounts': accounts,
        'user': user,
    })

@require_POST
def template_static_edit_proccess(request, template_id) :
    if not request.session.get('user_id', None) :
        return redirect('login')
    template_static_obj = Templates.objects.get(pk = template_id)
    template_text_obj = Texts.objects.get(template_id = template_id)
    template_image_obj = Images.objects.get(template_id = template_id)
    template_form = TemplateStaticAddForm(request.POST, instance = template_static_obj)
    template_text_form = TemplateAddTextForm(request.POST, instance = template_text_obj)
    template_file_form = TemplateAddFileForm(request.POST, request.FILES, instance = template_image_obj)
    if template_form.is_valid() and template_text_form.is_valid() and template_file_form.is_valid() :
        user_id = request.session.get('user_id', '')
        account_id = request.session.get('account_id', '')
        template_form.save()
        template_text_form.save()
        template_file_form.save()
        return redirect('template_index')
    else :
        return render(request, 'mypage/template_add.html', {
            'form': form
        })

def template_guest_add(request) :
    template_type = Template_types.objects.get(id=2)
    accounts = Accounts.objects.filter(user_id = request.session.get('user_id', None))
    template_add_form = TemplateStaticAddForm()
    template_add_text_form = TemplateAddTextForm()
    template_add_file_form = TemplateAddFileForm()
    main_account = get_object_or_404(Accounts, pk=request.session.get('account_id', None))
    user = Users.objects.get(id = request.session.get('user_id', None))
    return render(request, 'mypage/template_add.html', {
        'template_type': template_type,
        'template_add_form': template_add_form,
        'template_add_text_form': template_add_text_form,
        'template_add_file_form': template_add_file_form,
        'main_account': main_account,
        'accounts': accounts,
        'user': user,
    })

@require_POST
def template_guest_add_proccess(request) :
    if not request.session.get('user_id', None) :
        return redirect('login')
    template_form = TemplateStaticAddForm(request.POST)
    template_text_form = TemplateAddTextForm(request.POST)
    template_file_form = TemplateAddFileForm(request.POST, request.FILES)
    if template_form.is_valid() and template_text_form.is_valid() and template_file_form.is_valid() :
        user_id = request.session.get('user_id', '')
        account_id = request.session.get('account_id', '')
        template_form.save(account_id, 2)
        template_id = Templates.objects.get(name = template_form.cleaned_data['name'])
        template_text_form.save(template_id, 1)
        template_file_form.save(template_id, 2)
        return redirect('template_index')
    else :
        return render(request, 'mypage/template_add.html', {
            'form': form
        })
def template_repeater_add(request) :
    template_type = Template_types.objects.get(id=3)
    accounts = Accounts.objects.filter(user_id = request.session.get('user_id', None))
    template_add_form = TemplateStaticAddForm()
    template_add_text_form = TemplateAddTextForm()
    template_add_file_form = TemplateAddFileForm()
    main_account = get_object_or_404(Accounts, pk=request.session.get('account_id', None))
    user = Users.objects.get(id = request.session.get('user_id', None))
    return render(request, 'mypage/template_add.html', {
        'template_type': template_type,
        'template_add_form': template_add_form,
        'template_add_text_form': template_add_text_form,
        'template_add_file_form': template_add_file_form,
        'main_account': main_account,
        'accounts': accounts,
        'user': user,
    })

@require_POST
def template_repeater_add_proccess(request) :
    if not request.session.get('user_id', None) :
        return redirect('login')
    template_form = TemplateStaticAddForm(request.POST)
    template_text_form = TemplateAddTextForm(request.POST)
    template_file_form = TemplateAddFileForm(request.POST, request.FILES)
    if template_form.is_valid() and template_text_form.is_valid() and template_file_form.is_valid() :
        user_id = request.session.get('user_id', '')
        account_id = request.session.get('account_id', '')
        template_form.save(account_id, 3)
        template_id = Templates.objects.get(name = template_form.cleaned_data['name'])
        template_text_form.save(template_id, 1)
        template_file_form.save(template_id, 2)
        return redirect('template_index')
    else :
        return render(request, 'mypage/template_add.html', {
            'form': form
        })
def template_campaign_add(request) :
    template_type = Template_types.objects.get(id=4)
    accounts = Accounts.objects.filter(user_id = request.session.get('user_id', None))
    template_add_form = TemplateCampaignAddForm()
    template_add_text_form = TemplateAddTextForm()
    template_add_file_form = TemplateAddFileForm()
    main_account = get_object_or_404(Accounts, pk=request.session.get('account_id', None))
    user = Users.objects.get(id = request.session.get('user_id', None))
    return render(request, 'mypage/template_add.html', {
        'template_type': template_type,
        'template_add_form': template_add_form,
        'template_add_text_form': template_add_text_form,
        'template_add_file_form': template_add_file_form,
        'main_account': main_account,
        'accounts': accounts,
        'user': user,
    })

@require_POST
def template_campaign_add_proccess(request) :
    if not request.session.get('user_id', None) :
        return redirect('login')
    template_form = TemplateCampaignAddForm(request.POST)
    template_text_form = TemplateAddTextForm(request.POST)
    template_file_form = TemplateAddFileForm(request.POST, request.FILES)
    if template_form.is_valid() and template_text_form.is_valid() and template_file_form.is_valid() :
        user_id = request.session.get('user_id', '')
        account_id = request.session.get('account_id', '')
        template_form.save(account_id, 4)
        template_id = Templates.objects.get(name = template_form.cleaned_data['name'])
        template_text_form.save(template_id, 1)
        template_file_form.save(template_id, 2)
        return redirect('template_index')
    else :
        return render(request, 'mypage/template_add.html', {
            'form': form
        })

def follower_show(request) :
    if not request.session.get('user_id', None) :
        return redirect('login')
    sended_accounts = Sended_accounts.objects.filter(account_id = request.session.get('account_id', None))
    accounts = Accounts.objects.filter(user_id = request.session.get('user_id', None))
    main_account = get_object_or_404(Accounts, pk=request.session.get('account_id', None))
    user = Users.objects.get(id = request.session.get('user_id', None))
    return render(request, 'mypage/follower_show.html', {
        'sended_accounts': sended_accounts,
        'main_account': main_account,
        'accounts': accounts,
        'user': user,
    })
