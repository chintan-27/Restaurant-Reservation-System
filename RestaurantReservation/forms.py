from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from RestaurantReservation.models import User, Reservation, Review
import datetime


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30,widget= forms.TextInput(attrs={'class':'d-form','placeholder':'First Name'}))
    last_name = forms.CharField(max_length=30,widget= forms.TextInput(attrs={'class':'d-form','placeholder':'Last Name'}))
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.',widget= forms.TextInput(attrs={'class':'d-form','placeholder':'Email'}))
    phone = forms.CharField(max_length=10,widget= forms.TextInput(attrs={'class':'d-form','placeholder':'phone'}))
    username = forms.CharField(max_length=254,widget= forms.TextInput(attrs={'class':'d-form','placeholder':'username'}))
    password1=forms.CharField(max_length=20,widget=forms.PasswordInput(attrs={'class':'d-form','placeholder':'Password'}))
    password2=forms.CharField(max_length=20,widget=forms.PasswordInput(attrs={'class':'d-form','placeholder':'Confirm Password'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'phone', 'password1', 'password2', )
    def clean(self):
        cleaned_data = super(UserCreationForm, self).clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        phone = cleaned_data.get("phone")
        if password1 != password2:
            raise forms.ValidationError(
                "password and confirm_password does not match"
            )

class SignUpHotel(UserCreationForm):
    first_name = forms.CharField(max_length=30,widget= forms.TextInput(attrs={'class':'d-form','placeholder':''}))
    last_name = forms.CharField(max_length=30,widget= forms.TextInput(attrs={'class':'d-form','placeholder':''}))
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.',widget= forms.TextInput(attrs={'class':'d-form','placeholder':''}))
    phone = forms.CharField(max_length=10,widget= forms.TextInput(attrs={'class':'d-form','placeholder':''}))
    username = forms.CharField(max_length=254,widget= forms.TextInput(attrs={'class':'d-form','placeholder':''}))
    password1=forms.CharField(max_length=20,widget=forms.PasswordInput(attrs={'class':'d-form','placeholder':''}))
    password2=forms.CharField(max_length=20,widget=forms.PasswordInput(attrs={'class':'d-form','placeholder':''}))
    CHOICES = (
    ("NORMAL","NORMAL"),
    ("CAFE","CAFE"),
    ("TOP FLOOR/ TERRACE","TOP FLOOR/ TERRACE"),
    ("HIGHWAY SIDE","HIGHWAY SIDE"),
    ("NATURAL VIEW","NATURAL VIEW"),
    ("SEA VIEW","SEA VIEW"),
    )
    location = forms.ChoiceField(choices = CHOICES,widget=forms.Select(attrs={'class':'d-form','placeholder':''}))
    restaurant_name = forms.CharField(max_length = 500,widget= forms.TextInput(attrs={'class':'d-form','placeholder':''}))
    description = forms.CharField(max_length = 500,widget= forms.TextInput(attrs={'class':'d-form','placeholder':''}))
    city = forms.CharField(max_length = 50,widget= forms.TextInput(attrs={'class':'d-form','placeholder':''}))
    ratingbystaff = forms.IntegerField(max_value = 5,min_value = 0,widget= forms.NumberInput(attrs={'class':'d-form','placeholder':''}))
    ratingbyfood = forms.IntegerField(max_value = 5,min_value = 0,widget= forms.NumberInput(attrs={'class':'d-form','placeholder':''}))
    ratingbylocation = forms.IntegerField(max_value = 5,min_value = 0,widget= forms.NumberInput(attrs={'class':'d-form','placeholder':''}))
    ratingbyhygiene = forms.IntegerField(max_value = 5,min_value = 0,widget= forms.NumberInput(attrs={'class':'d-form','placeholder':''}))
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'phone', 'password1', 'password2', )

    def clean(self):
        cleaned_data = super(UserCreationForm, self).clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        phone = cleaned_data.get("phone")
        if password1 != password2:
            raise forms.ValidationError(
                "password and confirm_password does not match"
            )


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=254,widget= forms.TextInput(attrs={'class':'d-form ','placeholder':'Username'}))
    password = forms.CharField(max_length=20,widget=forms.PasswordInput(attrs={'class':'d-form ','placeholder':'Password'}))

    class Meta:
        model = User

class ReviewForm(forms.Form):
    review_title = forms.CharField(max_length=254,widget= forms.TextInput(attrs={'class':'d-form','placeholder':'TITLE'}))
    review = forms.CharField(max_length=500,widget= forms.TextInput(attrs={'class':'d-form','placeholder':'REVIEW'}))
    ratingbystaff = forms.IntegerField(min_value = 0,max_value = 5,widget= forms.NumberInput(attrs={'class':'d-form','placeholder':'RATING BY STAFF'}))
    ratingbyfood = forms.IntegerField(min_value = 0,max_value = 5,widget= forms.NumberInput(attrs={'class':'d-form','placeholder':'RATING BY FOOD'}))
    ratingbylocation = forms.IntegerField(min_value = 0,max_value = 5,widget= forms.NumberInput(attrs={'class':'d-form','placeholder':'RATING BY LOCATION'}))
    ratingbyhygiene = forms.IntegerField(min_value = 0,max_value = 5,widget= forms.NumberInput(attrs={'class':'d-form','placeholder':'RATING BY HYGIENE'}))

    class Meta:
        model = Review


class PhotosForm(forms.Form):
    image = forms.ImageField(widget= forms.FileInput(attrs={'class':'d-form'}))
