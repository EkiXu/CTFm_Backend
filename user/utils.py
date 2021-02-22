from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six
from django.contrib.sites.shortcuts import get_current_site

import json
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.ses.v20201002 import ses_client, models

from contest.models import Contest

contest = Contest.objects.all().first()

class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.is_active)
        )

account_activation_token = TokenGenerator()


cred = credential.Credential(settings.TENCENT_SECRET_ID, settings.TENCENT_SECRET_KEY) 
httpProfile = HttpProfile()
httpProfile.endpoint = "ses.tencentcloudapi.com"

clientProfile = ClientProfile()
clientProfile.httpProfile = httpProfile
client = ses_client.SesClient(cred, "ap-hongkong", clientProfile) 

def sendRegisterValidationEmail(user,current_site):
    
    templateData = {
        "contest_name":contest.name,
        "username": user.username,
        "sign_up_url":"{0}/activate/{1}/{2}".format(current_site.domain,user.id,account_activation_token.make_token(user))
    }

    req = models.SendEmailRequest()
    params = {
        "Destination": [ user.email ],
        "Template": {
            "TemplateID": settings.REGISTER_VALIDATION_EMAIL_TEMPLATE,
            "TemplateData": json.dumps(templateData)
        },
        "FromEmailAddress": settings.EMAIL,
        "Subject": "注册邮箱验证",
    }

    req.from_json_string(json.dumps(params))

    resp = client.SendEmail(req) 



def sendResetPasswordmail(user,current_site):

    templateData = {
        "contest_name":contest.name,
        "username": user.username,
        "reset_password_url":"{0}/reset_password/{1}/{2}".format(current_site.domain,user.id,account_activation_token.make_token(user))
    }

    req = models.SendEmailRequest()
    params = {
        "Destination": [ user.email ],
        "Template": {
            "TemplateID": settings.RESET_PASSWORD_EMAIL_TEMPLATE,
            "TemplateData": json.dumps(templateData)
        },
        "FromEmailAddress": settings.EMAIL,
        "Subject": "密码重置",
    }
    print(json.dumps(params))
    req.from_json_string(json.dumps(params))

    resp = client.SendEmail(req) 
    print(resp.to_json_string()) 