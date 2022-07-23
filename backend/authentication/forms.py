from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms  
from authentication.models import User  
from django.contrib.auth import get_user_model  
  
User = get_user_model()  
  
class CustomUserCreationForm(UserCreationForm):  

    ADMIN = 1; MENTOR = 2; USER = 3

    ROLE_CHOICES = (
        (ADMIN, 'Admin'),
        (MENTOR, 'Supervisor'),
        (USER, 'Operator')
    )
  
    password1 = forms.CharField(label='Password',widget=forms.PasswordInput)  
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
  
    class Meta:  
        model = User  
        fields = ('username', 'email' ,'role', 'phone')  
      
    def clean_username(self):  
        username = self.cleaned_data.get('username')  
        qs = User.objects.filter(username=username)  
        if qs.exists():  
            raise forms.ValidationError("Username is taken")  
        return username  
  
    def clean(self):  
        '''  
        Verify both passwords match.  
        '''  
        cleaned_data = super().clean()  
        password1 = cleaned_data.get("password1")  
        password2 = cleaned_data.get("password2")  
          
        if password1 is not None and password1 != password2:  
            self.add_error("password2", "Your passwords must match")  
        return cleaned_data  
  
    def save(self, commit=True):  
        # Save the provided password in hashed format  
        user = super().save(commit=False)  
        user.set_password(self.cleaned_data["password1"])
        if commit:  
            user.save()  
        return user          
      
  
class CustomUserChangeForm(UserChangeForm):  
    class Meta:  
        model = User  
        fields = ('username', )  
  
    # def clean_password(self):  
    #     # Regardless of what the user provides, return the initial value.  
    #     # This is done here, rather than on the field, because the  
    #     # field does not have access to the initial value  
    #     return self.initial["password1"]  