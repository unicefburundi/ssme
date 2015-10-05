from jsonview.decorators import json_view
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@json_view
def handel_rapidpro_request(request):
    #Let's instantiate the variable this function will return
    response = {}
    return response
