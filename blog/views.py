from django.shortcuts import reverse
from django.views import generic

from . import forms
from . import models


class PostListView(generic.ListView):
    model = models.Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts_list'

    def get_queryset(self):
        return models.Post.objects.filter(status='pub').order_by('-datetime_modified')


class PostDetailView(generic.DetailView):
    model = models.Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'


class PostCreateView(generic.CreateView):
    form_class = forms.PostForm
    template_name = 'blog/post_create.html'
    context_object_name = 'form'

    def get_success_url(self):
        return reverse('post_list_name')


class PostUpdateView(generic.UpdateView):
    model = models.Post
    form_class = forms.PostForm
    template_name = 'blog/post_create.html'
    context_object_name = 'form'

    def get_success_url(self):
        return reverse('post_detail_name', args=[self.object.pk])


class PostDeleteView(generic.DeleteView):
    model = models.Post
    template_name = 'blog/post_delete.html'
    context_object_name = 'post'

    # success_url = reverse_lazy('post_list_name')

    def get_success_url(self):
        return reverse('post_list_name')

# def post_list_view(request):
#     # posts_list = models.Post.objects.all()
#     posts_list = models.Post.objects.filter(status='pub').order_by('-datetime_modified')
#
#     return render(request, 'blog/post_list.html', {'posts_list': posts_list})
#
#
# def post_detail_view(request, pk):
#     # get post by given id
#     # Primary Key : pk
#
#     # Exception
#
#     # try:
#     #     post = models.Post.objects.get(pk=pk)
#     # except ObjectDoesNotExist:
#     #     post = None
#     #     print('Excepted')
#
#     post = get_object_or_404(models.Post, pk=pk)
#
#     return render(request, 'blog/post_detail.html', {'post': post})
#
#
# def show_form_add_post(request):
#     if request.method == 'POST':  # post request
#         form = forms.PostForm(request.POST)  # send information in variable form
#         if form.is_valid():  # check validation information form
#             form.save()  # save information form user
#             # form = forms.PostForm()  # Clear information form
#             return redirect('post_list_name')  # redirect to page list post
#
#     else:  # get request
#         form = forms.PostForm()  # Create Object class forms.PostForm

# print(request.method)

# print(request.POST.get('title'))

# if request.method == 'POST':
#     print('post request')
#     # send data to database
#     post_title = request.POST.get('title')
#     post_text = request.POST.get('text')
#
#     user = User.objects.all()[0]  # first user in database
#     models.Post.objects.create(title=post_title, text=post_text, author=user, status='pub')
# else:
#     print('get request')

# return render(request, 'blog/post_create.html', context={'form': form})


# /blog/10/update/
# def post_update_view(request, pk):
#     post = get_object_or_404(models.Post, pk=pk)
#     form = forms.PostForm(request.POST or None, instance=post)
#
#     if form.is_valid():
#         # print('hi')
#         form.save()
#         return redirect('post_detail_name', pk=pk)  # redirect to page detail post
#
#     return render(request, 'blog/post_create.html', context={'form': form})


# def post_delete_view(request, pk):
#     post = get_object_or_404(models.Post, pk=pk)
#
#     if request.method == 'POST':
#         post.delete()
#         return redirect('post_list_name')
#     return render(request, "blog/post_delete.html", context={'post': post})
