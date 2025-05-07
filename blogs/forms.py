from django import forms
from .models import Blog, Category, Tag, Comment
from .widgets import CustomSelectWithPlaceholder
from django_summernote.fields import SummernoteTextField


# Blog Form (Related to Creation)
class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'category', 'content', 'tags', 'short_description', 'featured_image']


    title = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter blog title',
            'class': 'form-control'
        })
    )

    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=CustomSelectWithPlaceholder(placeholder='Choose a category')
    )

    content = SummernoteTextField()

    tags = forms.CharField(
        required=False,
        help_text="Enter tags starting with # (e.g., #chair #comfortable)"
    )

    short_description = forms.CharField(
        widget=forms.Textarea(attrs={
            'id': "short_description",
            'name': "short_description",
            'class': "form-control",
            'rows': "2"
        }),
    )


    featured_image = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )

    def clean_tags(self):
        tags_text = self.cleaned_data['tags']
        if tags_text:
            tags = [tag.strip() for tag in tags_text.split() if tag.startswith("#")]
            tag_objects = []
            for tag_name in tags:
                tag_name = tag_name.lstrip("#")  #remove #
                tag_obj, created = Tag.objects.get_or_create(name=tag_name)
                tag_objects.append(tag_obj)
            return tag_objects
        return []








class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write a comment...'})
        }
