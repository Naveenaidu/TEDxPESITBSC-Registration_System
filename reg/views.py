from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Max

from .models import Participant
from .forms import LoginForm, CheckInForm, LunchForm, BreakfastForm, RegForm, \
	DinnerForm

def login_user(request):
	context = {}
	if request.method == 'GET':
		if request.user.is_authenticated():
			return redirect('home')

		form = LoginForm()
		context['form'] = form

		return render(request,'login.html',context)

	elif request.method == 'POST':
		form = LoginForm(request.POST)

		if form.is_valid():
			data = form.cleaned_data

			username = data['username']
			password = data['password']

			user = authenticate(username=username, password=password)

			if user is not None:
				if user.is_active:
					login(request, user)

					return redirect('home')

				else:
					context['form']			= LoginForm()
					context['message']		= "Account disabled."
					context['messageclass']	= "error"

					return render(request,'login.html',context)
			else:
				context['form']			= LoginForm()
				context['message']		= "Invalid username or password."
				context['messageclass']	= "error"

				return render(request,'login.html',context)

def logout_user(request):
	logout(request)

	return redirect('home')

def home(request):

	return render(request,'home.html',{})

@login_required(login_url='/login')
def register(request):
	context = {}

	if request.method == "GET":

		form = RegForm(hide_barcode=True)
		context['form']			= form
		context['form_type']	= 1

		return render(request,'register.html',context)

	elif request.method == "POST":

		form = RegForm(request.POST)

		if form.is_valid():
			data = form.cleaned_data

			pid = str(data['pid'])
			barcode	= str(data['barcode'])

			if not barcode:
				try:
					if len(pid) == 4:
						p = Participant.objects.get(participant_id=pid.upper())
					elif len(pid) == 10:
						p = Participant.objects.get(phone=pid)
					else:
						context['message'] = "Invalid Participant ID or \
							mobile number."
						context['messageclass'] = "error"
						context['form'] = RegForm(hide_barcode=True)

						return render(request,'register.html',context)

				except ObjectDoesNotExist:
					context['message']		= "No user found with those details."
					context['messageclass'] = "error"
					context['form']			= RegForm(hide_barcode=True)

					return render(request,'register.html',context)

				participant_details = {}
				participant_details['pid'] = p.id
				participant_details['name'] = p.name
				participant_details['type'] = p.reg_type
				participant_details['phone'] = p.phone
				participant_details['participant_id'] = p.participant_id
				participant_details['registered'] = "Yes" if p.registered else "No"
				participant_details['barcode'] = "None" if not p.barcode else p.barcode
				participant_details['checked_in'] = "Yes" if p.checked_in else "No"
				hide_barcode = False
				initial_dict = dict()
				if pid:
					initial_dict['pid'] = pid
				if p.barcode:
					hide_barcode = True

				form = RegForm(initial=initial_dict,
				 hide_barcode=hide_barcode)

				context['participant_details'] = participant_details
				context['form']	= form
				context['form_type'] = 2

				return render(request,'register.html',context)

			else:
				try:
					if len(pid) == 4:
						p = Participant.objects.get(participant_id=pid.upper())
					elif len(pid) == 10:
						p = Participant.objects.get(phone=pid)
					else:
						context['message'] = "Invalid Participant ID or \
							mobile number."
						context['messageclass'] = "error"
						context['form'] = RegForm(hide_barcode=True)

						return render(request,'register.html',context)

				except ObjectDoesNotExist:
					context['message']		= "No user found with those details."
					context['messageclass'] = "error"
					context['form']			= RegForm(hide_barcode=True)

					return render(request,'register.html',context)



				p.barcode = barcode
				p.registered = True
				p.checked_in = False
				p.save()

				form = RegForm(hide_barcode=True)

				context['form']				= form
				context['message']			= "Registered successfully"
				context['messageclass']		= "success"
				context['form_type']		= 1

				return render(request,'register.html',context)

		else:
			context['form'] = RegForm(hide_barcode=True)
			context['form_type'] = 1

			return render(request,'register.html',context)

@login_required(login_url='/login')
def lunch(request):
	context = {}

	if request.method == "GET":
		form = LunchForm()
		context['form'] = form
		return render(request,'lunch.html',context)
	elif request.method == "POST":
		form = LunchForm(request.POST)

		if form.is_valid():
			form_data = form.cleaned_data

			barcode = form_data['barcode']

			p = Participant.objects.filter(barcode=barcode)

			if p.exists():
				p = p[0]
				context['messageclass'] = 'success'
				if p.had_lunch == True:
					context['messageclass'] = 'error'
					context['message'] = "Lunch request was already \
						processed for {}.".format(p.name)
				else:
					p.had_lunch = True
					p.save()
					context['messageclass'] = 'success'
					context['message'] = "Lunch request successfully \
						processed for {}.".format(p.name)
			else:
				context['messageclass'] = 'error'
				context['message'] = "Couldn't find a user with that barcode."

		context['form'] = LunchForm()

	return render(request,'lunch.html',context)

@login_required(login_url='/login')
def dinner(request):
	context = {}

	if request.method == "GET":
		form = DinnerForm()
		context['form'] = form
		return render(request,'dinner.html',context)

	elif request.method == "POST":
		form = DinnerForm(request.POST)

		if form.is_valid():
			form_data = form.cleaned_data

			barcode = form_data['barcode']

			p = Participant.objects.filter(barcode=barcode)

			if p.exists():
				p = p[0]
				context['messageclass'] = 'success'
				if p.had_dinner == True:
					context['messageclass'] = 'error'
					context['message'] = "Dinner request was already processed for {}.".format(p.name)
				else:
					p.had_dinner = True
					p.save()
					context['messageclass'] = 'success'
					context['message'] = "Dinner request successfully processed for {}.".format(p.name)
			else:
				context['messageclass'] = 'error'
				context['message'] = "Couldn't find a user with that barcode."

		context['form'] = DinnerForm()

	return render(request,'dinner.html',context)

@login_required(login_url='/login')
def breakfast(request):
	context = {}

	if request.method == "GET":
		form = BreakfastForm()
		context['form'] = form
		return render(request,'breakfast.html',context)

	elif request.method == "POST":
		form = BreakfastForm(request.POST)

		if form.is_valid():
			form_data = form.cleaned_data

			barcode = form_data['barcode']

			p = Participant.objects.filter(barcode=barcode)

			if p.exists():
				p = p[0]
				context['messageclass'] = 'success'
				if p.had_breakfast== True:
					context['messageclass'] = 'error'
					context['message'] = "Breakfast request was already \
						processed for {}.".format(p.name)
				else:
					p.had_breakfast = True
					p.save()
					context['messageclass'] = 'success'
					context['message'] = "Breakfast request successfully \
						processed for {}.".format(p.name)
			else:
				context['messageclass'] = 'error'
				context['message'] = "Couldn't find a user with that barcode."

		context['form'] = BreakfastForm()

	return render(request,'breakfast.html',context)

@login_required(login_url='/login')
def check_in(request):
	context = {}

	if request.method == "GET":
		form = CheckInForm()
		context['form'] = form
		return render(request,'checkin.html',context)

	elif request.method == "POST":
		form = CheckInForm(request.POST)

		if form.is_valid():
			form_data = form.cleaned_data

			barcode = form_data['barcode']

			p = Participant.objects.filter(barcode=barcode)
			if p.exists():
				p = p[0]
				context['messageclass'] = 'success'
				if p.checked_in == True:
					p.checked_in = False
					p.save()
					context['message'] = "{} was checked-out successfully.".format(p.name)
				else:
					p.checked_in = True
					p.save()
					context['message'] = "{} was checked-in successfully.".format(p.name)

			else:
				context['messageclass'] = 'error'
				context['message'] = "Couldn't find a user with that barcode."

		context['form'] = CheckInForm()

	return render(request,'checkin.html',context)

@login_required(login_url='/login')
def stats(request):
	context = {}

	context['participants'] = Participant.objects.count()
	context['registered'] = Participant.objects.filter(registered=True).count()
	context['checked_in'] = Participant.objects.filter(checked_in=True).count()
	context['had_lunch'] = Participant.objects.filter(had_lunch=True).count()
	context['had_dinner'] = Participant.objects.filter(had_dinner=True).count()
	context['had_breakfast'] = Participant.objects.filter(had_breakfast=True).count()

	return render(request,'stats.html',context)

def dashboard(request):
	return render(request,'dashboard.html',{})
