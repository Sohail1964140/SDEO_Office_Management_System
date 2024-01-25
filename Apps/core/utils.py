from django.shortcuts import render

def loadMessage(request):

    return render(request, 'utils/message.html')