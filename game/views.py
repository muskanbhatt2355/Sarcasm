from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib.auth.models import User
from .models import Level
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

def bonus(request):
	return render(request, 'game/bonus.html',{})


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
			'que': question,
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
			if cur_level.is_bonus:
				if ans=="skip":
					cur_user.player.current_level=Level.objects.get(level_id = level_number + 1)
					cur_user.player.save()
				if ans == cur_level.answer:
					level_number = cur_user.player.current_level.level_id
					try:
						cur_user.player.current_level = Level.objects.get(level_id = level_number + 1)
						cur_user.player.bonus_attempted=cur_user.player.bonus_attempted+1
						cur_user.player.points=cur_user.player.points+4
						cur_user.player.current_level_time = timezone.now()	 					
						cur_user.player.save()
					except:
						pass
			else:
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

	# if form.is_valid():
	# 		ans = form.cleaned_data.get('answer')
	# 		if cur_level.is_bonus:
	# 			if ans=="skip":
	# 				cur_user.player.current_level=Level.objects.get(level_id = level_number + 1)
	# 				cur_user.player.save()
	# 			elif ans==cur_level.answer:
	# 				try:
	# 					cur_user.player.current_level = Level.objects.get(level_id = level_number + 1)
	# 					cur_user.player.current_level_time = timezone.now()
	# 					cur_user.player.points=cur_user.player.points+2
	# 					cur_user.player.bonus_attempted=cur_user.player.bonus_attempted+1
	# 					cur_user.player.save()
	# 				except:
	# 					pass

			
	# 		else:
	# 			if ans == cur_level.answer:
	# 				try:
	# 					cur_user.player.current_level = Level.objects.get(level_id = level_number + 1)
	# 					cur_user.player.current_level_time = timezone.now()
	# 					cur_user.player.points=cur_user.player.points+3
	# 					cur_user.player.save()
	# 				except:
	# 					pass
