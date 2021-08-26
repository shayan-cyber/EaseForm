from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username
class FormParent(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    builder = models.ForeignKey(Profile, on_delete= models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False)
    accept_responses = models.BooleanField(default=True)
    banner_img = models.ImageField(upload_to = 'banners', default='banner.png', blank=True, null=True)

    def __str__(self):
        return self.title


class FormDesign(models.Model):
    label= models.TextField()
    form_parent = models.ForeignKey(FormParent, on_delete=models.CASCADE)
    character_field = models.BooleanField(default = False)
    big_text_field = models.BooleanField(default = False)
    integer_field = models.BooleanField(default = False)
    file_field = models.BooleanField(default = False)
    mcq_field = models.BooleanField(default = False)
    def __str__(self):
        return self.form_parent.title





class FormObject(models.Model):
    form_parent = models.ForeignKey(FormParent, on_delete=models.CASCADE)
    applicant = models.OneToOneField(Profile, on_delete=models.CASCADE)
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False)

    def __str__(self):
        return self.form_parent.title 

    
class FormCharacterField(models.Model):
    label_name = models.TextField(blank=True)
    field_data = models.CharField(max_length=400)
    form_object = models.ForeignKey(FormObject, on_delete= models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    type_of = models.CharField(max_length=30, default="char")

    def __str__(self):
        return self.form_object.form_parent.title

class FormBigTextField(models.Model):
    label_name = models.TextField(blank=True)
    field_data = models.TextField()
    form_object = models.ForeignKey(FormObject, on_delete= models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    type_of = models.CharField(max_length=30, default="txt")
    def __str__(self):
        return self.form_object.form_parent.title


class FormIntegerField(models.Model):
    label_name = models.TextField(blank=True)
    field_data = models.BigIntegerField()
    form_object = models.ForeignKey(FormObject, on_delete= models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    type_of = models.CharField(max_length=30, default="int")
    def __str__(self):
        return self.form_object.form_parent.title

class FormFileField(models.Model):
    label_name = models.TextField( blank=True)
    field_data = models.FileField(upload_to='fileData')
    form_object = models.ForeignKey(FormObject, on_delete= models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    type_of = models.CharField(max_length=30, default="file")
    def __str__(self):
        return self.form_object.form_parent.title





class MCQField(models.Model):
    label_name = models.TextField( blank=True)
    field_data = models.IntegerField()
    form_object = models.ForeignKey(FormObject, on_delete= models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    type_of = models.CharField(max_length=30, default="Single")
    form_design = models.ForeignKey(FormDesign, on_delete=models.CASCADE)
    def __str__(self):
        return self.form_object.form_parent.title

class Choice(models.Model):
    name = models.CharField(max_length=100)
    mcq_parent = models.ForeignKey(FormDesign, on_delete= models.CASCADE)
    def __str__(self):
        return self.name





