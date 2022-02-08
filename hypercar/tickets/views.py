from django.views import View
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from collections import deque


class WelcomeView(View):
    template = 'welcome.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template)


class MenuView(View):
    template = 'menu/index.html'
    menu_services = {'Change oil': 'change_oil',
                     'Inflate tires': 'inflate_tires',
                     'Get diagnostic test': 'diagnostic'}

    def get(self, request, *args, **kwargs):
        return render(request, self.template,
                      {'services': self.menu_services})


services = {
    'change_oil': deque(),
    'inflate_tires': deque(),
    'diagnostic': deque(),
}

tickets = {
    'num': 0, 'waiting_time': 0, 'next': 0
}


class TicketView(View):
    template = 'get_ticket/index.html'

    TIME_FOR_SERVICES = {
        'change_oil': 2,
        'inflate_tires': 5,
        'diagnostic': 30
    }

    def get(self, request, service, *args, **kwargs):
        tickets['num'] += 1
        if service == 'change_oil':
            tickets['waiting_time'] = len(services['change_oil']) * self.TIME_FOR_SERVICES['change_oil']
        elif service == 'inflate_tires':
            tickets['waiting_time'] = len(services['change_oil']) * self.TIME_FOR_SERVICES['change_oil'] + \
                                      len(services['inflate_tires']) * self.TIME_FOR_SERVICES['inflate_tires']
        else:
            tickets['waiting_time'] = len(services['change_oil']) * self.TIME_FOR_SERVICES['change_oil'] + \
                                      len(services['inflate_tires']) * self.TIME_FOR_SERVICES['inflate_tires'] + \
                                      len(services['diagnostic']) * self.TIME_FOR_SERVICES['diagnostic']

        services[service].append(tickets['num'])

        return render(request, self.template, {'number': tickets['num'], 'time': tickets['waiting_time']})


class ProcessingView(View):
    template = 'processing/processing_menu.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template, {'oil_queue': len(services['change_oil']),
                                               'tires_queue': len(services['inflate_tires']),
                                               'diagnostic_queue': len(services['diagnostic'])})

    def post(self, request, *args, **kwargs):
        if services['change_oil']:
            tickets['next'] = services['change_oil'].popleft()
            tickets['waiting_time'] -= 2
        elif services['inflate_tires']:
            tickets['next'] = services['inflate_tires'].popleft()
            tickets['waiting_time'] -= 5
        elif services['diagnostic']:
            tickets['next'] = services['diagnostic'].popleft()
            tickets['waiting_time'] -= 30
        else:
            tickets['next'] = 0

        return redirect('/next')


class NextProcessView(View):
    template = 'processing/processed.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template, {'next_number': tickets['next']})
