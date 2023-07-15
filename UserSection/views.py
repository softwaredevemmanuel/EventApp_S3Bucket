from django.shortcuts import render, redirect, get_object_or_404
from AdminSection.models import Event, Customer
from django.views.generic import ListView, DetailView
from django.utils import timezone
from django.http import HttpResponse
from django.db import models
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.http.request import HttpRequest
from django.db.models import Sum
from django.core.paginator import Paginator





# Create your views here.

class EventView(ListView):
    model = Event
    template_name = "allEvents.html"
    paginate_by = 8


class BookView(ListView):
    model = Customer
    template_name = "BookingDetails.html"

class BookView(ListView):
    model = Customer
    template_name = "EventDetails2.html"

class EventDetailsView(DetailView):
    model = Event
    template_name = "Edetails.html"
    queryset = Event.objects.all()

class Booking(ListView):
    queryset = Customer.objects.all()
    template_name = "BookingDetails.html"


class EventSearchView(ListView):
    model = Event
    template_name = "searchEvents.html"
    paginate_by = 2

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('query')
        if query:
            queryset = queryset.filter(event_name__icontains=query)  # Filter based on the event_name field
        return queryset



class FreeEventView(ListView):
    model = Event
    template_name = "freeEvents.html"
    paginate_by = 8  # Number of events to display per page

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(price__isnull=True)  # Filter events where price is NULL
        return queryset


class PaidEventView(ListView):
    model = Event
    template_name = "paidEvents.html"
    paginate_by = 8  # Number of events to display per page

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.exclude(price=None).exclude(price=0)  # Filter events with a price
        return queryset

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     event_list = context['event_list']
    #     paginator = Paginator(event_list, self.paginate_by)
    #     page = self.request.GET.get('page')
    #     events = paginator.get_page(page)
    #     context['events'] = events
    #     return context


class DateAccendView(ListView):
    model = Event
    template_name = "eventAccending.html"
    ordering = 'event_date'
    paginate_by = 8

class DateDecendView(ListView):
    model = Event
    template_name = "eventDescending.html"
    ordering = '-event_date'
    paginate_by = 8


def about(request):
    return render(request, "about.html")

    

def register_free(request,pk):
    poll=Event.objects.get(pk=pk)
    if request.method == 'POST':
        sel_opt=request.POST['poll']
       

        if sel_opt == 'option1' :
            email = request.POST["email"]
            phone = request.POST["phone"]
            event_id=poll.id
            event_name = poll.event_name
            # event_date = poll.event_date

            b = Customer(
                email=email,
                phone=phone,
                event_id = event_id,
                verified = False,
                event_name = event_name,
                # event_date = event_date
            )

            if Customer.objects.filter(email=email, event_id=event_id, verified=True).exists():  
                messages.error(request, "You have already registered for this event")


            elif Customer.objects.filter(email=email, event_id=event_id, verified=False).exists():  
                messages.error(request, "Your previous payment wasnt successfull for this event")
                b.save()
                poll.save()
                return render(request, 'make_payment.html', {'customer':b, 'event': poll, 'paystack_public_key':settings.PAYSTACK_PUBLIC_KEY})

            else:
                poll.bookings += 1

                b.save()
                poll.save()
                return render(request, 'freeCheckout.html', {'customer':b, 'event': poll, 'paystack_public_key':settings.PAYSTACK_PUBLIC_KEY})

        
        else :
            return HttpResponse(400,'Invalid vote form')
        poll.save()  
        return redirect('user_events_page')        
       
    context={
        'poll':poll,
    }

    return render(request,'all-events.html', context)




def register(request,pk):
    poll=Event.objects.get(pk=pk)
    if request.method == 'POST':
        sel_opt=request.POST['poll']
       

        if sel_opt == 'option1' :
            email = request.POST["email"]
            phone = request.POST["phone"]
            event_id=poll.id
            price = poll.price
            event_name = poll.event_name
            event_date = poll.event_date

            b = Customer(
                email=email,
                phone=phone,
                event_id = event_id,
                amount = price,
                verified = False,
                event_name = event_name,
                event_date = event_date
            )

            if Customer.objects.filter(email=email, event_id=event_id, verified=True).exists():  
                messages.error(request, "You have already registered for this event")
            

            elif Customer.objects.filter(email=email, event_id=event_id, verified=False).exists():  
                messages.error(request, "Your previous payment wasnt successfull for this event")
                b.save()
                poll.save()
                return render(request, 'paidCheckout.html', {'customer':b, 'event': poll, 'paystack_public_key':settings.PAYSTACK_PUBLIC_KEY})

            else:
                #send_mail(subject, message, message_from,[email])
                poll.bookings += 1
                poll.slot_left = poll.space_capacity - poll.bookings
                b.save()
                poll.save()
                # print(Customer.objects.filter().get(pk=pk))
                hello=(Customer.objects.filter(email=email))
                return render(request, 'paidCheckout.html', {'customer':b, 'event': poll, 'paystack_public_key':settings.PAYSTACK_PUBLIC_KEY})

        
        else :
            return HttpResponse(400,'Invalid vote form')
        poll.save()  
        return redirect('user_events_page')        
       
    context={
        'poll':poll,
    }

    return render(request,'all-events.html', context)


def verify_payment(request:HttpRequest, ref:str) -> HttpResponse:
    payment = get_object_or_404(Customer, ref=ref)
    verified = payment.verify_payment()
    subject = "Event registration"
    message = "You have registered for event " + str(payment.event_name) + " which will be holding on the " + str(payment.event_date) + " \n Kindly show this message on getting to the venue. Thank You."
    message_from = "Event XYZ"
    
    if not verified:
        send_mail(subject, message, message_from,[payment.email])
        messages.success(request, "Payment Received successfully \n Check your email for futher informations")
    else:
        messages.error(request, "Verification Failled")
    return redirect('user_events_page')


def verify_free_payment(request:HttpRequest, ref:str) -> HttpResponse:
    payment = get_object_or_404(Customer, ref=ref)
    verified = payment.verify_payment()
    subject = "Event registration"
    message = "You have registered for event " + str(payment.event_name) + " which will be holding on the " + str(payment.event_date) + " \n Kindly show this message on getting to the venue. Thank You."
    message_from = "Event XYZ"
    
    if not verified:
        send_mail(subject, message, message_from,[payment.email])
        messages.success(request, "You have registered successfully \n Check your email for futher information")
    else:
        messages.error(request, "Verification Failled")
    return redirect('user_events_page')



# Create your views here.
def view_analytics(request):
    # Increment the number of visitors
    request.session['num_visitors'] = request.session.get('num_visitors', 0) + 1

    # Render the analytics page
    return render(request, 'view_analytics.html', {
        'num_visitors': request.session.get('num_visitors', 0)
    })



