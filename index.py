import os
import logging; logging.basicConfig()

from aws_resource_notifier import EC2Resource
from aws_resource_notifier import EIPResource
from aws_resource_notifier import RDSResource
from aws_resource_notifier import Slack
from aws_resource_notifier import configuration

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
    config = configuration(context)
    logger.info("Using configuration: %s", str(config))

    # Build a usage summary for each resource type.
    title = '> {0}'.format(config['title'])
    url = '> {0}'.format(config['signin_url'])
    slack_text = [title, url]
    for resource in [EC2Resource(), RDSResource(), EIPResource()]:
        slack_text.append(resource.summary())
    emoji_suffix = ':checkered_flag: :checkered_flag: :checkered_flag:'
    slack_text.append(emoji_suffix)

    final_output = "\n".join(slack_text)
    if os.getenv('DRY_RUN') == 'true':
        logging.info("Environment variable DRY_RUN is 'true'; will not post results to Slack")
        print(final_output)
    else:
        slack = Slack(channel=config['slack_target_id'],
                      url=config['slack_plaintext_url'],
                      text=final_output)
        slack.invoke()


if __name__ == '__main__':
    from aws_resource_notifier import LocalContext
    handler(None, LocalContext())
