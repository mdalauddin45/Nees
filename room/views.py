from typing import Any
from .import forms
from django.urls import reverse_lazy
from django.views.generic import DetailView
from .models import Room , RoomPurchase
from django.contrib import messages
from django.views import View
from .forms import ReviewForm, ReviewUpdateForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import UserReviews
from django.views.generic.edit import DeleteView,UpdateView
from transactions.views import send_transaction_email

# Create your views here.

class DetailsRoomView(DetailView):
    model = Room
    template_name = 'details_room.html'
    pk_url_kwarg = 'id'
    context_object_name = 'room'

    def post(self, request, *args, **kwargs):
        room = self.get_object()

        comment_form = ReviewForm(request.POST, room=room, user=request.user)

        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.room = room
            new_comment.user = request.user
            new_comment.save()
            messages.success(request, 'Your review has been added successfully!')
            return self.get(request, *args, **kwargs)
        else:
            if not RoomPurchase.objects.filter(user=request.user, room=room).exists():
                messages.error(request, 'Can not added your review , if you can give this room review must be purchased it bro')
            return self.get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room = self.object
        reviews = room.comments.all()
        review_form= forms.ReviewForm()
            
        context['reviews']= reviews
        context['review_form']= review_form
        return context
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.user = self.user
        if commit:
            instance.save()
        return instance
    
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

            messages.success(request, "Room Booked successful. Balance deducted.")
            send_transaction_email(self.request.user,room.price,"Room Booked Message", 'transactions/purchase_email.html' )
            return redirect('profile')
        

class ReviewDeleteView(DeleteView):
    model = UserReviews
    template_name = 'delete_confirm.html' 

    def get_success_url(self):
        messages.success(self.request, 'Review deleted successfully.')
        return reverse_lazy('profile')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user != request.user:
            messages.error(request, 'You do not have permission to delete this review.')
            return redirect('profile')
        return super().dispatch(request, *args, **kwargs)

class ReviewUpdateView(UpdateView):
    model = UserReviews
    form_class = ReviewUpdateForm
    template_name = 'edit_review.html'
    success_url = reverse_lazy('profile')  

    def get_object(self, queryset=None):
        review_id = self.kwargs.get('review_id')
        return get_object_or_404(UserReviews, id=review_id)
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Review updated successfully!')
        return response