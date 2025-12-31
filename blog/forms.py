# blog/forms.py

from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        # [수정 1] content를 body로 변경
        fields = ['body'] 
        
        widgets = {
            # [수정 2] content를 body로 변경
            'body': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': '댓글을 남겨주세요',
                'rows': 3
            }),
        }
        labels = {
            # [수정 3] content를 body로 변경
            'body': '내용',
        }