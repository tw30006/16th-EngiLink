from django.apps import AppConfig


class ResumeConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "resumes"

    def ready(self):
        import educations.rules
        educations.rules.add_rule()