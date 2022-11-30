from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Question, Choice, Profile, UserVote
from django.template import loader
from django.urls import reverse
from django.views import generic
# from .forms import RegisterForm
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from .forms import MyUserCreationForm,ProfileForm,ProfileFormWithoutHelpText
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.contrib import messages


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')




def detail(request, question_id,user_id):
    user = User.objects.get(id=user_id)
    question = Question.objects.get(id=question_id)
    uservotes = UserVote.objects.all()
    return render(request, "polls/detail.html", {'question': question,'uservotes':uservotes,'user':user})

def results(request, question_id,user_id):
    question = Question.objects.get(id=question_id)
    user = User.objects.get(id=user_id)
    return render(request, "polls/results.html", {'question': question})


def vote(request, question_id,user_id):
    question = get_object_or_404(Question, id=question_id)
    user = User.objects.get(id=user_id)
    uservotes = UserVote.objects.all()
    choice = Choice.objects.all()
    try:
        selected_choice = question.choice_set.get(id=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        if(uservotes):
            temp = 0
            for users in uservotes:
                if(str(users.question) == str(question_id)):
                    if(str(users.user_id) == str(user.id)):
                        temp += 1
            if(temp != 0):
                return render(request, "polls/results.html", {'question': question})
            else:
                return render(request, 'polls/detail.html', {
                    'question': question,
                    'error_message': 'Вы не сделали выбор'
                })
        else:
            return render(request, 'polls/detail.html', {
                'question': question,
                'error_message': 'Вы не сделали выбор'
            })
    else:
        temp = 0
        if(uservotes):
            for users in uservotes:
                if(str(users.question) == str(question_id)):
                    if(str(users.user_id) == str(user.id)):
                        temp += 1
            if(temp == 0):
                new_uservote = UserVote()
                new_uservote.user_id = user.id
                new_uservote.question = question_id
                new_uservote.save()

                selected_choice.votes += 1
                selected_choice.save()

                all_votes = 0
                for vote in choice:
                    if(vote.question_id==question_id):
                        all_votes += vote.votes
                for vote in choice:
                    if (vote.question_id == question_id):
                        vote.percent = round((vote.votes * 100)/all_votes,2)
                        vote.save()
        else:
            new_uservote = UserVote()
            new_uservote.user_id = user.id
            new_uservote.question = question_id
            new_uservote.save()

            selected_choice.votes += 1
            selected_choice.save()

            all_votes = 0
            for vote in choice:
                if (vote.question_id == question_id):
                    all_votes += vote.votes
            for vote in choice:
                if (vote.question_id == question_id):
                    vote.percent = round((vote.votes * 100) / all_votes)
                    vote.save()

        return render(request, "polls/results.html", {'question': question})


def AuthenticationView(request):
    return render(request, 'registration/authentication.html')


def login(request):
    return render(request, 'registration/login.html')

def account(request):
    return render(request, 'polls/account.html')


class Register(generic.CreateView):
    form_class = MyUserCreationForm
    success_url ='/'
    template_name = 'registration/register.html'


def edit(request, id):
    user = User.objects.get(id=id)
    profile = Profile.objects.get(user_id=id)

    tempImage = str(profile.image)
    tempName = str(user.username)

    form = ProfileFormWithoutHelpText(instance=profile)

    users_list = User.objects.all()

    if request.method == "POST":
        name = request.POST.get("name")
        password = request.POST.get("password")
        form = ProfileFormWithoutHelpText(request.POST, request.FILES,instance=profile)
        if form.is_valid():
            form.save()
        if(name == '' or password == ''):
            messages.error(request, "Имя или пароль не должны быть пустыми")
            return render(request, "registration/edit.html", {"user": user, "form": form})
        if (len(password) <= 7):
            messages.error(request, "Пароль должен быть не короче 8 символов")
            return render(request, "registration/edit.html", {"user": user, "form": form})
        for userss in users_list:
            if (name == userss.username and name != tempName):
                messages.error(request, 'Пользователь ' + str(userss) + ' уже существует')
                return render(request, "registration/edit.html", {"user": user, "form": form})
        else:
            user.username = name
            user.password = make_password(password)

            if (str(profile.image) == tempImage):
                user.profile.image = tempImage
            else:
                user.profile.image = str(profile.image)

            user.save()
            return HttpResponseRedirect("/login/")
    else:
        return render(request, "registration/edit.html", {"user": user, "form": form})

def delete(request, id):
    user = User.objects.get(id=id)

    if request.method == "POST":
        password1 = request.POST.get("password")
        password2 = request.POST.get("password2")

        if (password1 == '' or password2 == ''):
            messages.error(request, "Пароль не должен быть пустыми")
            return render(request, "registration/delete.html", {"user": user})

        if (str(password1) != str(password2)):
            messages.error(request, "Пароли не совпадают")
            return render(request, "registration/delete.html", {"user": user})

        if (check_password(password1, user.password) and check_password(password2, user.password)):
            user.delete()
            return HttpResponseRedirect("/")
        else:
            messages.error(request, "Неправильно введенный пароль")
            return render(request, "registration/delete.html", {"user": user})

    return render(request, "registration/delete.html", {"user": user})



