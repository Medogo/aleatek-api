from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

@csrf_exempt
def get_csrf_token(request):
    response = HttpResponse()
    response['X-CSRFToken'] = get_token(request)
    response['Access-Control-Allow-Origin'] = 'https://argosfront.netlify.app'  # L'URL de votre application React
    # response['Access-Control-Allow-Origin'] = 'http://localhost:3000'  # L'URL de votre application React
    response['Access-Control-Allow-Credentials'] = 'true'
    return response



def get_cuurent_user(request):
    return request.user