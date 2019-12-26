from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib.auth.models import User
from .models import Level, BonusQuestion
from .forms import LevelForm
from django.shortcuts import redirect
from django.utils import timezone
from django.urls import reverse
# from django.contrib.sites.models import Site	# To get location of current domain
# Create your views here.
def home(request):
	return render(request, 'game/home.html',{})

def prize(request):
	return render(request, 'game/prizes.html',{})

def forum(request):
	return render(request, 'game/forum.html',{})

def instructions(request):
	return render(request, 'game/instructions.html',{})


def contacts(request):
	return render(request, 'game/contacts.html',{})

class Play(LoginRequiredMixin,View) :
	login_url = '/login/'
	redirect_field_name = '/register/'
	redierct_url = 'http://localhost:8080/accounts/facebook/login/callback/'
	# Form field for the level
	form_class = LevelForm


	def get(self, request, *args, **kwargs):
		""" 
		GET Request 
		1. get the current user by the request.user
		2. find their current level and return the question accordingly
		"""
		cur_user = User.objects.get(id=request.user.id)
		# if cur_user.profile.is_banned:
	    # return render(request,'home.html')
		cur_level = cur_user.player.current_level
		form = self.form_class()
		context = {
			'level' : cur_level,
			'form': form,
		}
		return render(request,'game/play.html',context)   #{{form|crispy}} crispy form was removed try to add it back


	def post(self,request, *args, **kwargs):
		"""
		POST request
		1. Get the current user and their answer
		2. If the answer is correct, update the level
		"""
		cur_user = User.objects.get(id=request.user.id)
		cur_level = cur_user.player.current_level
		level_number = cur_user.player.current_level.level_id

		form = self.form_class(request.POST)    #What if request != 'POST' ????
		if form.is_valid():
			ans = form.cleaned_data.get('answer')
			if ans == cur_level.answer:
				level_number = cur_user.player.current_level.level_id
				try:
					cur_user.player.current_level = Level.objects.get(level_id = level_number + 1)
					cur_user.player.points=cur_user.player.points+3
					cur_user.player.current_level_time = timezone.now()	 					
					cur_user.player.save()
				except:
					pass

		return redirect(reverse('play'))


class Bonus(View) :
	login_url = '/login/'
	redirect_field_name = '/register/'
	redierct_url = 'http://localhost:8080/accounts/facebook/login/callback/'
	# Form field for the level
	form_class = LevelForm

	def get(self, request, *args, **kwargs):
		cur_user = User.objects.get(id=request.user.id)
		try:
			bonus_level = BonusQuestion.objects.get(level_id=cur_user.player.bonus_level_id)
			livedatetime=bonus_level.live_date
			current_time=timezone.now()
			expdatetime = bonus_level.expiration_date
			expired = bonus_level.expiration_date < current_time
			if expired:
				bonus_array = BonusQuestion.objects.filter(level_id__gt=cur_user.player.bonus_level_id)
				for q in bonus_array:
					if q.live_date < current_time and current_time<q.expiration_date:
						cur_user.player.bonus_level_id = q.level_id
						bonus_level = BonusQuestion.objects.get(level_id=cur_user.player.bonus_level_id)
						cur_user.player.save()

			if livedatetime>current_time:
				print("Question {0} not live".format(bonus_level.level_id))
				raise
		except:
			print("Error")
			return redirect(reverse('play'))
		form = self.form_class

		question = bonus_level.question
		livedatetime = bonus_level.live_date
		expdatetime = bonus_level.expiration_date
	
		current_time = timezone.now()
		year = expdatetime.strftime('%Y')
		month = expdatetime.strftime('%m')
		day = expdatetime.strftime('%d')
		hour = expdatetime.strftime('%H')
		minute = expdatetime.strftime('%M')
		second = expdatetime.strftime('%S')

		context = {'question': question,'year': year,'month': month,'day': day,'hour': hour,'minute': minute,
			'second':second,'expdate': expdatetime,'livedate': livedatetime,'now': current_time,'form':form,}
		return render(request, 'game/bonus.html', context)
	

	def post(self,request, *args, **kwargs):
		"""
		POST request
		1. Get the current user and their answer
		2. If the answer is correct, update the level
		"""
		cur_user = User.objects.get(id=request.user.id)
		bonus_level = BonusQuestion.objects.get(level_id=cur_user.player.bonus_level_id)
		form = self.form_class(request.POST)    #What if request != 'POST' ????
		if form.is_valid():
			ans = form.cleaned_data.get('answer')
			if ans == bonus_level.answer:
				
				level_number = bonus_level.level_id
				if cur_user.player.bonus_level_id == level_number:
					try:
						cur_user.player.bonus_level_id += 1
						cur_user.player.bonus_attempted=cur_user.player.bonus_attempted+1
						cur_user.player.points += 10	 					
						cur_user.player.save()
						return redirect(reverse('play'))
					except:
						pass
				else:
					print("Cant play Bonus Twice")
					return redirect(reverse('play'))
			else:
				print("Wrong Answer! Try Again")
				return redirect(reverse('bonus'))
		return redirect(reverse('play'))
