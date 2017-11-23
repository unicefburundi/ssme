from ssme_activities.models import CDS, Temporary, Reporter, Report, Campaign, CampaignBeneficiary, CampaignBeneficiaryProduct, ReportBeneficiary, CampaignProduct, ReportProductReception, ReportProductRemainStock, ReportStockOut, CampaignCDS, AllSupervisorsOnDistrictLevel, DistrictSupervisor
from django.db.models import Q
import re
import datetime
import requests
import json
from django.conf import settings


def check_number_of_values(args):
    # This function checks if the message sent is composed by an expected number of values
    print("==len(args['text'].split(' '))==")
    print(len(args['text'].split(' ')))
    print(args['text'].split(' '))
    if(args['message_type']=='SELF_REGISTRATION'):
        if len(args['text'].split(' ')) < 3:
            args['valide'] = False
            args['info_to_contact'] = "Erreur. Vous avez envoye peu de valeurs. Veuillez reenvoyer le message corrige."
        if len(args['text'].split(' ')) > 3:
            args['valide'] = False
            args['info_to_contact'] = "Erreur. Vous avez envoye beaucoup de valeurs. Veuillez reenvoyer le message corrige."
        if len(args['text'].split(' ')) == 3:
            args['valide'] = True
            args['info_to_contact'] = "Le nombre de valeurs envoye est correct."
    if(args['message_type']=='RUPTURE_STOCK'):
        if len(args['text'].split(' ')) < 3:
            args['valide'] = False
            args['info_to_contact'] = "Erreur. Vous avez envoye peu de valeurs. Veuillez reenvoyer le message corrige."
        if len(args['text'].split(' ')) > 3:
            args['valide'] = False
            args['info_to_contact'] = "Erreur. Vous avez envoye beaucoup de valeurs. Veuillez reenvoyer le message corrige."
        if len(args['text'].split(' ')) == 3:
            args['valide'] = True
            args['info_to_contact'] = "Le nombre de valeurs envoye est correct."
    if(args['message_type']=='POPULATION_CIBLE'):
        if len(args['text'].split(' ')) < 2:
            args['valide'] = False
            args['info_to_contact'] = "Erreur. Vous avez envoye peu de valeurs. Veuillez reenvoyer le message corrige."
        if len(args['text'].split(' ')) > 2:
            args['valide'] = False
            args['info_to_contact'] = "Erreur. Vous avez envoye beaucoup de valeurs. Veuillez reenvoyer le message corrige."
        if len(args['text'].split(' ')) == 2:
            args['valide'] = True
            args['info_to_contact'] = "Le nombre de valeurs envoye est correct."


def identify_the_opened_campaign(args):
    '''This function identifies an opened campaign. More than one campaign can not be opened at the same time'''
    campaign = Campaign.objects.filter(going_on = True)

    if len(campaign) < 1:
        # There is no opened campaign
        args['valide'] = False
        args['info_to_contact'] = "Erreur admin. Pas de campagne ouverte."
    if len(campaign) > 1:
        # There is more than one opened campaign
        args['valide'] = False
        args['info_to_contact'] = "Erreur admin. Plusieurs campagnes ouvertes en meme temps."
    if len(campaign) == 1:
        # There is one opened campaign
        campaign = campaign[0]
        args['opened_campaign'] = campaign
        args['valide'] = True
        args['info_to_contact'] = "Tout vas bien."



def check_if_is_reporter(args):
    concerned_reporter = Reporter.objects.filter(phone_number = args['phone'])
    if len(concerned_reporter) < 1:
        # This person is not in the list of reporters
        args['valide'] = False
        args['info_to_contact'] = "Erreur. Vous ne vous etes pas enregistre pour pouvoir donner des rapports."
        return

    one_concerned_reporter = concerned_reporter[0]

    if not one_concerned_reporter.cds:
        # The CDS of this reporter is not known
        args['valide'] = False
        args['info_to_contact'] = "Erreur. Votre CDS n est pas connu dans le systeme."
        return

    args['the_sender'] =  one_concerned_reporter
    args['cds'] = one_concerned_reporter.cds
    args['valide'] = True
    args['info_to_contact'] = " Le cds de ce rapporteur est connu "


def check_date_is_in_camp_period(args):
    '''This function checks if a date is in campaign period.'''

    # expression = r'^((0[1-9])|([1-2][0-9])|(3[01]))-((0[1-9])|(1[0-2]))-[0-9]{4}$'
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
        # The reporter must not record a partient who haven't yet come
        args['valide'] = False
        args['info_to_contact'] = "Erreur. La date indiquee n est pas encore arrivee."
        return








# ------------------------------Bellow functions are common for products-----------------------

def check_number_of_incoming_prod_variables(args):
    ''' This function checks if the phone user sends the expected number of of values '''

    the_expected_number_of_values = args['number_of_concerned_products'] + 2

    args['expected_vulues_number'] = the_expected_number_of_values
    if len(args['text'].split(' ')) < the_expected_number_of_values:
        args['valide'] = False
        args['info_to_contact'] = "Erreur. Vous avez envoye peu de valeurs. Veuillez reenvoyer le message corrige."
    if len(args['text'].split(' ')) > the_expected_number_of_values:
        args['valide'] = False
        args['info_to_contact'] = "Erreur. Vous avez envoye beaucoup de valeurs. Veuillez reenvoyer le message corrige."
    if len(args['text'].split(' ')) == the_expected_number_of_values:
        args['valide'] = True
        args['info_to_contact'] = "Tous vas bien jusqu ici."


def identify_number_of_concerned_products(args):
    ''' This function identifies the number of concerned products '''

    # Let's identify number of products for this campaign
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
        # if there is "colon" for french, treat it
        value = value.replace(',','.')
        # Let's identify the concerned CampaignProduct
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

# ------------------------------------------------------------------------------------






# ======================reporters self registration==================================


def check_cds(args):
    ''' This function checks if the CDS code sent by the reporter exists '''
    the_cds_code = args['text'].split(' ')[1]
    concerned_cds = CDS.objects.filter(code = the_cds_code)
    if (len(concerned_cds) > 0):
        args['valide'] = True
        args['info_to_contact'] = "Erreur. Le code cds envoye est reconnu."
    else:
        args['valide'] = False
        args['info_to_contact'] = "Erreur. Le code cds envoye n est pas enregistre dans le systeme."

def check_supervisor_phone_number(args):
    ''' This function checks if the phone number of the supervisor is well written '''
    the_supervisor_phone_number = args['text'].split(' ')[2]
    the_supervisor_phone_number_no_space = the_supervisor_phone_number.replace(" ", "")
    # expression = r'^(\+?(257)?)((62)|(79)|(71)|(76))([0-9]{6})$'
    expression = r'^(\+?(257)?)((61)|(62)|(68)|(69)|(71)|(72)|(75)|(76)|(79))([0-9]{6})$'
    print(the_supervisor_phone_number_no_space)
    if re.search(expression, the_supervisor_phone_number_no_space) is None:
        # The phone number is not well written
        args['valide'] = False
        args['info_to_contact'] = "Erreur. Le numero de telephone du superviseur n est pas bien ecrit."
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
        args['info_to_contact'] = "Erreur. Vous devriez envoyer le numero de telephone de votre superviseur seulement."
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
            args['info_to_contact'] = "Merci. Veuillez confirmer le numero de telephone du superviseur s il vous plait."


def check_has_already_session(args):
    '''This function checks if this contact has a session'''
    same_existing_temp = Temporary.objects.filter(phone_number = args['phone'])
    if len(same_existing_temp) > 0:
        same_existing_temp = same_existing_temp[0]
        same_existing_temp.delete()
        args['valide'] = False
        args['info_to_contact'] = "Erreur. Vous devriez envoyer le numero de telephone de votre superviseur seulement."
    else:
        args['valide'] = True
        args['info_to_contact'] = "Ok."

def temporary_record_reporter(args):
    '''This function is used to record temporary a reporter'''
    # Let's check if this contact has an existing session
    check_has_already_session(args)
    if not args['valide']:
        return

    # Let's check if the message sent is composed by an expected number of values
    check_number_of_values(args)
    if not args['valide']:
        return


    # Let's check if the code of CDS is valid
    check_cds(args)
    if not args['valide']:
        return

    # Let's check is the supervisor phone number is valid
    check_supervisor_phone_number(args)
    if not args['valide']:
        return

    # La ligne ci dessous ne peut pas fonctionner sur les instance Anonimise de RapidPro
    # Let's check if the contact didn't send his/her number in the place of the supervisor number
    # check_supervisor_phone_number_not_for_this_contact(args)
    # if not args['valide']:
        # return

    # Let's temporary save the reporter
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


        # if (the_one_existing_temp.supervisor_phone_number == the_sup_phone_number_without_spaces):
        if (the_sup_phone_number_without_spaces in the_one_existing_temp.supervisor_phone_number) and (len(the_sup_phone_number_without_spaces) >= 8):
            # The confirmation of the phone number of the supervisor pass


            # Let's check if this contact is not registered with this CDS and this supervisor Phone number
            # If it is the case, this contact is doing an unnecessary registration
            check_duplication = Reporter.objects.filter(phone_number = the_one_existing_temp.phone_number, cds = the_one_existing_temp.cds, supervisor_phone_number = the_one_existing_temp.supervisor_phone_number)
            if len(check_duplication) > 0:
                # Already registered and nothing to update
                args['valide'] = False
                args['info_to_contact'] = "Erreur. Vous etes deja enregistre sur ce CDS et avec le meme numero de telephone du superviseur. Envoyer votre rapport ou X pour sortir."
                the_one_existing_temp.delete()
                return

            check_duplication = ''


            # Let's check if the contact wants to update his cds
            check_duplication = Reporter.objects.filter(~Q(cds = the_one_existing_temp.cds), phone_number = the_one_existing_temp.phone_number, supervisor_phone_number = the_one_existing_temp.supervisor_phone_number)
            if len(check_duplication) > 0:
                # this contact wants to update his CDS
                check_duplication = check_duplication[0]
                check_duplication.cds = the_one_existing_temp.cds
                check_duplication.save()
                args['valide'] = True
                args['info_to_contact'] = "Mise a jour du CDS reussie. Votre nouveau CDS est : "+the_one_existing_temp.cds.name
                the_one_existing_temp.delete()
                return

            check_duplication = ''



            # Let's check if the contact wants to update the phone number of his supervisor
            check_duplication = Reporter.objects.filter(~Q(supervisor_phone_number = the_one_existing_temp.supervisor_phone_number), phone_number = the_one_existing_temp.phone_number, cds = the_one_existing_temp.cds)
            if len(check_duplication) > 0:
                # this contact wants to update the phone number of his supervisor
                check_duplication = check_duplication[0]
                check_duplication.supervisor_phone_number = the_one_existing_temp.supervisor_phone_number
                check_duplication.save()
                args['valide'] = True
                args['info_to_contact'] = "Mise a jour reussie. Le nouveau numero de telephone de votre superviseur est : "+the_one_existing_temp.supervisor_phone_number+". Merci."
                the_one_existing_temp.delete()
                return

            check_duplication = ''



            # Let's check if the contact wants to update both the CDS and the phone number of his supervisor
            check_duplication = Reporter.objects.filter(~Q(cds = the_one_existing_temp.cds), ~Q(supervisor_phone_number = the_one_existing_temp.supervisor_phone_number), phone_number = the_one_existing_temp.phone_number)
            if len(check_duplication) > 0:
                # this contact wants to update the phone number of his supervisor
                check_duplication = check_duplication[0]
                check_duplication.cds = the_one_existing_temp.cds
                check_duplication.supervisor_phone_number = the_one_existing_temp.supervisor_phone_number
                check_duplication.save()
                args['valide'] = True
                args['info_to_contact'] = "Mise a jour reussie. Le nouveau numero de votre superviseur est : "+the_one_existing_temp.supervisor_phone_number+" et le nouveau CDS est :"+the_one_existing_temp.cds
                the_one_existing_temp.delete()
                return


            # This contact is doing a first registration. Let's record him/her
            Reporter.objects.create(phone_number = the_one_existing_temp.phone_number,cds = the_one_existing_temp.cds,supervisor_phone_number = the_one_existing_temp.supervisor_phone_number)
            the_one_existing_temp.delete()
            args['valide'] = True
            args['info_to_contact'] = "Vous vous etes enregistre correctement."
        else:
            the_one_existing_temp.delete()
            args['valide'] = False
            args['info_to_contact'] = "Erreur. Vous avez envoye le numero de telephone du superviseur de differentes manieres. Veuillez reenvoyer le message commencant par rg. Merci"



# -----------------------------------------------------------------








# ==================Report SDS(Stock au Debut de la Semaine)=======



def record_sds(args):
    ''' This function is used to record products quantities received at the begining of a campaign '''
    # Let's identify the opened campaign
    identify_the_opened_campaign(args)
    print(args['valide'])
    if not args['valide']:
        return

    # Let's identify the number of products for this campaign
    identify_number_of_concerned_products(args)
    print(args['valide'])
    if not args['valide']:
        return

    # Let's check if the person who send this message is a reporter
    check_if_is_reporter(args)
    print(args['valide'])
    if not args['valide']:
        return

    # Let's check if the number of values sent by the phone user is the expected one
    check_number_of_incoming_prod_variables(args)
    print(args['valide'])
    if not args['valide']:
        return

    # Let's check if different quantity of products are valid
    check_product_values_validity(args)
    print(args['valide'])
    if not args['valide']:
        return

    # Let's test if the date is valid
    check_date_is_in_camp_period(args)
    print(args['valide'])
    if not args['valide']:
        return

    # Let's record the a beneficiary report
    the_created_report, created = Report.objects.get_or_create(cds = args['cds'],  concerned_date = args['sent_date'], category = 'STOCK_DEBUT_SEMAINE')
    the_created_report.text = args['text']
    the_created_report.save()
    priority = 1

    message_to_send = "Le message enregistre est ("

    while (priority <= args['number_of_concerned_products']):
        # We record each beneficiary number
        value = args['text'].split(' ')[priority+1]

        prod_camp = CampaignProduct.objects.filter(campaign = args['opened_campaign'], order_in_sms = priority)

        the_concerned_prod_campaign = prod_camp[0]

        report_prod, created = ReportProductReception.objects.get_or_create(campaign_product = the_concerned_prod_campaign, reception_date = args['sent_date'], report__cds=args['cds'], report__category='STOCK_DEBUT_SEMAINE')
        report_prod.received_quantity, report_prod.report = value.replace(',','.'), the_created_report
        report_prod.save()

        if priority == 1:
            message_to_send = message_to_send+""+the_concerned_prod_campaign.product.name+" : "+value
        else:
            message_to_send = message_to_send+", "+the_concerned_prod_campaign.product.name+" : "+value

        priority = priority + 1

    args['info_to_contact'] = message_to_send+")."
# ------------------------------------------------------------------








# ==================Report SR(Stock Recu)===========================

def record_sr(args):
    ''' This function is used to record products quantities received while a campaign is ongoing'''
    # Let's identify the opened campaign
    identify_the_opened_campaign(args)
    print(args['valide'])
    if not args['valide']:
        return

    # Let's identify the number of products for this campaign
    identify_number_of_concerned_products(args)
    print(args['valide'])
    if not args['valide']:
        return

    # Let's check if the person who send this message is a reporter
    check_if_is_reporter(args)
    print(args['valide'])
    if not args['valide']:
        return

    # Let's check if the number of values sent by the phone user is the expected one
    check_number_of_incoming_prod_variables(args)
    print(args['valide'])
    if not args['valide']:
        return

    # Let's check if different quantity of products are valid
    check_product_values_validity(args)
    print(args['valide'])
    if not args['valide']:
        return

    # Let's test if the date is valid
    check_date_is_in_camp_period(args)
    print(args['valide'])
    if not args['valide']:
        return

    # Let's record the a beneficiary report
    the_created_report, created= Report.objects.get_or_create(cds = args['cds'], concerned_date = args['sent_date'], category = 'STOCK_RECU')
    the_created_report.text = args['text']
    the_created_report.save()

    priority = 1

    message_to_send = "Le message enregistre est ("

    while (priority <= args['number_of_concerned_products']):
        # We record each beneficiary number
        value = args['text'].split(' ')[priority+1]

        prod_camp = CampaignProduct.objects.filter(campaign = args['opened_campaign'], order_in_sms = priority)

        the_concerned_prod_campaign = prod_camp[0]

        if priority == 1:
            message_to_send = message_to_send+""+the_concerned_prod_campaign.product.name+" : "+value
        else:
            message_to_send = message_to_send+", "+the_concerned_prod_campaign.product.name+" : "+value

        report_prod, created= ReportProductReception.objects.get_or_create(campaign_product = the_concerned_prod_campaign, reception_date = args['sent_date'], report__cds = args['cds'], report__category='STOCK_RECU')
        report_prod.received_quantity, report_prod.report = value.replace(',','.'), the_created_report
        report_prod.save()
        priority = priority + 1

    args['info_to_contact'] = message_to_send+")."
# ------------------------------------------------------------------








# ==================Report SF(Stock Final)===========================

def record_sf(args):
    ''' This function is used to record remaining products quantities on each day of a campaign '''
    # Let's identify the opened campaign
    identify_the_opened_campaign(args)
    print(args['valide'])
    if not args['valide']:
        return

    # Let's identify the number of products for this campaign
    identify_number_of_concerned_products(args)
    print(args['valide'])
    if not args['valide']:
        return

    # Let's check if the person who send this message is a reporter
    check_if_is_reporter(args)
    print(args['valide'])
    if not args['valide']:
        return

    # Let's check if the number of values sent by the phone user is the expected one
    check_number_of_incoming_prod_variables(args)
    print(args['valide'])
    if not args['valide']:
        return

    # Let's check if different quantity of products are valid
    check_product_values_validity(args)
    print(args['valide'])
    if not args['valide']:
        return

    # Let's test if the date is valid
    check_date_is_in_camp_period(args)
    print(args['valide'])
    if not args['valide']:
        return

    # Let's record the remaining stock report
    the_created_report, created = Report.objects.get_or_create(cds = args['cds'], concerned_date = args['sent_date'], category = 'STOCK_FINAL')
    the_created_report.text = args['text']
    the_created_report.save()

    priority = 1

    message_to_send = "Le message enregistre est ("

    while (priority <= args['number_of_concerned_products']):
        # We record each beneficiary number
        value = args['text'].split(' ')[priority+1]

        prod_camp = CampaignProduct.objects.filter(campaign = args['opened_campaign'], order_in_sms = priority)

        the_concerned_prod_campaign = prod_camp[0]

        if priority == 1:
            message_to_send = message_to_send+""+the_concerned_prod_campaign.product.name+" : "+value
        else:
            message_to_send = message_to_send+", "+the_concerned_prod_campaign.product.name+" : "+value

        report_prod, created = ReportProductRemainStock.objects.get_or_create(campaign_product = the_concerned_prod_campaign, concerned_date = args['sent_date'],  report__cds= args['cds'])
        report_prod.remain_quantity, report_prod.report = value.replace(',','.'),  the_created_report
        report_prod.save()

        priority = priority + 1

    args['info_to_contact'] = message_to_send+")."
# -------------------------------------------------------------------












# ==================Report B(Beneficiaries)===========================

def identify_number_of_concerned_beneficiaries(args):
    ''' This function identifies the number of concerned beneficiaries '''

    # Let's identify number of Beneficiaries on this campaign
    campaign_beneficiaries = CampaignBeneficiary.objects.filter(campaign = args['opened_campaign'])

    if len(campaign_beneficiaries) < 1:
        args['valide'] = False
        args['info_to_contact'] = "Erreur admin. Pas de beneficiaires lies a la campagne ouverte."
        return

    args['number_of_concerned_beneficiaries'] = len(campaign_beneficiaries)

    # Let's identify the number of beneficiary/product

    number_of_expected_beneficiarie_values = 0

    '''for campaign_beneficiary in campaign_beneficiaries:
        ok = True
        while(ok == True):
            camp_ben_products = CampaignBeneficiaryProduct.objects.filter(campaign_beneficiary = campaign_beneficiary)
            if len(camp_ben_products) < 1:
                ok = False
                args['valide'] = False
                args['info_to_contact'] = "Erreur admin. Il y a des beneficiaires dont les produits a recevoir ne sont pas defini."
            else:'''


    for campaign_beneficiary in campaign_beneficiaries:
        if args['valide']:
            camp_ben_products = CampaignBeneficiaryProduct.objects.filter(campaign_beneficiary = campaign_beneficiary)
            if len(camp_ben_products) < 1:
                # The admin didn't define products which will be received by these beneficiaries in the opened campaign
                args['valide'] = False
                args['info_to_contact'] = "Erreur admin. Il y a des beneficiaires dont les produits a recevoir ne sont pas defini."
            else:
                number_of_expected_beneficiarie_values = number_of_expected_beneficiarie_values + len(camp_ben_products)

    args['number_of_beneficiries_per_product'] = number_of_expected_beneficiarie_values

    print("Number of concerned beneficiaries")
    print(args['number_of_concerned_beneficiaries'])
    print("Number of beneficiaries per products")
    print(args['number_of_beneficiries_per_product'])


def check_number_of_incoming_variables(args):
    ''' This function checks if the phone user sends the expected number of of values '''
    # the_expected_number_of_values = args['number_of_concerned_beneficiaries'] + 2
    the_expected_number_of_values = args['number_of_beneficiries_per_product'] + 2
    args['expected_vulues_number'] = the_expected_number_of_values
    if len(args['text'].split(' ')) < the_expected_number_of_values:
        args['valide'] = False
        args['info_to_contact'] = "Erreur. Vous avez envoye peu de valeurs. Veuillez reenvoyer le message corrige."
    if len(args['text'].split(' ')) > the_expected_number_of_values:
        args['valide'] = False
        args['info_to_contact'] = "Erreur. Vous avez envoye beaucoup de valeurs. Veuillez reenvoyer le message corrige."
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
    # Let's identify the opened campaign
    identify_the_opened_campaign(args)
    print(args['valide'])
    if not args['valide']:
        return

    # Let's identify the number of concerned beneficiaries
    identify_number_of_concerned_beneficiaries(args)
    print(args['valide'])
    if not args['valide']:
        return

    # Let's check if the person who send this message is a reporter
    check_if_is_reporter(args)
    print(args['valide'])
    if not args['valide']:
        return

    # Let's check if the phone user sent expected number of values
    check_number_of_incoming_variables(args)
    print(args['valide'])
    if not args['valide']:
        return

    # Let's check if different values are valid
    check_beneficiary_values_valid(args)
    print(args['valide'])
    if not args['valide']:
        return

    # Let's test if the date is valid
    check_date_is_in_camp_period(args)
    print(args['valide'])
    if not args['valide']:
        return

    # Let's record the a beneficiary report
    the_created_report, created = Report.objects.get_or_create(cds = args['cds'], concerned_date = args['sent_date'],  category = 'BENEFICIAIRE')
    the_created_report.text = args['text']
    the_created_report.save()

    # The below two lines and while code will be removed
    priority = 1
    '''message_to_send = "Le message enregistre est ("

    while (priority <= args['number_of_concerned_beneficiaries']):
        # We record each beneficiary number
        value = args['text'].split(' ')[priority+1]

        ben_camp = CampaignBeneficiary.objects.filter(campaign = args['opened_campaign'], order_in_sms = priority)

        the_concerned_ben_campaign = ben_camp[0]

        if priority == 1:
            message_to_send = message_to_send+""+the_concerned_ben_campaign.beneficiary.designation+" : "+value
        else:
            message_to_send = message_to_send+", "+the_concerned_ben_campaign.beneficiary.designation+" : "+value

        report_ben, created = ReportBeneficiary.objects.get_or_create(campaign_beneficiary = the_concerned_ben_campaign, reception_date = args['sent_date'], report__cds = args['cds'])
        report_ben.received_number, report_ben.report = value, the_created_report
        report_ben.save()
        priority = priority + 1

    args['info_to_contact'] = message_to_send+")."'''



    args['info_to_contact'] = "NULL"

    message_to_send = "Le message enregistre est ("

    # while (priority <= args['number_of_concerned_beneficiaries']):
    while (priority <= args['number_of_beneficiries_per_product']):
        # We record each beneficiary number
        value = args['text'].split(' ')[priority+1]
        camp_ben_prod = CampaignBeneficiaryProduct.objects.filter(campaign_beneficiary__campaign = args['opened_campaign'], order_in_sms = priority)

        the_concerned_camp_ben_prod = camp_ben_prod[0]

        if priority == 1:
            message_to_send = message_to_send+""+the_concerned_camp_ben_prod.campaign_beneficiary.beneficiary.designation+" : "+value
        else:
            message_to_send = message_to_send+", "+the_concerned_camp_ben_prod.campaign_beneficiary.beneficiary.designation+" : "+value

        # The below line will be removed
        the_concerned_ben_campaign = the_concerned_camp_ben_prod.campaign_beneficiary

        report_ben, created = ReportBeneficiary.objects.get_or_create(beneficiaries_per_product = the_concerned_camp_ben_prod, campaign_beneficiary = the_concerned_ben_campaign, reception_date = args['sent_date'], report__cds = args['cds'])
        report_ben.received_number, report_ben.report = value, the_created_report
        report_ben.save()
        priority = priority + 1

    args['info_to_contact'] = message_to_send+")."
# --------------------------------------------------------------------







# ===============================Exit=====================================

def exit(args):
    ''' This function is used to delete an eventual session when someone want to exit a flow '''
    temporary_session = Temporary.objects.filter(phone_number = args['phone'])
    if len(temporary_session) > 0:
        for session in temporary_session:
            session.delete()
    args['valide'] = True
    args['info_to_contact'] = "Vous etes desormais en dehors du flow."

# -------------------------------------------------------------------------








# ================================Report RUP (Rupture du stock)============
def check_stock_out_values_validity(args):
    ''' This function checks if the values sent by the phone user are the expected ones '''

    priority = args['text'].split(' ')[1]
    value = args['text'].split(' ')[2]

    # Let's identify the concerned CampaignProduct
    campaign_product = CampaignProduct.objects.filter(campaign = args['opened_campaign'], order_in_sms = priority)

    if len(campaign_product) < 1:
        args['valide'] = False
        args['info_to_contact'] = "Erreur. Pas de produits de priorite "+str(priority)+". Veuillez reenvoyer le message corrige."
    else:
        one_campaign_product = campaign_product[0]

        if not one_campaign_product.product.can_be_fractioned:
            # value can not be a fraction
            expression = r'^[0-9]+$'
        else:
            # value can be an integer
            expression = r'^([0-9]+.[0-9]+)|([0-9]+)$'

        if re.search(expression, value) is None:
            args['valide'] = False
            args['info_to_contact'] = "Erreur. La quantite restante envoye n est pas valide."

    if args['valide']:
        args['info_to_contact'] = "Ok."


def alert_for_stock_out(args):
    ''' This function alerts in case of a stock out '''
    print("Begin alert_for_stock_out function")
    # url = 'https://api.rapidpro.io/api/v1/broadcasts.json'
    url = 'https://api.rapidpro.io/api/v2/broadcasts.json'
    token = getattr(settings, 'TOKEN', '')

    # Let's first send an alert to the phone number given by this reporter on his registration

    if args['the_sender'].supervisor_phone_number :
        # We have his/her supervisor phone number. Let's send to him/her this message
        the_sup_phone_number = "tel:"+args['the_sender'].supervisor_phone_number
        data = {"urns": [the_sup_phone_number],"text": args['message_to_send_for_alert']}

        print("Before sending alert to a supervisor")
        print(data)

        response = requests.post(url, headers={'Content-type': 'application/json', 'Authorization': 'Token %s' % token}, data = json.dumps(data))
        print("After sending alert to a supervisor")
        print(response.content)


    # Secondly, let's send this alert to all supervisors at the district level who have this CDS in their charge

    the_concerned_district = args['cds'].district
    if not the_concerned_district:
        print("Ce CDS n est pas attache a un district")
        return
    
    concerned_district_supersors = DistrictSupervisor.objects.filter(district = the_concerned_district)
    
    if(len(concerned_district_supersors) < 1):
        # There is not any supervisor linked with this district
        print("There is not any supervisor linked with this district")
        return

    contacts = []

    for district_supervisor in concerned_district_supersors:
        supervisor = district_supervisor.supervisor
        supervisor_phone_number = supervisor.phone_number
        
        supervisor_phone_number = supervisor_phone_number.strip()
        supervisor_phone_number = supervisor_phone_number.replace(" ", "")
        
        if(len(supervisor_phone_number) == 8):
            supervisor_phone_number = "+257"+supervisor_phone_number
        if(len(supervisor_phone_number) == 11):
            supervisor_phone_number = "+"+supervisor_phone_number
        
        supervisor_phone_number = "tel:"+supervisor_phone_number
        contacts.append(supervisor_phone_number)

    data = {"urns": contacts,"text": args['message_to_send_for_alert']}

    response = requests.post(url, headers={'Content-type': 'application/json', 'Authorization': 'Token %s' % token}, data = json.dumps(data))
    print(response.content)



def record_stock_out(args):
    ''' This function is used to record a stock out report '''

    # Let's identify the opened campaign
    identify_the_opened_campaign(args)
    print(args['valide'])
    if not args['valide']:
        return

    # Let's identify the number of products for this campaign
    identify_number_of_concerned_products(args)
    print(args['valide'])
    if not args['valide']:
        return

    # Let's check if the person who send this message is a reporter
    check_if_is_reporter(args)
    print(args['valide'])
    if not args['valide']:
        return

    # Let's check if the message sent is composed by an expected number of values
    check_number_of_values(args)
    if not args['valide']:
        return

    # Let's check if the product priority and remain stock value are valid
    check_stock_out_values_validity(args)
    print(args['valide'])
    if not args['valide']:
        return

    # Let's record a stock out report
    the_created_report = Report.objects.create(cds = args['cds'], reporting_date = datetime.datetime.now().date(), concerned_date = datetime.datetime.now().date(), text = args['text'], category = 'RUPTURE_STOCK')

    # Let's record this stock out report in the model for stock out reports

    priority = args['text'].split(' ')[1]
    value = args['text'].split(' ')[2]

    prod_camp = CampaignProduct.objects.filter(campaign = args['opened_campaign'], order_in_sms = priority)

    if len(prod_camp) < 1:
        args['valide'] = False
        args['info_to_contact'] = "Erreur d enregistrement du rapport de rupture du stock."
        return
    else:
        prod_camp = prod_camp[0]
        stock_out_report_object = ReportStockOut.objects.create(campaign_product = prod_camp, remaining_stock = value.replace(',','.'), report = the_created_report)

        
        args['the_concerned_district_name'] = ""
        the_concerned_district = args['cds'].district
        if not the_concerned_district:
            print("Le CDS "+args['cds'].name+" n est pas attache a un district")
        else:
            args['the_concerned_district_name'] = the_concerned_district.name
            

        args['cds_name'] = args['cds'].name
        args['product_name'] = stock_out_report_object.campaign_product.product.name
        args['remaining_stock'] = value
        args['measuring_unit'] = stock_out_report_object.campaign_product.product.unite_de_mesure
        args['message_to_send_for_alert'] = "Une rupture de stock de "+args['product_name']+" est signalee a "+args['cds_name']+", "+args['the_concerned_district_name']+". La quantite restante est "+args['remaining_stock']+" "+args['measuring_unit']+" ."

        print("cds_name")
        print(args['cds_name'])
        print("product_name")
        print(args['product_name'])
        print("remaining_stock")
        print(args['remaining_stock'])

        args['info_to_contact'] = "Le rapport de rupture de stock de '"+args['product_name']+"', lieu '"+args['cds_name']+"' est bien enregistre."

        # Let's make an alert to the concerned persons
        alert_for_stock_out(args)



# ------------------------------------------------------------------------------------------------------







# ===========================================Population Cible===========================================
def check_beneficiaries_value(args):
    expression = r'^[0-9]+$'
    value = args['text'].split(' ')[1]
    if re.search(expression, value) is None:
        args['valide'] = False
        args['info_to_contact'] = "Erreur. La valeur envoyee pour la population cible n est pas valide."
    else:
        args['valide'] = True
        args['info_to_contact'] = "Le nombre envoye pour la population cible est valide."

def record_population_cible(args):
    ''' This function is used to record 'Population cible' '''

    # Let's identify the opened campaign
    identify_the_opened_campaign(args)
    print(args['valide'])
    if not args['valide']:
        return

    # Let's identify the number of products for this campaign
    identify_number_of_concerned_products(args)
    print(args['valide'])
    if not args['valide']:
        return

    # Let's check if the person who send this message is a reporter
    check_if_is_reporter(args)
    print(args['valide'])
    if not args['valide']:
        return

    # Let's check if the message sent is composed by an expected number of values
    check_number_of_values(args)
    if not args['valide']:
        return

    # Let's check if the number of target beneficiaries is valid
    check_beneficiaries_value(args)
    if not args['valide']:
        return


    # Let's record the target population
    the_cds = args['cds']
    the_campaign = args['opened_campaign']
    value = args['text'].split(' ')[1]

    the_eventuals_existing_camp_cds = CampaignCDS.objects.filter(campaign = the_campaign, cds = the_cds)

    if len(the_eventuals_existing_camp_cds) > 0:
        # There is one or more such CampaignCDS object(s). We update an existing one.
        one_existing_camp_cds = the_eventuals_existing_camp_cds[0]
        one_existing_camp_cds.population_cible = value
        one_existing_camp_cds.save()
    else:
        # It have not been given before. We create it.
        the_new_camp_cds = CampaignCDS.objects.create(campaign = the_campaign, cds = the_cds, population_cible = value)

    args['valide'] = True
    args['info_to_contact'] = "Le message envoye est bien enregistre."

