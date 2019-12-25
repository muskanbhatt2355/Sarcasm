from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from game.models import Level,BonusQuestion
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.
# class userdata(models.Model):
# 	username=models.CharField(max_length=200)
# 	email=models.CharField(max_length=200)
# 	roll=models.CharField(max_length=9)
# 	referral=models.CharField(max_length=100,default=0)
# 	referral_count=models.IntegerField(default=0)

class Player(models.Model):
	user = models.OneToOneField(User, on_delete = models.CASCADE)
	username=models.CharField(max_length=200)
	email=models.CharField(max_length=200)
	roll=models.CharField(default='0', max_length=9)
	referral=models.CharField(max_length=100,default=0)
	referral_count = models.IntegerField(default=0)
	bonus_attempted = models.IntegerField(default=0)
	
	current_level = models.ForeignKey(Level, default=Level.DEFAULT_LEVEL, on_delete=models.CASCADE)
	current_level_time = models.DateTimeField(default=timezone.now)
	bonus_level_id = models.IntegerField(default=1)

	points=models.IntegerField(default=0)
	
	
	
	def __str__(self):
		return self.user.username
	
	def get_level(self):
		return self.current_level.level_id

	def get_name(self):
		return self.user.first_name + " " + self.user.last_name

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
	if created:
		Player.objects.create(user=instance)
	instance.player.save()
