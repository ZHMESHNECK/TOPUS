from django.urls import path, re_path
from .views import *
from django.views.decorators.cache import cache_page
from django.conf import settings
from django.conf.urls.static import static

# urlpatterns = [
#     path('', index), #http://127.0.0.1:8000/
#     path('tanks/<int:tank_class>/', categories), #http://127.0.0.1:8000/tanks/1/
#     re_path(r'^archive/(?P<year>[0-9]{4})/', archive)
# ]

urlpatterns = [
    # path('', cache_page(60 * 5)(TankHome.as_view()), name='home'),
    path('',(TankHome.as_view()), name='home'),
    # path('about/', about, name='about'),
    path('addpage/', AddPage.as_view(), name='add_page'),
    path('contact/', ContactFormView.as_view(), name='contact'),
    path('admin/', TankHome.as_view(), name='admin'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('profile', profile, name='profile'),
    path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),
    path('review/<int:pk>/', AddReview.as_view(), name='AddReview'),
    path('category/<slug:cat_slug>/', TankCategory.as_view(), name='category'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
