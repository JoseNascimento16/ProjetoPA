from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six


class TokenGenerator(PasswordResetTokenGenerator):

    def _make_hash_value(self, user, timestamp):
        return six.text_type(user.pk)+six.text_type(timestamp)+six.text_type(user.classificacao.email_ativado)

    # def _make_hash_value(self, user, timestamp: int) -> str:
    #     return super()._make_hash_value(user, timestamp)


generate_token = TokenGenerator()