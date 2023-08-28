import random

from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, DetailView, CreateView, DeleteView, UpdateView

from .filters import *
from .models import *
from .forms import *


class AdsList(ListView):
    model = Ads
    template_name = 'ads.html'
    context_object_name = 'ads'
    ordering = 'Heading'
    paginate_by = 2

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = AdsListSearch(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['filterset'] = self.filterset
        return context


class AdsDetail(DetailView):
    model = Ads
    template_name = 'ads_one.html'
    context_object_name = 'ads_one'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['res'] = Response.objects.filter(ads=self.kwargs['pk'])
        context['res_a'] = Response.objects.filter(ads=self.kwargs['pk']).values('author_id')
        ads = Ads.objects.get(id=self.kwargs['pk'])
        context['user'] = ads.Author
        return context


class StartView(TemplateView):
    template_name = 'start.html'


def logout_user(request):
    logout(request)
    return redirect('start')


class MyAdsList(ListView):
    model = Ads
    template_name = 'ads.html'
    context_object_name = 'ads'
    ordering = 'Heading'
    paginate_by = 2

    def get_queryset(self):
        queryset = Ads.objects.filter(Author=self.request.user)
        self.filterset = MyAdsListSearch(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['filterset'] = self.filterset
        return context


class MyResponses(ListView):
    model = Response
    template_name = 'my_responses.html'
    context_object_name = 'resp'
    ordering = 'Date'
    paginate_by = 4

    def get_queryset(self):
        a = User.objects.get(id=self.request.user.id)
        q = Ads.objects.filter(Author=a)
        queryset = []
        for i in range(0, len(q)):
            qs = Response.objects.filter(ads=q[i])
            queryset += qs
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sum_res'] = len(self.get_queryset())
        context['re'] = Ads.objects.filter(Author=self.request.user)
        q = Ads.objects.filter(Author=self.request.user).values('id')
        sum_ads = 0
        for i in range(0, len(q)):
            if Response.objects.filter(ads=q[i]['id']):
                sum_ads += 1
            else:
                pass
        context['sum_ads'] = sum_ads
        return context


class MyResponsesSearch(ListView):
    model = Response
    template_name = 'my_responses_search.html'
    context_object_name = 're'
    ordering = 'Date'
    paginate_by = 4

    def get_queryset(self):
        user = self.request.user
        queryset = Response.objects.filter(ads__Author=user.id)
        self.filterset = AdsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['filterset'] = self.filterset
        return context


class DeleteResponse(DeleteView):
    model = Response
    success_url = reverse_lazy('my_resp')

    def get(self, *a, **kw):
        return self.delete(*a, **kw)


class AdsCreate(CreateView):
    form_class = AdsCreateForm
    model = Ads
    template_name = 'ads_create.html'
    success_url = reverse_lazy('start')

    def form_valid(self, form):
        u = self.request.user
        a = User.objects.get(username=u)
        form.instance.Author = a
        return super().form_valid(form)


def CheckView(request):
    username = request.user
    c_1 = Code.objects.filter(user=User.objects.get(username=username))
    if not c_1:
        return render(request, 'ads_no_ok')
    else:
        return redirect('ads_create')


class ResponseDetail(LoginRequiredMixin, DetailView):
    model = Response
    template_name = 'resp_one.html'
    context_object_name = 'r'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        author = Response.objects.get(id=self.get_object().id)
        context['author'] = author.ads.Author
        context['user'] = self.request.user
        return context

    def accept(self):
        i = self.META['HTTP_REFERER'].split('/')
        r = Response.objects.get(id=int(i[-1]))
        r.Accepted = True
        r.save()
        user = r.author
        u = User.objects.get(id=user.id)
        a = Ads.objects.get(Heading=r.ads)
        send_mail(
            subject=f'Отклик!',
            message=f'{user}, Ваш отклик на объявление {r.ads} принят продавцом! \n\n'
                    f'Подробнее: http://127.0.0.1:8000/store/ads/{a.id}',
            from_email='Foma26199622@mail.ru',
            recipient_list=[f'{u.email}']
        )
        return HttpResponseRedirect(reverse_lazy('r_det', kwargs={'pk': int(i[-1])}))


class ResponseCreate(LoginRequiredMixin, CreateView):
    form_class = ResponseCreateForm
    model = Response
    template_name = 'resp_create.html'

    def form_valid(self, form):
        u = self.request.user
        a = User.objects.get(username=u)
        form.instance.author = a
        i = self.request.META['HTTP_REFERER'].split('/')
        A = Ads.objects.get(id=int(i[-1]))
        form.instance.ads = A
        form.save()
        author = A.Author
        email = User.objects.get(username=author).email
        result = super().form_valid(form)
        r = self.object.pk
        send_mail(
            subject=f'Отклик!',
            message=f'На ваше объявление {A} оставлен отклик! \n\n'
                    f'Подробнее: http://127.0.0.1:8000/store/response/{r}',
            from_email='Foma26199622@mail.ru',
            recipient_list=[f'{email}']
        )
        return result

    def get_success_url(self):
        return reverse_lazy('ads_one', kwargs={'pk': self.get_object().id})


class Registration_code(CreateView):
    form_class = CodeForm
    template_name = 'code.html'

    def get(self, request, *args, **kwargs):
        u = self.request.user
        if not Code.objects.filter(user=u):
            email = u.email
            c = Code.objects.create(code=random.randint(100000, 999999), user=u)
            send_mail(
                subject=f'Регистрация!',
                message=f'{u}, вот Ваш проверочный код! \n\n '
                        f'{c.code}',
                from_email='Foma26199622@mail.ru',
                recipient_list=[f'{email}']
            )
            return HttpResponse(render(request, 'code.html', context={'form': CodeForm}))
        else:
            return render(request, 'not_code.html')

    def post(self, request, *args, **kwargs):
        username = self.request.user
        c_1 = Code.objects.get(user=User.objects.get(username=username)).code
        if int(self.request.POST['code']) == c_1:
            u = Code.objects.get(code=int(self.request.POST['code']))
            u.is_ok = True
            u.save(update_fields=["is_ok"])
            return render(request, 'r_ok.html')
        else:
            return render(request, 'r_not_ok.html')


class AdsUpdate(LoginRequiredMixin, UpdateView):
    form_class = AdsFormUpdate
    model = Ads
    template_name = 'ads_update.html'

    def get(self, request, *args, **kwargs):
        user = self.request.user
        r = self.get_object()
        author = Ads.objects.get(id=r.id).Author
        if user != author:
            raise PermissionDenied()
        else:
            return HttpResponse(render(request, 'ads_update.html', context={'pk': r.id,
                                                                            'form': AdsFormUpdate(data={
                                                                                'Heading': self.get_object().Heading,
                                                                                'Description':
                                                                                    self.get_object().Description,
                                                                                'Content': self.get_object().Content,
                                                                                'Category': self.get_object().Category
                                                                            })}))

    def get_success_url(self):
        return reverse_lazy('ads_one', kwargs={'pk': self.get_object().id})
