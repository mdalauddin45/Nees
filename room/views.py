from typing import Any
from .import forms
from django.urls import reverse_lazy
from django.shortcuts import redirect
from .import models
from django.views.generic import DetailView
from .models import Room , RoomPurchase
from django.contrib import messages
from django.views import View
from .forms import ReviewForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

# Create your views here.

class DetailsRoomView(DetailView):
    model = models.Room
    pk_url_kwarg = 'id'
    template_name = 'post_details.html'
    
    def post(self, request, *args, **kwargs):
        post = self.get_object()

        comment_form = ReviewForm(request.POST, book=post, user=request.user)

        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            messages.success(request, 'Your review has been added successfully!')
            return self.get(request, *args, **kwargs)
        else:
            if not RoomPurchase.objects.filter(user=request.user, book=post).exists():
                messages.error(request, 'Can not added your review , if you can give this book review must be purchased it bro')
            return self.get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object
        reviews = post.comments.all()
        review_form= forms.ReviewForm()
            
        context['reviews']= reviews
        context['review_form']= review_form
        return context
    
@method_decorator(login_required, name='dispatch')
class PurchaseView(View):
    def get(self, request, id):
        room = Room.objects.get(id=id)

        if request.user.account.balance < room.price:
            messages.error(request, "Insufficient balance to make the purchase.")
        else:
            purchase = RoomPurchase.objects.create(user=request.user, room=room,before_purchase_balance=request.user.account.balance, after_purchase_balance=request.user.account.balance - room.price )
            request.user.account.balance -= room.price
            request.user.account.save()

            messages.success(request, "Purchase successful. Balance deducted.")
        # send_transaction_email(self.request.user,room.price,"Purchase Message", 'transactions/purchase_email.html' )
        return redirect('profile')

           