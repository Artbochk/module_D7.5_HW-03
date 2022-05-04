from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.core.paginator import Paginator
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect
from .models import NewsArticle, Category
from .filters import NewsArticleFilter
from .forms import NewsArticleForm
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.core.mail import send_mail, mail_admins

from django.db.models import signals

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .tasks import notify_users_news


class NewsListView(ListView):
    model = NewsArticle
    ordering = '-news_data'
    template_name = 'simpleapp/news_list.html'
    context_object_name = 'articles'
    paginate_by = 3
    form_class = NewsArticleForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = NewsArticleForm()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
        return super().get(request, *args, **kwargs)


class NewsListSearch(ListView):
    model = NewsArticle
    ordering = '-news_data'
    template_name = 'simpleapp/news_search.html'
    context_object_name = 'articles'
    paginate_by = 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = NewsArticleFilter(self.request.GET, queryset=self.get_queryset())
        return context


class NewsDetail(DetailView):
    model = NewsArticle
    template_name = 'simpleapp/news_detail.html'
    context_object_name = 'article'


class NewsCreateView(PermissionRequiredMixin, CreateView):
    template_name = 'simpleapp/news_create.html'
    form_class = NewsArticleForm
    permission_required = ('simpleapp.add_newsarticle',)


class NewsEditView(PermissionRequiredMixin, UpdateView):
    template_name = 'simpleapp/news_edit.html'
    form_class = NewsArticleForm
    permission_required = ('simpleapp.change_newsarticle',)

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return NewsArticle.objects.get(pk=id)


class NewsDeleteView(DeleteView):
    template_name = 'simpleapp/news_delete.html'
    context_object_name = 'article'
    queryset = NewsArticle.objects.all()
    success_url = '/news/'


class CategoryList(ListView):
    model = Category
    template_name = 'simpleapp/category_list.html'
    context_object_name = 'categories'
    paginate_by = 3


@login_required
def subscribe_me(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    if category not in user.category_set.all():
        category.subscribers.add(user)
        return redirect('/news/category/')


@login_required
def unsubscribe_me(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    if category in user.category_set.all():
        category.subscribers.remove(user)
        return redirect('/news/category/')


def user_post_save(sender, instance, signal, *args, **kwargs):
        # Send email
        notify_users_news.delay(instance.pk)


signals.post_save.connect(user_post_save, sender=NewsArticle)



# @receiver(post_save, sender=Appointment)
# def notify_admin_appointment(sender, instance, created, **kwargs):
#     subject = f'{instance.client_name} {instance.date.strftime("%d %m %Y")}'
#
#     mail_admins(
#         subject=subject,
#         message=instance.message,
#     )


# коннектим наш сигнал к функции обработчику и указываем, к какой именно модели после сохранения привязать функцию
# post_save.connect(notify_admin_appointment, sender=Appointment)


# class AppointmentView(View):
#     def get(self, request, *args, **kwargs):
#         return render(request, 'simpleapp/make_appointment.html', {})
#
#     def post(self, request, *args, **kwargs):
#         appointment = Appointment(
#             date=datetime.strptime(request.POST['date'], '%Y-%m-%d'),
#             client_name=request.POST['client_name'],
#             message=request.POST['message'],
#         )
#         appointment.save()

        # # получаем наш html
        # html_content = render_to_string(
        #     'simpleapp/appointment_created.html',
        #     {
        #         'appointment': appointment,
        #     }
        # )
        #
        # # в конструкторе уже знакомые нам параметры, да? Называются правда немного по другому, но суть та же.
        # msg = EmailMultiAlternatives(
        #     subject=f'{appointment.client_name} {appointment.date.strftime("%Y-%M-%d")}',
        #     body=appointment.message,  # это то же, что и message
        #     from_email='volko.ina@yandex.ru',
        #     to=['artbo4karev@yandex.ru'],  # это то же, что и recipients_list
        # )
        # msg.attach_alternative(html_content, "text/html")  # добавляем html
        #
        # msg.send()  # отсылаем


        # send_mail(
        #     subject=f'{appointment.client_name} {appointment.date.strftime("%Y-%M-%d")}',
        #     # имя клиента и дата записи будут в теме для удобства
        #     message=appointment.message,  # сообщение с кратким описанием проблемы
        #     from_email='volko.ina@yandex.ru',  # здесь указываете почту, с которой будете отправлять (об этом попозже)
        #     recipient_list=['artbo4karev@yandex.ru']  # здесь список получателей. Например, секретарь, сам врач и т. д.
        # )

        # mail_admins(
        #     subject=f'{appointment.client_name} {appointment.date.strftime("%Y-%M-%d")}',
        #     # имя клиента и дата записи будут в теме для удобства
        #     message=appointment.message,  # сообщение с кратким описанием проблемы
        # )
        #
        # return redirect('appointment:make_appointment')