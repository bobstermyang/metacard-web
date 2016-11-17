#! /usr/bin/env python2.7
from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.core.serializers import serialize
from sma.settings import STRIPE_API_KEY,SWG_USER,SWG_KEY,SWG_HEADER,SWG_API,CARD_REWARDS
from home.models import User, User_Card, User_Card_Transaction
import  requests
import json
from uuid import uuid4


def get_reward_value(card, reward_key):
	from datetime import datetime
	from re import findall
	now_month = datetime.now().month
	value = getattr(card, reward_key)
	splitted_value = value.split("_")	
	if len(splitted_value)>1:
		if now_month >= int(splitted_value[1]) and now_month <= int(splitted_value[2]):
			return int(splitted_value[0])
		return 0
	return int( value )

def find_best_card(user_cards, cb_type):
	best_card = user_cards[0]
	for i in user_cards:
		val1 = get_reward_value(i, cb_type)
		val2 = get_reward_value(best_card, cb_type)
		if val1 > val2:
			best_card=i
	return best_card

## return all card rewards data
def find_card_by_bin(bin_number):
  	for i in CARD_REWARDS:
	    if i['bin_number']==bin_number:
		return i
	return None
  	

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
	card_ids = cards.values_list('id', flat=True)
	transactions = User_Card_Transaction.objects.filter(card_id__in=card_ids).all()
		
	context = {
		"cards": cards,
		"can_show_cards": True if len(cards)>0  else False,
		"transactions": transactions,
		"can_show_transactions": True if len(transactions)>0 else False,
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

		 # remove any spaces
		 from re import sub	
		 card_number = request.POST['number'].replace(" ", "")
		 bin_number = card_number[0:6]
		 bin_data = find_card_by_bin(bin_number)
		 user_card_details = {
			"card": bin_data['card'],
			"cb_global": bin_data['cb_global'],
			"cb_groceries": bin_data['cb_groceries'],
			"cb_wholesale_clubs": bin_data['cb_wholesale_clubs'],
			"cb_restaurants": bin_data['cb_restaurants'],
			"cb_amazon": bin_data['cb_amazon'],
			"cb_gasoline": bin_data['cb_gasoline'],
			"cb_department_stores": bin_data['cb_department_stores'],
			"cb_type": bin_data['cb_type'],
			"cb_fee": bin_data['cb_fee'],
			"cb_is_default": bin_data['cb_is_default'],
			"user_id": request.session['user'][0]['pk'],
			"customer_id": customer['id'], 
			"category": ""
			 }

		 user_card = User_Card( **user_card_details )
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

class BuyItemView(TemplateView):
	template_name = "buy_item.html"
	def post(self, request, *args, **kwargs):
		try:
			import stripe
			from json import loads
			user_cards = User_Card.objects.filter(
				user_id=request.session['user'][0]['pk'] ).all()
			stripe.api_key =STRIPE_API_KEY
			CHARGE_AMOUNT_CENTS = 100
			CHARGE_AMOUNT_DECIMAL = format(float(CHARGE_AMOUNT_CENTS/100), '.2f')
			CURRENCY = "USD"
			DESCRIPTION ="{} charge for Meqeta example application".format(request.POST['type'].title())
			##marqeta_transaction=  {
			##	"amount": CHARGE_AMOUNT_DECIMAL,
			##	"pin": "",
			##	"mid": "0000",
			##	"card_token": request.session['user'][0]['fields']['card_token'] }
			##response = requests.post(SWG_API+"/simulate/authorization", headers=SWG_HEADER, json=marqeta_transaction )
			##if not (response.status.code>=200 and response.status_code<=299):
			##	raise Exception(response.content)
		
			##transaction_response = loads(response.content)
			if request.POST['type']=="gasoline":
				card = find_best_card(user_cards, "cb_gasoline")
			elif request.POST['type']=="amazon":
				card = find_best_card(user_cards, "cb_amazon")
			elif request.POST['type'] == "department_stores":
				card = find_best_card(user_cards, "cb_department_stores")

			customer = stripe.Customer.retrieve(card.customer_id)
			stripe.Charge.create(**{
				'amount': CHARGE_AMOUNT_CENTS,
				'currency':  CURRENCY,
				'description': DESCRIPTION,
				'customer': customer['id'],
				'card': customer['default_source'] })
			new_user_card_transaction = User_Card_Transaction(
				card=card,
				##token=transactions_response['transaction']['token'],
				amount=CHARGE_AMOUNT_DECIMAL)
			new_user_card_transaction.save()
			content = {
				"message": "Transaction was created" }
			return redirect("/main")
		except Exception, ex:
			content = {
				"message": repr( ex ) } 
			return self.render_to_response(content)
