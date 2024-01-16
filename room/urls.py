from django.urls import path
from .import views

urlpatterns = [
    path('details/<int:id>',views.DetailsRoomView.as_view(), name='details_room'),
    path('purchase/<int:id>/', views.PurchaseView.as_view(), name='purchase_room'),
    path('delete_review/<int:review_id>/', views.delete_review, name='delete_review'),
]