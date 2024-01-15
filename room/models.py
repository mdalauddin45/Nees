from django.db import models
from django.contrib.auth.models import User

GUEST_CHOICES = [
    (1, '1 Guest'),
    (2, '2 Guests'),
    (3, '3 Guests'),
    (4, '4 Guests'),
    (5, '5 Guests'),
]

STAR_CHOICES = [
    ('⭐', '⭐'),
    ('⭐⭐', '⭐⭐'),
    ('⭐⭐⭐', '⭐⭐⭐'),
    ('⭐⭐⭐⭐', '⭐⭐⭐⭐'),
    ('⭐⭐⭐⭐⭐', '⭐⭐⭐⭐⭐'),
]

# Create your models here.
class Room(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='media/')
    guest = models.IntegerField(choices=GUEST_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return self.title
    
class UserReviews(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.CharField(max_length=5, choices=STAR_CHOICES)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} on {self.room.title}"
    
class RoomPurchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    purchase_date = models.DateTimeField(auto_now_add=True)
    before_purchase_balance = models.DecimalField(max_digits=10, decimal_places=2)
    after_purchase_balance = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Purchase by {self.user.username} - Room: {self.room.title} - Date: {self.purchase_date}"