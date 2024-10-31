from rest_framework.routers import DefaultRouter
from app.views import CoursesViewSet
from django.urls import path


router = DefaultRouter()
router.register(r'courses', CoursesViewSet, basename='courses')

urlpatterns = router.urls

# router = DefaultRouter()
# # router.register("courses", CoursesViewSet.as_view(), basename="courses")
# router.register("courses", CoursesViewSet.as_view({
#         'get': 'list',
#         'post': 'create',
#         'put': 'update',
#         'patch': 'partial_update',
#         'delete': 'destroy',
#     }), basename="courses")

