from ssme_activities.models import CDS, Temporary, Reporter, Report, Campaign, Beneficiaire, CampaignBeneficiary, CampaignBeneficiaryProduct
import re
import datetime

def check_number_of_values(args):
	#This function checks if the message sent is composed by an expected number of values
	print("==len(args['text'].split(' '))==")
	print(len(args['text'].split(' ')))
	print(args['text'].split(' '))
	if(args['message_type']=='SELF_REGISTRATION'):
		if len(args['text'].split(' ')) < 3:
			args['valide'] = False
			args['info_to_contact'] = "Vous avez envoye peu de valeurs."
		if len(args['text'].split(' ')) > 3:
			args['valide'] = False
			args['info_to_contact'] = "Vous avez envoye beaucoup de valeurs."
		if len(args['text'].split(' ')) == 3:
			args['valide'] = True
			args['info_to_contact'] = "Le nombre de valeurs envoye est correct."

		

def identify_the_opened_campaign(args):
	'''This function identifies an opened campaign. More than one campaign can not be opened at the same time'''
	campaign = Campaign.objects.filter(open = True)
	
	if len(campaign) < 1:
		#There is no opened campaign
		args['valide'] = False
		args['info_to_contact'] = "Erreur admin. Pas de campagne ouverte."
	if len(campaign) > 1:
		#There is more than one opened campaign
		args['valide'] = False
		args['info_to_contact'] = "Erreur admin. Plusieurs campagnes ouvertes en meme temps."
	if len(campaign) == 1:
		#There is one opened campaign
		campaign = campaign[0]
		args['opened_campaign'] = campaign
		args['valide'] = True
		args['info_to_contact'] = "Tout vas bien."



#------------------------------------------------------------------------------------

#======================reporters self registration==================================


def check_cds(args):
	''' This function checks if the CDS code sent by the reporter exists '''
	the_cds_code = args['text'].split(' ')[1]
	concerned_cds = CDS.objects.filter(code = the_cds_code)
	if (len(concerned_cds) > 0):
		args['valide'] = True
		args['info_to_contact'] = "Le code cds envoye est reconnu."
	else:
		args['valide'] = False
		args['info_to_contact'] = "Le code cds envoye n est pas enregistre dans le systeme."

def check_supervisor_phone_number(args):
	''' This function checks if the phone number of the supervisor is well written '''
	the_supervisor_phone_number = args['text'].split(' ')[2]
	the_supervisor_phone_number_no_space = the_supervisor_phone_number.replace(" ", "")
	expression = r'^(\+?(257)?)((62)|(79)|(71)|(76))([0-9]{6})$'
	print(the_supervisor_phone_number_no_space)
	if re.search(expression, the_supervisor_phone_number_no_space) is None:
		#The phone number is not well written
		args['valide'] = False
		args['info_to_contact'] = "Le numero de telephone du superviseur n est pas bien ecrit."
	else:
		args['valide'] = True
		args['info_to_contact'] = "Le numero de telephone du superviseur est bien ecrit."

'''
def check_supervisor_phone_number_not_for_this_contact(args):
	'This function checks if the contact didn't send his/her phone number in the place of the supervisor phone number'
	print("args['phone']")
	print(args['phone'])
	print("args['phone'][4:]")
	print(args['phone'][4:])
	print("args['text'].split(' ')[2]")
	print(args['text'].split(' ')[2])
	if args['phone'] == args['text'].split(' ')[2] or args['phone'][4:] == args['text'].split(' ')[2]:
		args['valide'] = False
		args['info_to_contact'] = "Erreur. Le numero de telephone du superviseur ne peut pas etre le tien."
	else:
		args['valide'] = True
		args['info_to_contact'] = "Le numero de telephone du superviseur est bien note."
'''

def save_temporary_the_reporter(args):
	same_existing_temp = Temporary.objects.filter(phone_number = args['phone'])
	if len(same_existing_temp) > 0:
		same_existing_temp = same_existing_temp[0]
		same_existing_temp.delete()
		args['valide'] = False
		args['info_to_contact'] = "Vous devriez envoyer le numero de telephone de votre superviseur seulement."
	else:
		the_phone_number = args['phone']

		the_cds_code = args['text'].split(' ')[1]

		cds = CDS.objects.filter(code = the_cds_code)
		if len(cds) > 0:
			the_concerned_cds = cds[0]

			the_supervisor_phone_number = args['text'].split(' ')[2]
			the_supervisor_phone_number_no_space = the_supervisor_phone_number.replace(" ", "")

			if len(the_supervisor_phone_number_no_space) == 8:
				the_supervisor_phone_number_no_space = "+257"+the_supervisor_phone_number_no_space
			if len(the_supervisor_phone_number_no_space) == 11:
				the_supervisor_phone_number_no_space = "+"+the_supervisor_phone_number_no_space

			Temporary.objects.create(phone_number = the_phone_number,cds = the_concerned_cds,supervisor_phone_number = the_supervisor_phone_number_no_space)
			args['valide'] = True
			args['info_to_contact'] = "Merci. Veuillez confirmer le numero du superviseur s il vous plait."

def temporary_record_reporter(args):
	'''This function is used to record temporary a reporter'''
	#Let's check if the message sent is composed by an expected number of values
	check_number_of_values(args)
	if not args['valide']:
		return


	#Let's check if the code of CDS is valid
	check_cds(args)
	if not args['valide']:
		return

	#Let's check is the supervisor phone number is valid
	check_supervisor_phone_number(args)
	if not args['valide']:
		return

	#La ligne ci dessous ne peut pas fonctionner sur les instance Anonimise de RapidPro
	#Let's check if the contact didn't send his/her number in the place of the supervisor number
	#check_supervisor_phone_number_not_for_this_contact(args)
	#if not args['valide']:
		#return

	#Let's temporary save the reporter
	save_temporary_the_reporter(args)


def complete_registration(args):
	the_sup_phone_number = args['text']
	the_sup_phone_number_without_spaces = the_sup_phone_number.replace(" ", "")

	the_existing_temp = Temporary.objects.filter(phone_number = args['phone'])

	if len(the_existing_temp) < 1:
		args['valide'] = False
		args['info_to_contact'] = "Votre message n est pas considere."
	else:
		the_one_existing_temp = the_existing_temp[0]
		#if (the_one_existing_temp.supervisor_phone_number == the_sup_phone_number_without_spaces):
		if (the_sup_phone_number_without_spaces in the_one_existing_temp.supervisor_phone_number) and (len(the_sup_phone_number_without_spaces) >= 8):
			#The confirmation of the phone number of the supervisor pass

			#Let's check if this reporter is not already registered for this CDS
			check_duplication = Reporter.objects.filter(phone_number = the_one_existing_temp.phone_number,cds = the_one_existing_temp.cds)
			if len(check_duplication) > 0:
				#This reporter is doing registration twice on the same CDS
				args['valide'] = False
				args['info_to_contact'] = "Erreur. Vous vous etes deja enregistre sur ce meme CDS. Merci."
				the_one_existing_temp.delete()
				return
	
			#Let's check if this reporter is not already registered
			check_duplication1 = Reporter.objects.filter(phone_number = the_one_existing_temp.phone_number)
			if len(check_duplication1) > 0:
				#This reporter is doing registration twice
				args['valide'] = False
				args['info_to_contact'] = "Erreur. Vous n avez pas le droit de vous enregistrer plus d une seule fois. Merci."
				the_one_existing_temp.delete()
				return

			Reporter.objects.create(phone_number = the_one_existing_temp.phone_number,cds = the_one_existing_temp.cds,supervisor_phone_number = the_one_existing_temp.supervisor_phone_number)

			the_one_existing_temp.delete()

			args['valide'] = True
			args['info_to_contact'] = "Vous vous etes enregistre correctement."
		else:
			the_one_existing_temp.delete()
			args['valide'] = False
			args['info_to_contact'] = "Vous avez envoye le numero de telephone du superviseur de differentes manieres."



#-----------------------------------------------------------------


#==================Report SDS(Stock au Debut de la Semaine)=======

def record_sds(args):
	pass


#------------------------------------------------------------------

#==================Report SR(Stock Recu)===========================

def record_sr(args):
	pass

#------------------------------------------------------------------

#==================Report SF(Stock Final)===========================

def record_sf(args):
	pass

#-------------------------------------------------------------------

#==================Report B(Beneficiaries)===========================

def identify_number_of_concerned_beneficiaries(args):
	''' This function identifies the number of concerned beneficiaries '''

	#Let's identify number of Beneficiaries on this campaign
	campaign_beneficiaries = CampaignBeneficiary.objects.filter(campaign = args['opened_campaign'])

	if len(campaign_beneficiaries) < 1:
		args['valide'] = False
		args['info_to_contact'] = "Erreur admin. Pas de beneficiaires lies a la campagne ouverte."
		return

	args['number_of_concerned_beneficiaries'] = len(campaign_beneficiaries)

	#Let's identify the number of beneficiary/product

	number_of_expected_beneficiarie_values = 0

	for campaign_beneficiary in campaign_beneficiaries:
		if args['valide']:
			camp_ben_products = CampaignBeneficiaryProduct.objects.filter(camapaign_beneficiary = campaign_beneficiary)
			if len(camp_ben_products) < 1:
				#The admin didn't define products which will be received by these beneficiaries in the opened campaign
				args['valide'] = False
				args['info_to_contact'] = "Erreur admin. Il y a des beneficiaires dont les produits a recevoir ne sont pas definis."
			number_of_expected_beneficiarie_values = number_of_expected_beneficiarie_values + len(camp_ben_products)

	args['number_of_beneficiries_per_product'] = number_of_expected_beneficiarie_values

	print("Number of concerned beneficiaries")
	print(args['number_of_concerned_beneficiaries'])
	print("Number of beneficiaries per products")
	print(args['number_of_beneficiries_per_product'])


def check_number_of_incoming_variables(args):
	pass

def record_beneficiaries(args):
	'''This function is used to record number of beneficiaries'''
	#Let's identify the opened campaign
	identify_the_opened_campaign(args)
	print(args['valide'])
	if not args['valide']:
		return

	#Let's identify the opened campaign
	identify_number_of_concerned_beneficiaries(args)
	print(args['valide'])
	if not args['valide']:
		return

	#Let's check if the phone user sent expected number of values
	check_number_of_incoming_variables(args)
	print(args['valide'])
	if not args['valide']:
		return

#--------------------------------------------------------------------
