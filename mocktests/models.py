import datetime
import collections
from django.db import models  
from tinymce.models import HTMLField
from django.contrib.auth.models import AbstractUser, UserManager,User

 

# from questions.models import Question 
from programs.models import ReviewProgram 
# Create your models here.

class MockTest(models.Model):
    title=models.CharField(max_length = 200)
    subtitle = models.TextField(null=True)
    description = models.TextField(null=True)
    overview = HTMLField()
    guidelines = HTMLField()
    reviewprogram = models.ForeignKey(ReviewProgram,on_delete=models.CASCADE) 
    
    active_from = models.DateTimeField()
    active_to = models.DateTimeField()
    postedby = models.ForeignKey(User,related_name='Posted',on_delete=models.CASCADE)
    # approvedby = models.IntegerField(blank=True)

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

    deleted = models.BooleanField(default=False, blank=True)
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    mocktestsections = None
    @property
    def active(self):
        return (timezone.now() >= self.active_from and
            timezone.now() < self.active_to)

    def __str__(self):
        return self.title   
    def setmocktestsections(self): 
        self.mocktestsections = self.mocktestsection_set.all()
        print(self.mocktestsections)
        return  self.mocktestsections
    
class MockTestSectionManager(models.Manager):
     
    def get_attempts_for_user(self, user):
        attempts = self.attempt_set
        attempts_dict = collections.defaultdict(lambda:None)
        for attempt in attempts:
            if( attempt.user == user):
              attempts_dict[attempt.id] = attempt 
        return attempts_dict    

class MockTestSection(models.Model):
    title=models.CharField(max_length = 200)
    subtitle = models.TextField(null=True)
    description = HTMLField()
    
    guidelines = HTMLField()
     
    mocktest = models.ForeignKey(MockTest,on_delete=models.CASCADE)

    test_time_minutes= models.TimeField(blank=False)
    max_no_of_attempts = models.IntegerField(blank=False) 
    passing_mark = models.IntegerField()
    password = models.CharField(max_length=10, blank=True)
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

    deleted = models.BooleanField(default=False, blank=True)
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    no_of_attempts= 0 
    total_no_of_items= 0 
    attempts=None 
    objects = MockTestSectionManager()
    
    def __str__(self):
        return self.title  
 
    def get_attempts(self,user): 
        mocktestsection = self
        attemptcount = mocktestsection.attempt_set.filter(user=user)
        self.no_of_attempts = attemptcount.count()
        return  attemptcount  
    def get_total_no_of_items(self): 
        total_no_of_items = 0
        for mocktestsubsection in self.mocktestsubsection_set.all():
            total_no_of_items += mocktestsubsection.question_set.count()
 
        self.total_no_of_items = total_no_of_items
        return  total_no_of_items  

    def setattempts(self,user): 
        self.attempts =  Attempt.objects.filter(mocktestsection=self.id,user=user).order_by('-attempt_date','-start_time')  
         
        return  self.attempts

   
class MockTestSubSection(models.Model):
    title=models.CharField(max_length = 200)
    subtitle = models.TextField(null=True)
    description = models.TextField(null=True)
    guidelines = models.TextField(null=True,blank=True) 
   
    
    mocktestsection = models.ForeignKey(MockTestSection,on_delete=models.CASCADE) 

    # questions = models.ManyToManyField( Question, blank=True,
    #     through='MockTestSubSectionQuestion')

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

    deleted = models.BooleanField(default=False, blank=True)
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)   
    def __str__(self):
        return self.title   
    def mocktesttestsentences (self):
        return self.mocktestsentence_set.order_by('sentence_no')  
    def questions(self):
        return self.question_set.order_by('question_no')
    
# class MockTestSubSectionQuestion(models.Model):

#     question = models.ForeignKey(Question,on_delete=CASCADE)
#     mocktestsubsection = models.ForeignKey(MockTestSubSection,on_delete=CASCADE)

#     def __str__(self):
#         return '{} for {}'.format(self.question, self.exam)
    



class Attempt(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    mocktestsection = models.ForeignKey('MockTestSection',on_delete=models.CASCADE)

    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    totalscore = models.IntegerField(null=True,default=0)
     
    totalitems = models.IntegerField()

    CANCELLED = 0
    ONGOING = 1  
    FINISHED = 2 

    STATUS_CHOICES = (
        (CANCELLED, 'CANCELLED'),
        (ONGOING, 'ONGOING'),
        (FINISHED, 'FINISHED'), 
    )

    status = models.IntegerField(
        choices=STATUS_CHOICES,
        default=ONGOING,
    ) 
   
    attempt_date = models.DateField(auto_now_add=True) 
    
    result = models.IntegerField()

    scores=None

    def __str__(self):
        return '{} for {}'.format(self.user, self.mocktestsection)
    def wrong(self):
        return  (self.totalitems -  self.totalscore)
    def totaltime(self):
        if(self.start_time and self.end_time):
            start_delta = datetime.timedelta(hours=self.start_time.hour,minutes=self.start_time.minute,seconds=self.start_time.second)
            end_delta = datetime.timedelta(hours=self.end_time.hour,minutes=self.end_time.minute,seconds=self.end_time.second)
            difference_delta = end_delta - start_delta 
            print(difference_delta)
            return  (difference_delta)
        else:
            return ("N/A")
    def updateresult(self):  
        if self.totalscore < self.mocktestsection.passing_mark:
            self.result = 0
        else:
            self.result = 1 
        
        self.save()
        return self        
    def getresult(self): 
        if self.result == 1:
            return "PASSED"
        elif self.result == 0:
            return "FAILED"  
        else:
            return "N/A"    

    def getstatus(self): 
        CANCELLED = 0
        ONGOING = 1  
        FINISHED = 2 

        STATUS_CHOICES = (
            (CANCELLED, 'CANCELLED'),
            (ONGOING, 'ONGOING'),
            (FINISHED, 'FINISHED'), 
        )

        return STATUS_CHOICES[self.status][1]
    def setscores(self): 

        self.scores =  Score.objects.filter(attempt=self.id)  
         
        return  self.scores
    
   
        


class Score(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    attempt = models.ForeignKey('Attempt',on_delete=models.CASCADE)
    mocktestsubsection = models.ForeignKey('MockTestSubSection',on_delete=models.CASCADE)
 
    score = models.IntegerField()
    totalitems = models.IntegerField()
 

    def __str__(self):
        return '{} for {}'.format(self.score, self.mocktestsubsection)
    def wrong(self):
        return  (self.totalitems -  self.score)
    