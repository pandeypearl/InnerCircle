''' 
    Script responsible for handling HTTP requests, processing data,
    and returning a HTTP response for the assistant application.
'''
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import openai
from django.conf import settings
from .models import Chat
from django.utils import timezone


openapi_api_key = settings.OPENAI_API_KEY
openai.api_key = openapi_api_key

def ask_openai(message):
    ''' OpenAI chatbot setup. '''
    response = openai.Completion.create(
        model = "text-davinci-003",
        prompt = message,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.7,
    )

    answer = response.choices[0].text.strip()
    return answer

# Create your views here.
login_required(login_url='signIn')
def assistant(request):
    ''' User chat view. '''
    template = 'assistant/assistant.html'
    today = timezone.now().date()
    chats = Chat.objects.filter(user=request.user, created_at__date=today).order_by('-created_at')

    if request.method == 'POST':
        message = request.POST.get('message')
        response = ask_openai(message)

        chat = Chat(user=request.user, message=message, response=response, created_at=timezone.now())
        chat.save()
        return JsonResponse({'message': message, 'response': response})
    context = {
        'chats': chats
    }

    return render(request, template, context)

login_required(login_url='signIn')
def chat_history(request):
    ''' User chat history view. '''
    template = 'assistant/chat_history.html'

    chats = Chat.objects.filter(user=request.user).order_by('-created_at')

    context = {
        'chats': chats,
    }

    return render(request, template, context)
