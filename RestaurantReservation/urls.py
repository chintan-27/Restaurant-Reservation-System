from django.urls import path
from . import views
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth.views import LoginView,LogoutView
from django.conf import settings
from .forms import UserLoginForm
from django.conf.urls.static import static

urlpatterns = [
    path('', views.IndexView, name="home"),
    path('filter/<type>/<filter>/', views.FilterIndex, name="FilteredHome"),
    path('accounts/login/',LoginView.as_view(authentication_form=UserLoginForm),name="login_url"),
    path('register/',views.registerView,name="register_url"),
    path('registerhotel/',views.registerHotelView,name="register_hotel_url"),
    path('logout/',LogoutView.as_view(next_page='home'),name="logout"),
    path('search/',views.SearchView,name="search"),
    path('rphotos/<restaurant_id>',views.AddRestaurantPhotos,name="ARP"),
    path('cphotos/<restaurant_id>',views.AddCustomerPhotos,name="ACP"),
    path('checkotp/<reservation_id>/<otp>',views.CheckOtp,name="CheckOtp"),
    path('review/<restaurant_id>/',views.ReviewView,name="Review"),
    path('accounts/profile/',views.Dashboard,name="Dashboard"),
    path('search/<day>/<start_time>/<end_time>/<persons>/',views.SelectRestaurant,name="select_restaurant"),
    path('one/<restaurant_id>/<day>/<start_time>/<end_time>/<persons>/',views.CheckAvailabilityOne,name="CheckAvailabilityOne"),
    path('one/<restaurant_id>/',views.OneRestaurant,name="OneRestaurant"),
    path('tables/<restaurant_id>/<day>/<start_time>/<end_time>/<persons>/',views.SelectTables,name="select_restaurant"),
    path('confirm/<restaurant_id>/<day>/<start_time>/<end_time>/<persons>/<tables>',views.ConfirmReservation,name="ConfirmReservation"),
]


urlpatterns+= staticfiles_urlpatterns()
urlpatterns=urlpatterns+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
