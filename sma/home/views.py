#! /usr/bin/env python2.7
from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.core.serializers import serialize
from sma.settings import STRIPE_API_KEY,SWG_USER,SWG_KEY,SWG_HEADER,SWG_API
from home.models import User, User_Card
import  requests
import json
from uuid import uuid4


class HomeView(TemplateView):
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        context = {
            'some_dynamic_value': 'This text comes from django view!',
        }
        return self.render_to_response(context)
class RegisterView(TemplateView):
    template_name = "register.html"
    def post(self, request, *args, **kwargs):
	try:

		addr_data = {
			"address1": request.POST['address1'],
			"address2": request.POST['address2'],
			"country": request.POST['country'],
			"city": request.POST['city'],
			"state": request.POST['state'],
			"zip": request.POST['zip'],
			"phone": request.POST['phone'],
			"first_name": request.POST['first_name'],
			"middle_name": request.POST['middle_name'],
			"last_name": request.POST['last_name']
		}
		marqeta_user_data = {
			"active": True,
			"email": request.POST['email'],
			"first_name": request.POST['first_name'],
			"middle_name": request.POST['middle_name'],
			"last_name": request.POST['last_name']
		}
		result = requests.post(SWG_API+'/users', json=marqeta_user_data, headers=SWG_HEADER,
			auth=(SWG_USER, SWG_KEY))
		if not (result.status_code>200 and result.status_code<299):
			raise Exception(result.content)
		user_result = json.loads(result.content)	
		card_product_token = "b6084340-a5a3-4a85-90c3-eb5673c6dee9"	
		user_data = dict(addr_data.items() + dict(email=request.POST['email']).items())
			
	 	recipient_addr = {}

		marqeta_card_data = {
			##"bulk_issuance_token": "",
			##"token": "",
			"user_token":user_result['token'],
			##"fulfillment": {
			##	"shipping": { 
			##		"method": "USPS_REGULAR",
			##		"return_address": addr_data,
			##		"recipient_address": addr_data
			##	 },
			##"card_personalization": "card_personalization"
			##},
			##"reissue_pan_from_card_token": "",
			"card_product_token": card_product_token
		}
		result = requests.post(SWG_API+'/cards', json=marqeta_card_data, headers=SWG_HEADER, 
			auth=(SWG_USER, SWG_KEY))
		
		if not (result.status_code>200 and result.status_code<299):
			raise Exception(result.content)
		card_result = json.loads(result.content)
		user_data['user_token']=user_result['token']
		user_data['card_token']=card_result['token']
		user = User(**user_data)
		user.save()
		request.session['user'] = json.loads(serialize("json", [user]))
		return redirect("/main")
	except Exception,ex:
		content = {
			"error": True,
			"message": repr(ex)
		}
		return self.render_to_response( content )
		
    def get(self, request, *args, **kwargs):
	 context = {}
	 return self.render_to_response(context)
class MainView(TemplateView):
    template_name = "main.html"
    def get(self, request, *args, **kwargs):
	user = User.objects.get(pk=request.session['user'][0]['pk'])
	cards = User_Card.objects.filter(
		 user_id=user.id
	).all()
		
	context = {
		"cards": cards,
		"can_show_cards": True if len(cards)>0  else False,
		"user": user }
	return self.render_to_response(context)
class CreateCardView(TemplateView):
    template_name = "create_card.html"
    def post(self, request, *args, **kwargs):
	 import stripe
	 try:
		 stripe.api_key = STRIPE_API_KEY
		 card_data = {
			'number': request.POST['number'],
			'cvc': request.POST['cvc'],
			'exp_month': request.POST['exp_month'],
			'exp_year': request.POST['exp_year']
		  }
		 token = stripe.Token.create(
			card=card_data )
		 customer = stripe.Customer.create( 
			source=token['id']
		 )
		 ## does a token exist?
		 user_cards = User_Card.objects.filter(
			user_id=request.session['user'][0]['pk'],
			customer_id=customer['id']).count()
		 if user_cards>0:
			raise Exception("Card token exists")
		 user_card = User_Card(user_id=request.session['user'][0]['pk'], 
				customer_id=customer['id'],	
				category="")
		 user_card.save()
		 return redirect("/main")
	 except Exception, ex:
		content = {
			"error": True,
			"message": repr(ex) }
		return self.render_to_response( content )
    def get(self, request, *args, **kwargs):
	 context = {}
	 return self.render_to_response(context)
