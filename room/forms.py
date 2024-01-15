from django import forms
from .models import Room, UserReviews,RoomPurchase

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        
class ReviewForm(forms.ModelForm):
    class Meta:
        model = UserReviews
        fields = ['body']
        
    def __init__(self, *args, **kwargs):
        self.room = kwargs.pop('room', None)
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()

        user_purchased_or_borrowed = RoomPurchase.objects.filter(user=self.user, room=self.room).exists()

        if not user_purchased_or_borrowed:
            raise forms.ValidationError("You must purchase the Room to leave a review.")

        return cleaned_data