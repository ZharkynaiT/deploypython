from django.urls import path , include

from rest_framework.routers import DefaultRouter

from .views import ProblemViewSet, ReplyViewSet

router = DefaultRouter()
router.register('problem', ProblemViewSet)
router.register('reply', ReplyViewSet)


urlpatterns = [
    path("", include(router.urls))

]