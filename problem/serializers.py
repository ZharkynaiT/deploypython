from rest_framework import serializers

from .models import Problem, Reply, Image
from comment.serializers import CommentSerializer


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('image', )


class ProblemSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = Problem
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        action = self.context.get('action')
        if action == 'list':
            representation['replies'] = instance.replies.count()
            representation['comments'] = instance.comments.count()
        elif action == 'retrieve':
            representation['images'] = ImageSerializer(
                instance.images.all(), many=True
            ).data
            representation['replies'] = ReplySerializer(
                instance.replies.all(), many=True
            ).data              #для получения всех / ответov
            representation['comments'] = CommentSerializer(
                instance.comments.all(), many=True
            ).data
        return representation

    def create(self, validated_data):
        request = self.context.get('request')
        image_data = request.FILES
        problem = Problem.objects.create(
            author=request.user,
            **validated_data
        )

        for image in image_data.getlist('image'):     #для получения всех картинок исрользуем метод getlist

            Image.objects.create(
                image=image,
                problem=problem
            )
        return problem


class ReplySerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = Reply
        fields = "__all__"

    def create(self, validated_data):
        request = self.context.get('request')
        reply = Reply.objects.create(
            author=request.user,
            **validated_data
            )
        return reply

#TODO:Комментарии и сериализаторы
#TODO: IsAuthorPermission
#TODO:добавить PermissionMixin в problem.views
#TODO:закончить email.html добавить туда ссылку
#TODO:swagger
#TODO:celery
#TODO:Model Signals
#TODO: восстановление пароля