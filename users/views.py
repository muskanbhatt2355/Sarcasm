from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
from .models import Player
from django.contrib.auth.models import User


def register(request):
		current_user = request.user
		current_user_data = Player.objects.get(user = current_user.id)				#Change
		# try:
		# 	current_user_data = Player.objects.get(id = current_user.id)
		# except Player.DoesNotExist:
		# 	current_user_data = None
		if request.method == 'POST':
			form = UserRegisterForm(request.POST, instance = current_user_data)
			if form.is_valid():
				user = form.save()
				# print(user)										
				user.refresh_from_db()
				# print(user)										
				username = form.cleaned_data.get('username')
				referral = form.cleaned_data.get('referral')
				# print(referral)										
				if Player.objects.filter(roll=referral).exists():
					# print("Referral Exists")
					t = Player.objects.get(roll=referral)
					if t.referral_count < 3:
						t.referral_count = t.referral_count + 1
						t.points+=3
					t.save()
				else:
					# print("Referral Doesn't Exist")		
				messages.success(request, 'Account created for {0}!'.format(username))
				return redirect('login')
			else:
				form = UserRegisterForm()
			return render(request, 'users/register.html', {'form': form})
		form = UserRegisterForm()
		return render(request, 'users/register.html', {'form': form})


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

