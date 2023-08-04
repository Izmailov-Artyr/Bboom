from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Post, User
from .permissions import IsAuthorOrReadOnly
from .serializers import PostSerializer, UserSerializer
from .forms import CreatePostForm
from django.contrib.auth.decorators import login_required


def users_list(request):
    users = User.objects.all()
    return render(request, 'base.html', context={'users': users})


def user_posts(request, pk):
    user = get_object_or_404(User, pk=pk)
    user_posts = Post.objects.select_related('user').filter(user=user)
    return render(request, 'post.html', context={'posts': user_posts})


@login_required
def add_post(request):
    if request.method == 'POST':
        form = CreatePostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('user-posts', post.user.pk)
    else:
        form = CreatePostForm()
        return render(request, 'add_post.html', {'form': form})


@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    context = {'post': post}
    if request.method == 'GET':
        return render(request, 'del_post.html', context)
    elif request.method == 'POST':
        post.delete()
        return redirect('users-list')


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['get'])
    def user_posts(self, request, pk=None):
        posts = Post.objects.filter(user=pk)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)


class UserPostList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_queryset(self):
        user = self.kwargs['user']
        queryset = Post.objects.filter(user_id=user)

        return queryset


class PostDel(generics.RetrieveDestroyAPIView):
    permission_classes = [IsAuthorOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostCreate(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
