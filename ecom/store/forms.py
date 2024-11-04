from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Product, UserProfile, Address, UserAddresses
from ckeditor.widgets import CKEditorWidget

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    mobile = forms.CharField(max_length=15, required=True)
    first_name = forms.CharField(max_length=30, required=True)  # New field
    last_name = forms.CharField(max_length=30, required=True)   # New field
    house_no = forms.IntegerField(required=True)
    street_name = forms.CharField(max_length=255, required=True)
    address_lines = forms.CharField(widget=forms.Textarea, required=True)
    city = forms.CharField(max_length=255, required=True)
    region = forms.CharField(max_length=255, required=True)
    pincode = forms.IntegerField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'mobile', 'house_no', 'street_name', 'address_lines', 'city', 'region', 'pincode']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']  # Save first name
        user.last_name = self.cleaned_data['last_name']    # Save last name
        if commit:
            user.save()

            # Create UserProfile with mobile number as an integer
            mobile = self.cleaned_data['mobile']
            UserProfile.objects.create(user=user, mobile=int(mobile))  # Convert to int before saving

            # Create Address
            address = Address.objects.create(
                house_no=self.cleaned_data['house_no'],
                street_name=self.cleaned_data['street_name'],
                address_lines=self.cleaned_data['address_lines'],
                city=self.cleaned_data['city'],
                region=self.cleaned_data['region'],
                pincode=self.cleaned_data['pincode']
            )

            # Associate address with the user (UserAddresses)
            UserAddresses.objects.create(user=user, address=address, is_default=True)

        return user


class ProductForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Product
        fields = ['product_name', 'product_price', 'category', 'discount', 'product_description', 'img']
