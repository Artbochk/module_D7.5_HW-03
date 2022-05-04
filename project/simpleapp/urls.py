from django.urls import path
from .views import NewsListView, NewsDetail, NewsListSearch, NewsCreateView, NewsEditView, NewsDeleteView, CategoryList, subscribe_me, unsubscribe_me

urlpatterns = [

    path('', NewsListView.as_view()),
    path('<int:pk>', NewsDetail.as_view(), name='news_detail'),
    path('search/', NewsListSearch.as_view(), name='news_search'),
    path('add/', NewsCreateView.as_view(), name='news_create'),
    path('<int:pk>/edit', NewsEditView.as_view(), name='news_edit'),
    path('<int:pk>/delete', NewsDeleteView.as_view(), name='news_delete'),
    path('category/', CategoryList.as_view(), name='category_list'),
    path('category/subscribe/<int:pk>', subscribe_me),
    path('category/unsubscribe/<int:pk>', unsubscribe_me),
    # path('', AppointmentView.as_view(), name='make_appointment'),
]