import os
import boto3
import datetime
import yaml
from base64 import b64decode


def configuration(context):
    result = {}
    lambda_arn = context.invoked_function_arn.split(":")
    account_num = lambda_arn[4]
    with open(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'conf/config.yml')), 'r') as f:
        configs = yaml.load(f)['aws_entities']

    this_config = None
    for config in configs:
        if config['aws_acct'] == account_num:
            this_config = config
            break
    if this_config is None:
        raise ValueError("Unable to find configuration")

    result['slack_plaintext_url'] = 'https://' + boto3.client('kms').decrypt(
        CiphertextBlob=b64decode(this_config['slack_encrypted_url']))['Plaintext']
    result['slack_target_id'] = this_config['slack_target_id']
    result['signin_url'] = this_config['signin_url']
    result['title'] = "Report for account *{0}* (`{1}`) on *{2}*".format(
        this_config['description'],
        int(account_num),
        datetime.datetime.today().strftime("%a %Y-%m-%d"))
    return result
