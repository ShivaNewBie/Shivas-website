from django.db import models
from django.urls import reverse

from django.contrib.auth.models import User
# Create your models here.
#User model is the parent because when we create a product under the user model we are giving them the same id of the same user who created the product.
#What we pass in the foreignkey will be the parent model.
class Product(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, default=False) #on_delete=models.CASCADE allows me to delete parent. It will also delete the child. Ex of my code. Delete Shiva user in db it will delete the products it created.
    prodname = models.CharField(max_length=255, null=True)
    description = models.CharField(max_length=255, null=True)
    price = models.FloatField(null=True)
    image = models.ImageField(null=True, upload_to='images')
    last_update = models.DateTimeField(auto_now_add = False, auto_now= True, null=True) #last time updated
    timestamps = models.DateTimeField(auto_now_add = True, auto_now= False, null=True) #date created
    likes = models.ManyToManyField(User, related_name='product_post') #A user can like all products he wants to
    def __str__(self):
        return self.prodname + '  |  ' + str(self.creator) + ' | ' + str(self.creator.id)
    @property
    def num_likes(self):
        return self.likes.all().count
    def get_absolute_url(self):
           return reverse("product:product-detail", kwargs={'pk': self.id})


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    prod = models.ForeignKey(Product, related_name='comments',on_delete=models.SET_NULL, null=True)
    description = models.TextField()
    last_update = models.DateTimeField(auto_now_add = False, auto_now= True) #last time updated
    timestamps = models.DateTimeField(auto_now_add = True, auto_now= False) #date created

    def __str__(self):
        return str(self.user)
LIKE_CHOICES = (
    ('Like','Like'),
    ('Unlike', 'Unlike')
)
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Product, on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES, default='Like', max_length=10)



#ManyToManyField all can be related. Say if user_id_1 like product_id_1, user_id_2 can also like product_id_2
