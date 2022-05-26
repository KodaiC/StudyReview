from templated_mail.mail import BaseEmailMessage
from django.contrib.auth.tokens import default_token_generator
from djoser import utils
from config import settings


DOMAIN = "localhost:3000"


class EmailManager(BaseEmailMessage):
    def send(self, to, *args, **kwargs):
        self.render()
        self.to = to
        self.cc = kwargs.pop("cc", [])
        self.bcc = kwargs.pop("bcc", [])
        self.reply_to = kwargs.pop("reply_to", [])
        self.from_email = kwargs.pop(
            "from_email",
            f"Study Review<{settings.DEFAULT_FROM_EMAIL}>"
        )
        super(BaseEmailMessage, self).send(*args, **kwargs)


class ActivationEmail(EmailManager):
    template_name = "api/activation.html"

    def get_context_data(self):
        context = super().get_context_data()
        user = context.get("user")
        context["name"] = user.username
        context["uid"] = utils.encode_uid(user.pk)
        context["token"] = default_token_generator.make_token(user)
        context["url"] = settings.DJOSER["ACTIVATION_URL"].format(**context)
        context["domain"] = DOMAIN
        return context


class ConfirmationEmail(EmailManager):
    template_name = "api/confirmation.html"

    def get_context_data(self):
        context = super().get_context_data()
        user = context.get("user")
        context["name"] = user.username
        return context


class PasswordResetEmail(EmailManager):
    template_name = "api/password_reset.html"

    def get_context_data(self):
        context = super().get_context_data()
        user = context.get("user")
        context["name"] = user.username
        context["uid"] = utils.encode_uid(user.pk)
        context["token"] = default_token_generator.make_token(user)
        context["url"] = settings.DJOSER["PASSWORD_RESET_CONFIRM_URL"].format(**context)
        context["domain"] = DOMAIN
        return context


class PasswordChangedConfirmationEmail(EmailManager):
    template_name = "api/password_changed_confirmation.html"

    def get_context_data(self):
        context = super().get_context_data()
        user = context.get("user")
        context["name"] = user.username
        return context


class EmailResetEmail(EmailManager):
    template_name = "api/email_reset.html"

    def get_context_data(self):
        context = super().get_context_data()
        user = context.get("user")
        context["name"] = user.username
        context["uid"] = utils.encode_uid(user.pk)
        context["token"] = default_token_generator.make_token(user)
        context["url"] = settings.DJOSER["USERNAME_RESET_CONFIRM_URL"].format(**context)
        context["domain"] = DOMAIN
        return context


class UsernameChangedConfirmationEmail(EmailManager):
    template_name = "api/email_changed_confirmation.html"

    def get_context_data(self):
        context = super().get_context_data()
        user = context.get("user")
        context["name"] = user.username
        return context
