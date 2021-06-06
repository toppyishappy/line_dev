from django.shortcuts import render
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils.decorators import method_decorator

from line.line_class import Line

@method_decorator(csrf_exempt, name='dispatch')
class Callback(View):

    def post(self, request):
        body = request.body.decode()
        instance = Line(body=body)
        instance.receive_message()
        return JsonResponse({})
