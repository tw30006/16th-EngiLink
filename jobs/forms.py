from django.forms import ModelForm
from django import forms
from .models import Job,Job_Resume


class JobForm(ModelForm):
    class Meta:
        model = Job
        fields = [
            "title",
            "openings",
            "experience",
            "salary",
            "address",
            "description",
            "is_published",
        ]
        labels = {
            "title": "職位名稱",
            "openings": "人數需求",
            "experience": "工作經驗",
            "salary": "工作薪資",
            "address": "工作地點",
            "description": "工作內容",
            "is_published": "是否刊登",
        }

    
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)



class InterviewInvitationForm(forms.ModelForm):
    interview_date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    interview_invitation = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Job_Resume
        fields = ['interview_date', 'interview_invitation']
    
    def __init__(self, *args, **kwargs):
        super(InterviewInvitationForm, self).__init__(*args, **kwargs)
        self.fields['interview_invitation'].initial = (
            "親愛的 {{ job_resume.resume.name }}，\n\n"
            "感謝您應徵 {{ job_resume.job.title }} 一職。經過初步篩選，我們很高興通知您進入了面試環節。\n\n"
            "面試詳情如下：\n"
            "日期：<填寫面試日期>\n"
            "地點：<填寫面試地點>\n"
            "聯絡人：<填寫聯絡人姓名及聯絡方式>\n\n"
            "請攜帶相關證件及資料準時參加面試。如有任何疑問，請隨時聯絡我們。\n\n"
            "期待與您的面談！\n\n"
            "此致\n"
            "{{ company.company_name }}"
        )

class InterviewResponseForm(forms.Form):
    ACCEPT = 'accept'
    REJECT = 'reject'
    
    RESPONSE_CHOICES = [
        (ACCEPT, '接受'),
        (REJECT, '拒絕'),
    ]
    
    response = forms.ChoiceField(choices=RESPONSE_CHOICES, widget=forms.RadioSelect, required=False) 
