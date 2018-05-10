from jsonview.decorators import json_view
from django.views.decorators.csrf import csrf_exempt
import re
from django.conf import settings
from ssme_activities.models import  Temporary
from recorders import *
import urllib


def identify_message(args):
	''' This function identifies which kind of message this message is. '''
	incoming_prefix = args['text'].split(' ')[0].upper()
	if args['text'].split(' ')[0].upper() in getattr(settings,'KNOWN_PREFIXES',''):
		#Prefixes and related meanings are stored in the dictionary "KNOWN_PREFIXES"
		args['message_type'] = getattr(settings,'KNOWN_PREFIXES','')[incoming_prefix]
	else:
		args['message_type'] = "UNKNOWN_MESSAGE"

def check_session(args):
	'''This function checks if there is an already created session'''
	reporter_phone_number = args['phone']
	concerned_reporter = Temporary.objects.filter(phone_number = reporter_phone_number)
	if len(concerned_reporter) < 1:
		args['has_session'] = False
	else:
		args['has_session'] = True

def eliminate_unnecessary_spaces(args):
    '''This function eliminate unnecessary spaces in an the incoming message'''
    the_incoming_message = args['text']
    print("The text before sub             "+the_incoming_message)
    #Messages from RapidPro comes with spaces replaced by '+'
    #Let's replace those '+' (one or more) by one space
    the_new_message = re.sub('[+]+',' ',the_incoming_message)
    # Find any comma
    the_new_message = urllib.unquote_plus(the_new_message)
    #Let's eliminate spaces at the begining and the end of the message
    the_new_message = the_new_message.strip()
    print("The text after sub              "+the_new_message)
    args['text'] = the_new_message
    print("The text after sub args['text'] "+args['text'])


@csrf_exempt
@json_view
def handel_rapidpro_request(request):
	'''This function receives requests sent by RapidPro.
	This function send json data to RapidPro as a response.'''
	#We will put all data sent by RapidPro in this variable
	incoming_data = {}

    # Let's put all the incoming data in the dictionary 'incoming_data'
    incoming_data = byteify(json.loads(request.body))

    # Let's assume that the incoming data is valid
    incoming_data['valide'] = True
    incoming_data['info'] = "The default information."

    # Because RapidPro sends the contact phone number in the format "tel:+12345678925"
    # let's get it from incomming_data
    incoming_data['phone'] = incoming_data['contact']['urn'].replace("tel:", "")

    # Let's instantiate the variable this function will return
    response = {}

	#Let's eliminate unnecessary spaces in the incoming message
	eliminate_unnecessary_spaces(incoming_data)

	#Let's check which kind of message this message is.
	identify_message(incoming_data)

	if(incoming_data['message_type']=='UNKNOWN_MESSAGE'):
		#Let's check if this contact is confirming his phone number
		#It means that he has an already created session
		check_session(incoming_data)
		if not(incoming_data['has_session']):
			#This contact doesn't have an already created session
			response['ok'] = False
			response['info_to_contact'] = "Erreur. Le mot qui commence votre message n'est pas reconnu par le systeme. Envoyez un message valide."
			return response
		else:
			#This contact is confirming the phone number of his supervisor
			complete_registration(incoming_data)
			#response['ok'] = False
			response['ok'] = incoming_data['valide']
			response['info_to_contact'] = incoming_data['info_to_contact']
			return response



	if(incoming_data['message_type']=='SELF_REGISTRATION'):
		#The contact who sent the current message is doing self registration  in the group of reporters
		temporary_record_reporter(incoming_data)
	if(incoming_data['message_type']=='STOCK_DEBUT_SEMAINE'):
		#The contact who sent the current message is reporting the stock at the begining of the campaign
		record_sds(incoming_data)
	if(incoming_data['message_type']=='STOCK_RECU'):
		#The contact who sent the current message is reporting a stock reception
		record_sr(incoming_data)
	if(incoming_data['message_type']=='STOCK_FINAL'):
		#The contact who sent the current message is reporting the final stock for one day
		record_sf(incoming_data)
	if(incoming_data['message_type']=='BENEFICIAIRE'):
		#The contact who sent the current message is reporting number of beneficiaries for one day
		record_beneficiaries(incoming_data)
	if(incoming_data['message_type']=='EXIT'):
		#The contact who sent the current message want to exit
		exit(incoming_data)
	if(incoming_data['message_type']=='RUPTURE_STOCK'):
		#The contact who sent the current message want to report a stock out
		record_stock_out(incoming_data)
	if(incoming_data['message_type']=='POPULATION_CIBLE'):
		#The contact who sent the current message want to report a stock out
		record_population_cible(incoming_data)



	if incoming_data['valide'] :
		#The message have been recorded
		response['ok'] = True
	else:
		#The message haven't been recorded
		response['ok'] = False

	response['info_to_contact'] = incoming_data['info_to_contact']

	return response
