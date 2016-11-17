from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.
class User(AbstractBaseUser):
	email = models.EmailField(max_length=255, unique=True)
	cards = models.ManyToManyField("User_Card", related_name="User_Cards")
     	address1 = models.CharField(max_length=255, null=False)	
	address2 = models.CharField(max_length=255, null=False)
        city = models.CharField(max_length=255, null=False)
 	state = models.CharField(max_length=255, null=False)
	zip = models.CharField(max_length=255, null=False)
        country = models.CharField(max_length=255, null=False)
        phone = models.CharField(max_length=255, null=False)
	first_name = models.CharField(max_length=255, null=False)
	middle_name = models.CharField(max_length=255, null=False)
	last_name = models.CharField(max_length=255, null=False)
        created = models.DateTimeField(auto_now=True)
	updated = models.DateTimeField(auto_now_add=True)
  	# marqeta data
	user_token = models.CharField(max_length=255, null=False)
	card_token = models.CharField(max_length=255, null=False)
        # end marqeta data
	objects = BaseUserManager()
	USERNAME_FIELD = "email"
	REQUIRED_FIELDS = ['password']
	
class User_Card(models.Model):
  	user = models.ForeignKey("User", related_name="User_Card_User_Id", null=False)
	customer_id = models.CharField(max_length=255, null=False)
	token = models.CharField(max_length=255, null=False)
	category = models.CharField(max_length=255, null=False)
	card = models.CharField(max_length=255, null=False)
    	cb_global = models.CharField(max_length=255, null=False)
	cb_groceries = models.CharField(max_length=255, null=False)
        cb_wholesale_clubs = models.CharField(max_length=255, null=False)
        cb_amazon = models.CharField(max_length=255, null=True)
        cb_restaurants = models.CharField(max_length=255, null=True)
	cb_gasoline =models.CharField(max_length=255, null=True)
        cb_department_stores = models.CharField(max_length=255, null=True)
 	cb_fee = models.CharField(max_length=255, null=True)
	cb_type = models.CharField(max_length=255, null=True)
	cb_is_default = models.CharField(max_length=255, null=True)
	created = models.DateTimeField( auto_now=True )
	updated = models.DateTimeField( auto_now_add=True )
class User_Card_Transaction(models.Model):
	card = models.ForeignKey("User_Card", related_name="User_Card_Transaction_card", null=False)
	token = models.CharField(max_length=255, null=False)
	amount = models.CharField(max_length=255, null=False)
	created = models.DateTimeField( auto_now=True )

