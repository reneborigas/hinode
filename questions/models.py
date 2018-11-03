import os
import locale
from tinymce.models import HTMLField
from django.db import models
from django.conf import settings
from mocktests.models import MockTestSubSection
from django.core.files.storage import default_storage as storage
from django.core.files.base import ContentFile
from django.contrib.auth.models import AbstractUser, UserManager,User
from io import BytesIO
from PIL import Image

from mocktests.models import Attempt
from projecthinode.settings import THUMB_SIZE
 
from audiofield.fields import AudioField
import os.path

def upload_location(instance,filename):
    return "%s/%s" %("questions/images",filename) 
 
def upload_location_sentence(instance,filename):
    return "%s/%s" %("questions/images",filename) 

def upload_location_choices(instance,filename):
    return "%s/%s" %("choices/images",filename) 
def upload_location_audio(instance,filename):
    return "%s/%s" %("questions/audios",filename) 
class Question(models.Model):
    
    question_no=models.IntegerField(blank=False)
    question_text = HTMLField()
    hint = HTMLField() 
    image = models.FileField(upload_to=upload_location, null=True,blank=True)
    thumbnail = models.FileField(upload_to='thumbs', editable=False)
    audio_file = AudioField(upload_to=upload_location_audio, blank=True,
                        ext_whitelist=(".mp3", ".wav", ".ogg"),
                        help_text=("Allowed type - .mp3, .wav, .ogg"))

    # choices = models.ManyToManyField('Choice')



    mocktestsubsection = models.ForeignKey(MockTestSubSection,on_delete=models.CASCADE)
    mocktestsentence = models.ForeignKey('MockTestSentence',on_delete=models.CASCADE,blank=True,null=True) 

    # correct_answer=models.CharField(max_length = 1)

    # deleted = models.BooleanField(default=False, blank=True)
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)   
    def __str__(self):
        return "%s. %s" % (self.question_no,self.question_text)
    def save(self, *args, **kwargs):
        """
        Make and save the thumbnail for the photo here.
        """
        super(Question, self).save(*args, **kwargs)
        
        if self.image:    
            if not self.make_thumbnail():
                raise Exception('Could not create thumbnail - is the file type valid?')
                
    def make_thumbnail(self):
        """
        Create and save the thumbnail for the photo (simple resize with PIL).
        """ 
        
        image = Image.open(self.image)
        image.thumbnail(THUMB_SIZE, Image.ANTIALIAS)

        thumb_name, thumb_extension = os.path.splitext(self.image.name)
        thumb_extension = thumb_extension.lower()

        thumb_filename = thumb_name + '_thumb' + thumb_extension

        if thumb_extension in ['.jpg', '.jpeg']:
            FTYPE = 'JPEG'
        elif thumb_extension == '.gif':
            FTYPE = 'GIF'
        elif thumb_extension == '.png':
            FTYPE = 'PNG'
        else:
            return False    # Unrecognized file type

        # Save thumbnail to in-memory file as StringIO
        temp_thumb = BytesIO()
        image.save(temp_thumb, FTYPE)
        temp_thumb.seek(0)

        # set save=False, otherwise it will run in an infinite loop
        self.thumbnail.save(thumb_filename, ContentFile(temp_thumb.read()), save=False)
        temp_thumb.close()

        return True

    def audio_file_player(self):
        """audio player tag for admin"""
        if self.audio_file: 
            file_url = settings.MEDIA_URL + str(self.audio_file) 
            player_string = '<audio src="%s" controls>Your browser does not support the audio element.</audio>' % (file_url)
            return player_string

    audio_file_player.allow_tags = True
    audio_file_player.short_description = ('Audio file player')    

class Choice(models.Model):

    # choice_no= models.CharField(max_length = 1)

    choice_text = HTMLField()
    correct = models.BooleanField(default=False)
    image = models.FileField(upload_to=upload_location_choices, null=True,blank=True)
    thumbnail = models.FileField(upload_to='thumbs', editable=False)
    # question = models.ForeignKey(Question)

    # choice_item = models.TextField(null=True,blank=True)
    # choice_picture = models.TextField(null=True,blank=True)
    # choice_audio = models.TextField(null=True,blank=True) 
    

    
  
    # mocktestitem = models.ForeignKey(MockTestItem,on_delete=models.CASCADE)

    question = models.ForeignKey(Question,on_delete=models.CASCADE)

    deleted = models.BooleanField(default=False, blank=True)
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)   
    def __str__(self):
        return "%s" % (self.choice_text)
    def save(self, *args, **kwargs):
        """
        Make and save the thumbnail for the photo here.
        """
        super(Choice, self).save(*args, **kwargs)
        
        if self.image:    
            if not self.make_thumbnail():
                raise Exception('Could not create thumbnail - is the file type valid?')
    def make_thumbnail(self):
        """
        Create and save the thumbnail for the photo (simple resize with PIL).
        """ 
        
        image = Image.open(self.image)
        image.thumbnail(THUMB_SIZE, Image.ANTIALIAS)

        thumb_name, thumb_extension = os.path.splitext(self.image.name)
        thumb_extension = thumb_extension.lower()

        thumb_filename = thumb_name + '_thumb' + thumb_extension

        if thumb_extension in ['.jpg', '.jpeg']:
            FTYPE = 'JPEG'
        elif thumb_extension == '.gif':
            FTYPE = 'GIF'
        elif thumb_extension == '.png':
            FTYPE = 'PNG'
        else:
            return False    # Unrecognized file type

        # Save thumbnail to in-memory file as StringIO
        temp_thumb = BytesIO()
        image.save(temp_thumb, FTYPE)
        temp_thumb.seek(0)

        # set save=False, otherwise it will run in an infinite loop
        self.thumbnail.save(thumb_filename, ContentFile(temp_thumb.read()), save=False)
        temp_thumb.close()

        return True
 

class MockTestSentence(models.Model):
    sentence_no=models.IntegerField(blank=False)
    sentence_text=models.TextField(null=True,blank=True)
    image = models.FileField(upload_to=upload_location_sentence, null=True,blank=True)
    thumbnail = models.FileField(upload_to='thumbs', editable=False)
    audio = models.TextField(null=True,blank=True)
    
    # question = models.ForeignKey(Question,on_delete=models.CASCADE, limit_choices_to={'MockTestSubSection':Question.mocktestsubsection},related_name='instructor')
    
   
    mocktestsubsection = models.ForeignKey(MockTestSubSection,on_delete=models.CASCADE,blank=True)
    # question = models.ForeignKey(Question,on_delete=models.CASCADE) 

    deleted = models.BooleanField(default=False, blank=True)
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)   
    def __int__(self):
        return   self.sentence_no    
        
    def save(self, *args, **kwargs):
        """
        Make and save the thumbnail for the photo here.
        """
        super(MockTestSentence, self).save(*args, **kwargs)
       
        if self.image:    
            if not self.make_thumbnail():
                raise Exception('Could not create thumbnail - is the file type valid?')

    def make_thumbnail(self):
        """
        Create and save the thumbnail for the photo (simple resize with PIL).
        """ 
        
        image = Image.open(self.image)
        image.thumbnail(THUMB_SIZE, Image.ANTIALIAS)

        thumb_name, thumb_extension = os.path.splitext(self.image.name)
        thumb_extension = thumb_extension.lower()

        thumb_filename = thumb_name + '_thumb' + thumb_extension

        if thumb_extension in ['.jpg', '.jpeg']:
            FTYPE = 'JPEG'
        elif thumb_extension == '.gif':
            FTYPE = 'GIF'
        elif thumb_extension == '.png':
            FTYPE = 'PNG'
        else:
            return False    # Unrecognized file type

        # Save thumbnail to in-memory file as StringIO
        temp_thumb = BytesIO()
        image.save(temp_thumb, FTYPE)
        temp_thumb.seek(0)

        # set save=False, otherwise it will run in an infinite loop
        self.thumbnail.save(thumb_filename, ContentFile(temp_thumb.read()), save=False)
        temp_thumb.close()

        return True
    def __str__(self):
        return "Sentence No. %s: %s" % (self.sentence_no,self.sentence_text)
    def questions(self):
        return self.question_set.order_by('question_no')

class StudentAnswer(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    question = models.ForeignKey(Question,on_delete=models.CASCADE)
    choice =  models.ForeignKey(Choice,on_delete=models.CASCADE,null=True,blank=True)
    attempt = models.ForeignKey(Attempt,on_delete=models.CASCADE)

    def __str__(self):
        return '{} for {} for {}'.format(self.user,
            self.question.question_text, self.question.mocktestsubsection.mocktestsection.mocktest.title)
    