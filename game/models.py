from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.

#Write a model for level here
class Level(models.Model):
	""" A model representing a single level """
	DEFAULT_LEVEL = 1
	
	level_id = models.IntegerField(primary_key=True) 
	title = models.CharField(max_length=100)
	question = RichTextField(config_name = 'awesome_ckeditor', blank = True)
	answer = models.CharField(max_length=120)
	is_bonus=models.BooleanField(default=False)

	# hint = models.CharField(max_length=255, null=True, blank=True)
	image = models.ImageField(upload_to = 'static', null = True,	blank = True)
	audiofile= models.FileField(upload_to='static/', null=True, blank = True, verbose_name="")
	videofile= models.FileField(upload_to='static/', null=True, blank = True, verbose_name="")

	def __str__(self):
		return self.title
