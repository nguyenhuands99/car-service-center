from django.views import View
from django.http.response import HttpResponse
from django.shortcuts import render


class WelcomeView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('<h2>Welcome to the Hypercar Service!</h2>')


class MenuView(View):
    template = 'menu/index.html'
    menu_services = {'Change oil': 'change_oil',
                     'Inflate tires': 'inflate_tires',
                     'Get diagnostic test': 'diagnostic'}

    def get(self, request, *args, **kwargs):
        return render(request, self.template, {'services': self.menu_services})


class TicketView(View):
    template = 'get_ticket/index.html'
    line_of_cars = {
        'change_oil': 0,
        'inflate_tires': 0,
        'diagnostic': 0
    }
    TIME_FOR_SERVICES = {
        'change_oil': 2,
        'inflate_tires': 5,
        'diagnostic': 30
    }

    def get(self, request, service, *args, **kwargs):
        if service == 'change_oil':
            waiting_time = self.line_of_cars['change_oil'] * self.TIME_FOR_SERVICES['change_oil']
        elif service == 'inflate_tires':
            waiting_time = self.line_of_cars['change_oil'] * self.TIME_FOR_SERVICES['change_oil'] + \
                           self.line_of_cars['inflate_tires'] * self.TIME_FOR_SERVICES['inflate_tires']
        else:
            waiting_time = self.line_of_cars['change_oil'] * self.TIME_FOR_SERVICES['change_oil'] + \
                           self.line_of_cars['inflate_tires'] * self.TIME_FOR_SERVICES['inflate_tires'] + \
                           self.line_of_cars['diagnostic'] * self.TIME_FOR_SERVICES['diagnostic']

        # increment the car in service line by 1
        self.line_of_cars[service] += 1
        ticket_numer = sum(self.line_of_cars.values())
        return render(request, self.template, {'number': ticket_numer, 'time': waiting_time})
