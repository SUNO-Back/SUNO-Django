from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import UserCreationForm


User = get_user_model()

class SignUpForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        class_update_fields = ('password1', 'password2')
        # class_defualt_fields = ('password1', 'password2') 이렇게 사용해도 됨

        for field in class_update_fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields[field].widget.attrs['placeholder'] = 'password'
            if field == 'password1':
                self.fields[field].label = '비밀번호'
            else:
                self.fields[field].label = '비밀번호 확인'

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email', 'nickname',)
        labels = {
            'email' : '이메일',
            'nickname' : '닉네임'
        }
        widgets = {
            'email' : forms.EmailInput(
                attrs={
                    'placeholder' : 'example@example.com',
                    'class' : 'form-control',
                }
            ),
            'nickname' : forms.TextInput(attrs={'placeholder' : '닉네임','class' : 'form-control',})
        }

class LoginForm(forms.Form):
    email = forms.CharField(
        label='이메일',
        required=True,
        widget=forms.EmailInput(attrs={'placeholder' : 'example@example.com','class' : 'form-control',}))
    password = forms.CharField(
        label='패스워드',
        required=True,
        widget=forms.PasswordInput(attrs={'placeholder' : 'password','class' : 'form-control',}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None


    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        self.user = authenticate(email=email, password=password)

        if not self.user.is_active:
            raise forms.ValidationError('유저가 인증되지 않았습니다.')
        return cleaned_data

    # def clean(self):
    #     cleaned_data = super().clean()
    #     email = cleaned_data.get('email')
    #     password = cleaned_data.get('password')
    #
    #     if not email or not password:
    #         return cleaned_data
    #
    #     # ✅ 핵심: username에 email 넣어서 인증 (USERNAME_FIELD=email이면 이렇게 동작함)
    #     user = authenticate(username=email, password=password)
    #
    #     if user is None:
    #         raise forms.ValidationError('이메일 또는 비밀번호가 올바르지 않습니다.')
    #
    #     if not user.is_active:
    #         raise forms.ValidationError('유저가 인증되지 않았습니다.')
    #
    #     self.user = user
    #     return cleaned_data