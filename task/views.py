from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from .models import Task
from django.urls import reverse_lazy
from .days import Days
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from .forms import SearchForm

# Create your views here.
# class IndexView(generic.ListView):
#     model = Task
#     template_name = 'task/index.html'

# HomeView(Topページ)
def IndexView(request):
    days = Days()
    taskModel = {
        # 未完了のタスクかつ、期限を過ぎたタスク
        'tasks' : Task.objects.filter(comp_flg=False, author=request.user.id).order_by('deadline').reverse(),
        # 未完了かつ、期限が一週間以内で期限を過ぎていないタスク
        'nearDeadlineTask' : Task.objects.filter(deadline__lte=days.after1Week, deadline__gte=days.today, comp_flg=False, author=request.user.id).order_by('deadline').reverse(),
        # 未完了且つ、怪訝を過ぎているタスク
        'overDeadlineTask' : Task.objects.filter(comp_flg=False, deadline__lte=days.today, author=request.user.id).order_by('deadline').reverse(),
    }
    return render(request, 'task/index.html', taskModel)

def CompletedView(request):
    taskModel = {
        'tasks' : Task.objects.filter(comp_flg=True, author=request.user.id).order_by('deadline').reverse()
    }
    return render(request, 'task/completed.html', taskModel)

# CreateView
class CreateView(LoginRequiredMixin, generic.edit.CreateView):
    model = Task
    template_name = 'task/create.html'
    fields = ('task', 'priority', 'deadline')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(CreateView, self).form_valid(form)

# UpdateView
class UpdateView(generic.UpdateView):
    model = Task
    template_name = 'task/update.html'
    fields = ('task', 'priority', 'deadline')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != self.request.user:
            raise PermissionDenied('編集権限がありません')
        return super(UpdateView, self).dispatch(request, *args, **kwargs)

# deleteView
class DeleteView(LoginRequiredMixin, generic.edit.DeleteView):
    model = Task
    template_name = 'task/delete.html'
    success_url = reverse_lazy('task:index')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != self.request.user:
            raise PermissionDenied('編集権限がありません')
        return super(DeleteView, self).dispatch(request, *args, **kwargs)

# CompleteView
class CompleteView(LoginRequiredMixin, generic.edit.UpdateView):
    model = Task
    template_name = 'task/complete.html'
    fields = ()

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.author != self.request.user:
            raise PermissionDenied('編集権限がありません')
        return super(CompleteView, self).dispatch(request, *args, **kwargs)

    # タスク完了の処理
    def task_comp(request, pk):
        task = get_object_or_404(Task, id=pk)
        task.comp_flg = True
        task.save()
        return redirect('task:index')

def search(request):
    taskModel = None
    searchForm = SearchForm(request.GET)
    
    if searchForm.is_valid():
        query = searchForm.cleaned_data['task']
        taskModel = {
            'results' : Task.objects.filter(task__icontains=query, author=request.user.id, comp_flg=False)
        }
        return render(request, 'task/search.html', taskModel)

def custom_permission_denied_view(request, exception):
    return render(request, '403.html', {'error_message': str(exception)}, status=403)