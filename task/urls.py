from django.urls import path
from . import views

app_name = 'task'

urlpatterns = [
    path('', views.IndexView, name='index'),      # 一覧ページ
    path('create', views.CreateView.as_view(), name='create'),     # タスク作成ページ
    path('<int:pk>/update', views.UpdateView.as_view(), name='update'),   # タスク編集ページ
    path('<int:pk>/delete', views.DeleteView.as_view(), name='delete'),   # タスク削除ページ
    path('<int:pk>/comp', views.CompleteView.as_view(), name='comp'),  # タスク完了ページ
    path('<int:pk>/task_comp', views.CompleteView.task_comp, name='task_comp'),   # タスク完了処理
    path('completed', views.CompletedView, name='completed'),     # 完了済みタスクページ
    path('search', views.search, name='search'),    # 検索
]