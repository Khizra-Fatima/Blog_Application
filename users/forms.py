from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile


#SignUp Form
class SignupForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    


#Login Form
class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=120, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))



#ProfileUpdate Form
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_image', 'bio']

        widgets = {
            'profile_image': forms.FileInput(attrs={'class': 'form-control-file'})
        }



# UsernameChange Form
'''class UsernameChangeForm(forms.ModelForm):
    new_username = forms.CharField(label='New Username', max_length=150)

    class Meta:
        model = User
        fields = ['username']

    def clean_new_username(self):
        new_username = self.cleaned_data.get('new_username')
        if User.objects.filter(username=new_username).exists():
            raise forms.ValidationError("This username is already taken.")
        return new_username

    def save(self, commit=True):
        user = super(UsernameChangeForm, self).save(commit=False)
        user.username = self.cleaned_data['new_username']
        if commit:
            user.save()
        return user'''



# EmailChange Form
class EmailChangeForm(forms.ModelForm):
    email = forms.EmailField(label='New Email', max_length=150)

    class Meta:
        model = User
        fields = ['email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already used for an account.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

       