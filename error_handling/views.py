''' 
    Script responsible for handling HTTP requests, processing data,
    and returning a HTTP response for the error_handling application.
'''
from django.shortcuts import render

# Create your views here.
def custom_400(request, exception=None):
    ''' Custom 400 bad request http error code view. '''
    template = 'error_handling/400.html'
    context = {'exception': exception}
    return render(request, template, context, status=400)

def custom_401(request):
    ''' Custom 401 unauthorized http error code view. '''
    template = 'error_handling/401.html'
    return render(request, template, status=401)

def custom_403(request, exception=None):
    ''' Custom 403 forbidden http error code view. '''
    template = 'error_handling/403.html'
    context = {'exception': exception}
    return render(request, template, context, status=403)

def custom_404(request, exception=None):
    ''' Custom 404 not found http error code view. '''
    template = 'error_handling/404.html'
    context = {'exception': exception}
    return render(request, template, context, status=404)

def custom_405(request, exception=None):
    ''' Custom 405 method not allowed http error code view. '''
    template = 'error_handling/405.html'
    context = {'exception': exception}
    return render(request, template, context, status=405)

def custom_408(request):
    ''' Custom 408 request timeout http error code view. '''
    template = 'error_handling/408.html'
    return render(request, template, status=408)

def custom_500(request):
    '''Custom 500 internal server http error code view. '''
    template = 'error_handling/500.html'
    return render(request, template, status=500)