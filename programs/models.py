import os
import locale 
from django.db import models
# from django.contrib.auth.models import Group, User
from django.contrib.auth.models import AbstractUser, UserManager,User
# from questions.models import Question 
from django.conf import settings

from tinymce.models import HTMLField

# Create your models here.
from django.core.files.storage import default_storage as storage
from django.core.files.base import ContentFile
from io import BytesIO
from PIL import Image


from projecthinode.settings import THUMB_SIZE


# class program(models.Model):
#     name=models.CharField(max_length=120)
#     description = models.TextField(null=True)
#     location=models.CharField(max_length=120,default='0.0')

#     def _unicode_(self):
#         return self.name 


def upload_location(instance,filename):
    return "%s/%s" %("reviewprograms/images",filename) 
    
class ReviewProgram(models.Model):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title=models.CharField(max_length = 200,blank=False)
    overview = HTMLField()
    description = HTMLField()
    instructor = models.ForeignKey(User,on_delete=models.CASCADE, limit_choices_to={'is_teacher':True},related_name='instructor')
    
    # lesson = models.ManyToManyField(Lesson,related_name=_('Lessons'))
    # members = models.ManyToManyField(User, related_name = _('Members'))
   
 
    image = models.FileField(upload_to=upload_location, null=True,blank=True)
    thumbnail = models.FileField(upload_to='thumbs', editable=False)

    enrolled = models.ManyToManyField(User, blank=True,
        through='Enrollment')


    ACTIVE = 1
    INACTIVE = 0
    
    STATUS_CHOICES = (
        (ACTIVE, 'ACTIVE'),
        (INACTIVE, 'INACTIVE'),
        
    )
   
    status = models.IntegerField(
        choices=STATUS_CHOICES,
        default=ACTIVE,
    ) 

    # deleted = models.BooleanField(default=False, blank=True)
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    # def _unicode_(self):
    #     return self.name   
    def save(self, *args, **kwargs):
        """
        Make and save the thumbnail for the photo here.
        """
        super(ReviewProgram, self).save(*args, **kwargs)
        if self.image:    
            if not self.make_thumbnail():
                raise Exception('Could not create thumbnail - is the file type valid?')

    def __str__(self):
        return self.title   

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
 

class Enrollment(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    reviewprogram = models.ForeignKey(ReviewProgram,on_delete=models.CASCADE)
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    
    ACTIVE = 1
    INACTIVE = 0
    
   
    STATUS_CHOICES = (
        (ACTIVE, 'ACTIVE'),
        (INACTIVE, 'INACTIVE'), 
    )
    status = models.IntegerField(
        choices=STATUS_CHOICES,
        default=ACTIVE,
    ) 
     
    def getstatus(self): 
        ACTIVE = 1
        INACTIVE = 0
        
    
        STATUS_CHOICES = (
            (ACTIVE, 'ACTIVE'),
            (INACTIVE, 'INACTIVE'), 
        )

        return STATUS_CHOICES[self.status][1]
        
        

    def __str__(self):
        return '{} for {}'.format(self.user, self.reviewprogram)

