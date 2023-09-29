from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
from django.db import models
import uuid

class Test(models.Model):
    tid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=50)
    desc = models.TextField(null=True, blank=True)
    img = models.ImageField(upload_to="static/test/")
    
    def image_tag(self):
        return mark_safe('<img src="{}" height=50 />'.format(self.image.url))
    
    def __str__(self):
        return "{}".format(self.title)
    
class Question(models.Model):
    test = models.ForeignKey(Test, models.CASCADE)
    text = models.TextField()
    
    def __str__(self):
        return "{}".format(self.text)
    
class Answer(models.Model):
    question = models.ForeignKey(Question, models.CASCADE)
    text = models.CharField(max_length=200)
    correct = models.BooleanField()
    
    def __str__(self):
        return "{}".format(self.text)
    
    
class UserAnswer(models.Model):
    user = models.ForeignKey(User, models.CASCADE)
    test = models.ForeignKey(Test, models.CASCADE)
    question = models.ForeignKey(Question, models.CASCADE)
    answer = models.ForeignKey(Answer, models.CASCADE)
    
    def checkanswer(self):
        try:
            ans = Answer.objects.filter(question=self.question).get(correct=True)
            if ans == self.answer:
                return True
            else:
                return False
        except:
            return False
        
    def check_answer(self):
        if self.checkanswer():
            return mark_safe('<img src="/static/admin/img/icon-yes.svg" alt="True">')
        else:
            return mark_safe('<img src="/static/admin/img/icon-no.svg" alt="False">')