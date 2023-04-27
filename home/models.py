from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.timezone import now
from Blog.config import ROLE_CHOICES
    
def getChoices(item):
        """
        Return a tuple of choices used in django model for choices
        """
        choices_list = []
        is_list = isinstance(item, list)

        if is_list:
            for _key in item:
                choices_list.append((_key, _key))
        else:
            for _key in item:
                choices_list.append((_key, item[_key]))

        return tuple(choices_list)
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(upload_to="profile_pics", blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    phone_no = models.IntegerField(blank=True, null=True)
    facebook = models.CharField(max_length=300, blank=True, null=True)
    instagram = models.CharField(max_length=300, blank=True, null=True)
    linkedin = models.CharField(max_length=300, blank=True, null=True)
    
    def __str__(self):
        return str(self.user)

class BlogPost(models.Model):
    title=models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    slug=models.CharField(max_length=130)
    content=models.TextField()
    image = models.ImageField(upload_to="profile_pics", blank=True, null=True)
    dateTime=models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=True)
    published_at = models.DateTimeField(blank=True, null=True)
    role = models.CharField(
        max_length=10,
        choices=getChoices(ROLE_CHOICES),
    )
    
    def __str__(self):
        return str(self.author) +  " Blog Title: " + self.title
    
    def get_absolute_url(self):
        return reverse('blogs')
    
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    blog = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)   
    dateTime=models.DateTimeField(default=now)

    def __str__(self):
        return self.user.username +  " Comment: " + self.content

class drfprofile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=1)
    role = models.CharField(
        max_length=10,
        choices=getChoices(ROLE_CHOICES),
        default=ROLE_CHOICES['user']
        
    )
    

