from ssme_activities.models import CDS, Temporary, Reporter, Report, Campaign, Beneficiaire, CampaignBeneficiary, CampaignBeneficiaryProduct, ReportBeneficiary, CampaignProduct, Product, ReportProductReception, ReportProductRemainStock
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
	campaign = Campaign.objects.filter(going_on = True)
	
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



def check_if_is_reporter(args):
	concerned_reporter = Reporter.objects.filter(phone_number = args['phone'])
	if len(concerned_reporter) < 1:
		#This person is not in the list of reporters
		args['valide'] = False
		args['info_to_contact'] = "Erreur. Vous ne vous etes pas enregistre pour pouvoir donner des rapports."
		return

	one_concerned_reporter = concerned_reporter[0]
	
	if not one_concerned_reporter.cds:
		#The CDS of this reporter is not known
		args['valide'] = False
		args['info_to_contact'] = "Erreur. Votre CDS n est pas connu dans le systeme."
		return

	args['cds'] = one_concerned_reporter.cds
	args['valide'] = True
	args['info_to_contact'] = " Le cds de ce rapporteur est connu "


def check_date_is_in_camp_period(args):
	'''This function checks if a date is in campaign period.'''

	#expression = r'^((0[1-9])|([1-2][0-9])|(3[01]))-((0[1-9])|(1[0-2]))-[0-9]{4}$'
	expression = r'^((0[1-9])|([1-2][0-9])|(3[01]))((0[1-9])|(1[0-2]))[0-9]{2}$'
	if re.search(expression, args['text'].split(' ')[1]) is None:
		args['valide'] = False
		args['info_to_contact'] = "Erreur. La date indiquee n est pas valide."
		return
	

	sent_date = args['text'].split(' ')[1][0:2]+"-"+args['text'].split(' ')[1][2:4]+"-20"+args['text'].split(' ')[1][4:]

	sent_date_without_dash = sent_date.replace("-","")
	try:
		date_sent = datetime.datetime.strptime(sent_date_without_dash, "%d%m%Y").date()
	except:
		args['valide'] = False
		args['info_to_contact'] = "Erreur. La date indiquee n est pas valide."
		return

	args['sent_date'] =  date_sent

	if (date_sent < args['opened_campaign'].start_date or date_sent > args['opened_campaign'].end_date):
		args['valide'] = False
		args['info_to_contact'] = "Erreur. La date indiquee n est pas dans la periode de la campagne SSME ouverte."
		return

	if date_sent > datetime.datetime.now().date():
		#The reporter must not record a partient who haven't yet come
		args['valide'] = False
		args['info_to_contact'] = "Erreur. La date indiquee n est pas encore arrivee."
		return
	







#------------------------------Bellow functions are common for products-----------------------

def check_number_of_incoming_prod_variables(args):
	''' This function checks if the phone user sends the expected number of of values '''

	the_expected_number_of_values = args['number_of_concerned_products'] + 2

	args['expected_vulues_number'] = the_expected_number_of_values
	if len(args['text'].split(' ')) < the_expected_number_of_values:
		args['valide'] = False
		args['info_to_contact'] = "Vous avez envoye peu de valeurs."
	if len(args['text'].split(' ')) > the_expected_number_of_values:
		args['valide'] = False
		args['info_to_contact'] = "Vous avez envoye beaucoup de valeurs."
	if len(args['text'].split(' ')) == the_expected_number_of_values:
		args['valide'] = True
		args['info_to_contact'] = "Tous vas bien jusqu ici."


def identify_number_of_concerned_products(args):
	''' This function identifies the number of concerned products '''

	#Let's identify number of products for this campaign
	campaign_products = CampaignProduct.objects.filter(campaign = args['opened_campaign'])

	if len(campaign_products) < 1:
		args['valide'] = False
		args['info_to_contact'] = "Erreur admin. Pas de produits lies a la campagne ouverte."
		return

	args['number_of_concerned_products'] = len(campaign_products)


def check_product_values_validity(args):
	''' This function checks if the values sent by the phone user are the expected ones '''

	priority = 1
	
	while ((priority <= args['number_of_concerned_products']) and (priority > 0)):
		value = args['text'].split(' ')[priority+1]
	
		#Let's identify the concerned CampaignProduct
		campaign_product = CampaignProduct.objects.filter(campaign = args['opened_campaign'], order_in_sms = priority)

		if len(campaign_product) < 1:
			args['valide'] = False
			args['info_to_contact'] = "Erreur admin. Pas de produits de priorite "+str(priority)+"."
			priority = -1
		else:
			one_campaign_product = campaign_product[0]

			if not one_campaign_product.product.can_be_fractioned:
				expression = r'^[0-9]+$'
			else:
				expression = r'^([0-9]+.[0-9]+)|([0-9]+)$'

			if re.search(expression, value) is None:
				args['valide'] = False
				args['info_to_contact'] = "Erreur. La valeur envoyee en position "+str(priority)+" n est pas valide."
				priority = -1
			
		priority = priority + 1
	if args['valide']:
		args['info_to_contact'] = "Ok."

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
	''' This function is used to record products quantities received at the begining of a campaign '''
	#Let's identify the opened campaign
	identify_the_opened_campaign(args)
	print(args['valide'])
	if not args['valide']:
		return

	#Let's identify the number of products for this campaign
	identify_number_of_concerned_products(args)
	print(args['valide'])
	if not args['valide']:
		return

	#Let's check if the number of values sent by the phone user is the expected one
	check_number_of_incoming_prod_variables(args)
	print(args['valide'])
	if not args['valide']:
		return

	#Let's check if the person who send this message is a reporter
	check_if_is_reporter(args)
	print(args['valide'])
	if not args['valide']:
		return

	#Let's check if different quantity of products are valid
	check_product_values_validity(args)
	print(args['valide'])
	if not args['valide']:
		return

	#Let's test if the date is valid
	check_date_is_in_camp_period(args)
	print(args['valide'])
	if not args['valide']:
		return

	#Let's record the a beneficiary report
	the_created_report = Report.objects.create(cds = args['cds'], reporting_date = datetime.datetime.now().date(), concerned_date = args['sent_date'], text = args['text'], category = 'STOCK_DEBUT_SEMAINE')

	priority = 1
	
	while (priority <= args['number_of_concerned_products']):
		#We record each beneficiary number
		value = args['text'].split(' ')[priority+1]
	
		prod_camp = CampaignProduct.objects.filter(campaign = args['opened_campaign'], order_in_sms = priority)

		the_concerned_prod_campaign = prod_camp[0]
		
		report_prod = ReportProductReception.objects.create(campaign_product = the_concerned_prod_campaign, reception_date = args['sent_date'], received_quantity = value, report = the_created_report)

		priority = priority + 1
	

#------------------------------------------------------------------








#==================Report SR(Stock Recu)===========================

def record_sr(args):
	''' This function is used to record products quantities received while a campaign is ongoing'''
	#Let's identify the opened campaign
	identify_the_opened_campaign(args)
	print(args['valide'])
	if not args['valide']:
		return

	#Let's identify the number of products for this campaign
	identify_number_of_concerned_products(args)
	print(args['valide'])
	if not args['valide']:
		return

	#Let's check if the number of values sent by the phone user is the expected one
	check_number_of_incoming_prod_variables(args)
	print(args['valide'])
	if not args['valide']:
		return

	#Let's check if the person who send this message is a reporter
	check_if_is_reporter(args)
	print(args['valide'])
	if not args['valide']:
		return

	#Let's check if different quantity of products are valid
	check_product_values_validity(args)
	print(args['valide'])
	if not args['valide']:
		return

	#Let's test if the date is valid
	check_date_is_in_camp_period(args)
	print(args['valide'])
	if not args['valide']:
		return

	#Let's record the a beneficiary report
	the_created_report = Report.objects.create(cds = args['cds'], reporting_date = datetime.datetime.now().date(), concerned_date = args['sent_date'], text = args['text'], category = 'STOCK_RECU')

	priority = 1
	
	while (priority <= args['number_of_concerned_products']):
		#We record each beneficiary number
		value = args['text'].split(' ')[priority+1]
	
		prod_camp = CampaignProduct.objects.filter(campaign = args['opened_campaign'], order_in_sms = priority)

		the_concerned_prod_campaign = prod_camp[0]
		
		report_prod = ReportProductReception.objects.create(campaign_product = the_concerned_prod_campaign, reception_date = args['sent_date'], received_quantity = value, report = the_created_report)

		priority = priority + 1

#------------------------------------------------------------------








#==================Report SF(Stock Final)===========================

def record_sf(args):
	''' This function is used to record remaining products quantities on each day of a campaign '''
	#Let's identify the opened campaign
	identify_the_opened_campaign(args)
	print(args['valide'])
	if not args['valide']:
		return

	#Let's identify the number of products for this campaign
	identify_number_of_concerned_products(args)
	print(args['valide'])
	if not args['valide']:
		return

	#Let's check if the number of values sent by the phone user is the expected one
	check_number_of_incoming_prod_variables(args)
	print(args['valide'])
	if not args['valide']:
		return

	#Let's check if the person who send this message is a reporter
	check_if_is_reporter(args)
	print(args['valide'])
	if not args['valide']:
		return

	#Let's check if different quantity of products are valid
	check_product_values_validity(args)
	print(args['valide'])
	if not args['valide']:
		return

	#Let's test if the date is valid
	check_date_is_in_camp_period(args)
	print(args['valide'])
	if not args['valide']:
		return

	#Let's record the a beneficiary report
	the_created_report = Report.objects.create(cds = args['cds'], reporting_date = datetime.datetime.now().date(), concerned_date = args['sent_date'], text = args['text'], category = 'STOCK_FINAL')

	priority = 1
	
	while (priority <= args['number_of_concerned_products']):
		#We record each beneficiary number
		value = args['text'].split(' ')[priority+1]
	
		prod_camp = CampaignProduct.objects.filter(campaign = args['opened_campaign'], order_in_sms = priority)

		the_concerned_prod_campaign = prod_camp[0]
		
		report_prod = ReportProductRemainStock.objects.create(campaign_product = the_concerned_prod_campaign, concerned_date = args['sent_date'], remain_quantity = value, report = the_created_report)

		priority = priority + 1

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
			camp_ben_products = CampaignBeneficiaryProduct.objects.filter(campaign_beneficiary = campaign_beneficiary)
			if len(camp_ben_products) < 1:
				#The admin didn't define products which will be received by these beneficiaries in the opened campaign
				args['valide'] = False
				args['info_to_contact'] = "Erreur admin. Il y a des beneficiaires dont les produits a recevoir ne sont pas defini."
			number_of_expected_beneficiarie_values = number_of_expected_beneficiarie_values + len(camp_ben_products)

	args['number_of_beneficiries_per_product'] = number_of_expected_beneficiarie_values

	print("Number of concerned beneficiaries")
	print(args['number_of_concerned_beneficiaries'])
	print("Number of beneficiaries per products")
	print(args['number_of_beneficiries_per_product'])


def check_number_of_incoming_variables(args):
	''' This function checks if the phone user sends the expected number of of values '''
	the_expected_number_of_values = args['number_of_concerned_beneficiaries'] + 2
	args['expected_vulues_number'] = the_expected_number_of_values
	if len(args['text'].split(' ')) < the_expected_number_of_values:
		args['valide'] = False
		args['info_to_contact'] = "Vous avez envoye peu de valeurs."
	if len(args['text'].split(' ')) > the_expected_number_of_values:
		args['valide'] = False
		args['info_to_contact'] = "Vous avez envoye beaucoup de valeurs."
	if len(args['text'].split(' ')) == the_expected_number_of_values:
		args['valide'] = True
		args['info_to_contact'] = "Tous vas bien jusqu ici."


def check_beneficiary_values_valid(args):
	''' This function checks if the values sent by the phone user are the one expected '''
	priority = 1
	
	while ((priority <= args['number_of_concerned_beneficiaries']) and (priority > 0)):
		value = args['text'].split(' ')[priority+1]
		expression = r'^[0-9]+$'
		if re.search(expression, value) is None:
			args['valide'] = False
			args['info_to_contact'] = "Erreur. La valeur envoyee en position "+str(priority)+" n est pas valide."
			priority = -1
			return
		priority = priority + 1
	if args['valide']:
		args['info_to_contact'] = "Ok."

def record_beneficiaries(args):
	'''This function is used to record number of beneficiaries'''
	#Let's identify the opened campaign
	identify_the_opened_campaign(args)
	print(args['valide'])
	if not args['valide']:
		return

	#Let's identify the number of concerned beneficiaries
	identify_number_of_concerned_beneficiaries(args)
	print(args['valide'])
	if not args['valide']:
		return

	#Let's check if the phone user sent expected number of values
	check_number_of_incoming_variables(args)
	print(args['valide'])
	if not args['valide']:
		return

	#Let's check if the person who send this message is a reporter
	check_if_is_reporter(args)
	print(args['valide'])
	if not args['valide']:
		return

	#Let's check if different values are valid
	check_beneficiary_values_valid(args)
	print(args['valide'])
	if not args['valide']:
		return

	#Let's test if the date is valid
	check_date_is_in_camp_period(args)
	print(args['valide'])
	if not args['valide']:
		return
	
	#Let's record the a beneficiary report
	the_created_report = Report.objects.create(cds = args['cds'], reporting_date = datetime.datetime.now().date(), concerned_date = args['sent_date'], text = args['text'], category = 'BENEFICIAIRE')

	priority = 1
	
	while (priority <= args['number_of_concerned_beneficiaries']):
		#We record each beneficiary number
		value = args['text'].split(' ')[priority+1]
	
		ben_camp = CampaignBeneficiary.objects.filter(campaign = args['opened_campaign'], order_in_sms = priority)

		the_concerned_ben_campaign = ben_camp[0]
		
		report_ben = ReportBeneficiary.objects.create(campaign_beneficiary = the_concerned_ben_campaign, reception_date = args['sent_date'], received_number = value, report = the_created_report)

		priority = priority + 1
		
#--------------------------------------------------------------------







#===============================Exit=====================================

def exit(args):
	''' This function is used to delete an eventual session when someone want to exit a flow '''
	temporary_session = Temporary.objects.filter(phone_number = args['phone'])
	if len(temporary_session) > 0:
		for session in temporary_session:
			session.delete()
	args['valide'] = True
	args['info_to_contact'] = "Vous etes desormais en dehors du flow."
