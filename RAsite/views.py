from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from users.models import CustomUser, Questionnaire, Chat
from django.utils.safestring import mark_safe
import json

# Create your views here.

def index(request):
    # Отрисовка HTML-шаблона index.html с данными внутри
    #print('kek')
    return render(
        request,
        'index.html',
        context = {'data' : 'ok'},
    )

def wrapper(request):
    return render(
        request,
        'wrapper.html',
        context = {'data' : 'ok'},
    )

def account(request):
    return render(
        request,
        'account.html',
        context = {'data' : 'ok'},
    )

def chat_members(request, id):
    return render(
        request,
        'chat_members.html',
        context = {'data' : 'ok'},
    )

def chats_test(request):
    print('wow')
    return render(
        request,
        'chats_test.html',
        context = {'data' : 'ok'},
    )

def survey(request):
    return render(
        request,
        'survey.html',
        context = {'data' : 'ok'},
    )

def chats(request):
    user = request.user
    #пришел со страницы входа
    if request.POST['from'] == 'login':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email = email, password = password)
        if user is not None:
            login(request, user)
        else:
            # Return an 'invalid login' error message.
            return render(
                request,
                'index.html',
                context = {'data' :  mark_safe(json.dumps('invalid'))}
                )
    
    if user is not None:
        if len(user.questionnaires.all()) == 0:
            if(request.POST['from'] == 'login'):
                return redirect("http://127.0.0.1:8000/questionnaire/")
            #заполнил анкету и отправляет ее нам
            else:
                return register_questionnaire(request)
        else:
            return chatspage(request, user)


@login_required
def register_questionnaire(request):
    user = request.user
    questionnaire = Questionnaire.objects.create(
        user_pk = user.pk,
        landlord_pk = request.POST['landlord_pk'],
        placementValue =  request.POST['placementValue'],
        contractConditionsValue =  request.POST['contractConditionsValue'],
        futureParthershipValue =  request.POST['futureParthershipValue'],
        qualityValue =  request.POST['qualityValue'],
        politenessValue =  request.POST['politenessValue'],
        currentSituationValue =  request.POST['currentSituationValue'],
        communicationValue =  request.POST['communicationValue'],
        recommendationValue =  request.POST['recommendationValue'],
        expectationsValue = request.POST['expectationsValue'],
        safetyValue =  request.POST['safetyValue'],
        review = request.POST['review'],
    )
    user.questionnaires.add(questionnaire)

    return chatspage(request, user)

@login_required
def chatspage(request, user):
    chats_list = []
    if user.is_renter:
        for landlord in user.clients.all():
            chat = landlord.Chat
            #А если чат не нашелся???
            chat_size = len(chat.users.all())
            chats_list.append({ 'chat_name' : chat.name, 'chat_pk': chat.pk, 'landlord_pk' : landlord.pk, 'chat_size' : chat_size})
        #print(chats_list)
        return render(
            request,
            'chats.html',
            context = {'chats_list' : chats_list, 'username' : user.name}
        )

@login_required
def questionnaire(request):
    #нужно передавать pk (имя) арендатора, которое будет отображаться в верху анкеты
    user = request.user
    landlord = user.clients.all()[0]
    return render(
        request,
        'questionnaire.html', context={'landlord_name' : landlord.name}
    )

# {% for key in {{chat}}.keys() %}
#     {if {{key}} == "chat_name" %}
#         <h3>{{value}}</h3>
#     {% endif %}
#     {if {{chat[key]}} == "chat_size" %}
#         <span>{{value}} арендатора, ?? в чате</span>
#     {% endif %}
# {% endfor %}

# @login_required
# def room(request, user_pk):
#     our_user = request.user
#     list = []
#     for chat in our_user.chats.all():
#         list.append( { 'name': chat.name, 'pk' : chat.pk } )
#     return render(request, 'chat/room.html', {
#         'user_pk' : mark_safe(json.dumps(user_pk)),
#         'email' : mark_safe(json.dumps(request.user.email)),
#         'chats' : mark_safe(json.dumps(list))
#     })
