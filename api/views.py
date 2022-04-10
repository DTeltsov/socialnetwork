from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User

from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from .serializers import UserSerializer, PostSerializer, PostRateSerializer, UserActivitySerializer
from .models import Post, PostRate, UserActivity


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            composed_perm = AllowAny
            return [composed_perm()]
        return super().get_permissions()

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        instance = self.get_object()
        if instance.id != self.request.user.id:
            return Response({'detail': "You can't update another users info"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.id == self.request.user:
            self.perform_destroy(instance)
        else:
            return Response({'detail': "You can't delete another user"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response(status=status.HTTP_204_NO_CONTENT)


class PostViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(posted_by=self.request.user)

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        instance = self.get_object()
        if instance.posted_by != self.request.user:
            return Response({'detail': "You can't update another users post"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.posted_by == self.request.user:
            self.perform_destroy(instance)
        else:
            return Response({'detail': "You can't delete another users post"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get'], detail=True, permission_classes=[IsAuthenticated])
    def analitics(self, request, pk=None):
        try:
            post = Post.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if post.posted_by == request.user:
            serializer = PostSerializer(post, context={'request':request})
            date_from = request.query_params.get('date_from', None)
            date_to = request.query_params.get('date_to', None)
            likes = post.get_likes_analitics(date_from=date_from, date_to=date_to)
            return Response({'data': serializer.data, 'likes_statistics': likes}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Not your post'},status=status.HTTP_406_NOT_ACCEPTABLE)

    @action(methods=['post'], detail=True, permission_classes=[IsAuthenticated])
    def rate(self, request, pk=None):
        try:
            post = Post.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response({'detail':'Not found'}, status=status.HTTP_404_NOT_FOUND)
        postrate, _ = PostRate.objects.get_or_create(rated_post=post, rated_by=request.user)
        serializer = PostRateSerializer(postrate, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostRateViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = PostRate.objects.all()
    serializer_class = PostRateSerializer
    http_method_names = ['get', 'head']

    def perform_create(self, serializer):
        try:
            postrate = PostRate.objects.get(rated_by=self.request.user, rated_post=self.request.data['rated_post'])
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            post = Post.objects.get(id=self.request.data['rated_post'])
            serializer.save(rated_by=self.request.user, rated_post=post)


class UserActivityViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = UserActivity.objects.all()
    serializer_class = UserActivitySerializer
    http_method_names = ['get', 'head']