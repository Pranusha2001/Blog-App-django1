from django import forms
from .models import UserProfile, BlogPost
from django.utils.text import slugify

class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('phone_no', 'bio', 'facebook', 'instagram', 'linkedin', 'image', )
     
        
class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ('title', 'content', 'image')
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Title of the Blog'}),
            'slug': forms.HiddenInput(),
            'content': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Content of the Blog'}),
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        slug = slugify(title)
        if BlogPost.objects.filter(slug=slug).exists():
            raise forms.ValidationError('A blog post with this title already exists.')
        return title

    def save(self, commit=True):
        instance = super(BlogPostForm, self).save(commit=False)
        instance.slug = slugify(instance.title)
        if commit:
            instance.save()
        return instance