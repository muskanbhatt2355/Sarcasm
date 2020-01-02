from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
from .models import Player
from django.contrib.auth.models import User
import time

def ajax(request):
	if request.is_ajax():
		username = request.POST("username")
	
		try:
			Player.objects.filter(username=username):
			response_dict = {
				success: False,
			}
		except:
			response_dict = {
				success: True,
			}
	return render(request,'users/register.html',response_dict)


def register(request):
	current_user = request.user
	current_user_data = Player.objects.get(user=current_user.id)
	current_user_data.is_registered = False
	

	if (not current_user_data.is_registered):
		if request.method == 'POST':
			form = UserRegisterForm(request.POST, instance = current_user_data)
			if form.is_valid():
				user = form.save()
				user.refresh_from_db()									
				username = form.cleaned_data.get('username')
				referral = form.cleaned_data.get('referral')									
				if Player.objects.filter(roll=referral).exists():
					t = Player.objects.get(roll=referral)
					if t.referral_count < 3:
						t.referral_count = t.referral_count + 1
						t.points+=3
					t.save()
				else:
					pass
				current_user_data.is_registered = True
				current_user_data.save()
				messages.success(request, 'Account created for {0}!'.format(username))
				time.sleep(2)
				return redirect('login')
			else:
				form = UserRegisterForm()
			return render(request, 'users/register.html', {'form': form})
		form = UserRegisterForm()
		return render(request, 'users/register.html', {'form': form})
	else:
		return redirect(reverse('play'))

def leaderboard(request):
    """
    Returns the leadboard, sorted first with level (desc) then time (asc)
    """
    queryset = User.objects.order_by(
        '-player__points', 'player__current_level_time')
    context = {
        'queryset': queryset,
    }
    return render(request, 'users/leaderboard.html', context)

