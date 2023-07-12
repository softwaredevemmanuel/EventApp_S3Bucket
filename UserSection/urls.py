from django.urls import path, re_path
from . import views
from .views import EventView, EventDetailsView, Booking, PaidEventView, FreeEventView, DateAccendView, DateDecendView, BookView, EventSearchView

urlpatterns = [

    path("", EventView.as_view(), name="user_events_page"),

    path("about_page", views.about, name="about_page"),

    path("search", EventSearchView.as_view(), name="search"),

    path("book", BookView.as_view(), name="book_events_page"),

    path("free-details-url/<int:pk>/", EventDetailsView.as_view(), name="free_event_details_page"),

    path("booking-details-url/", Booking.as_view(), name="booking_event_details"),

    path("paid_event_page/", PaidEventView.as_view(), name="paid_event_page"),

    path("free_event_page/", FreeEventView.as_view(), name="free_event_page"),

    path("accend-date/", DateAccendView.as_view(), name="order_by_date_accend"),

    path("decend-date/", DateDecendView.as_view(), name="order_by_date_decend"),

    path('vote/<int:pk>',views.register,name='vote'),

    path('register-free/<int:pk>',views.register_free,name='register_free'),

    path('<str:ref>/', views.verify_payment, name="verify-payment"),

    path('free/<str:ref>/', views.verify_free_payment, name="freebooking"),

    path('analytics/', views.view_analytics, name="view_analytics")
]
