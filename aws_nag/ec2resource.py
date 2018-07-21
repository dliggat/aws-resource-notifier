import datetime
import boto3

from base import MonitoredResource
from utility import Utility


class EC2Resource(MonitoredResource):
    A_WHILE = datetime.datetime.utcnow() - datetime.timedelta(days=3)

    ABBREVIATIONS = { 'aws:autoscaling:groupname': 'asg',
                      'aws:cloudformation:stack-name': 'cf' }

    TAGS_OF_INTEREST = ['name', 'role', 'owner_slack_username'] + ABBREVIATIONS.values()

    def __init__(self):
        MonitoredResource.__init__(self, aws_resource='ec2')

    def titles(self):
        return ['id', 'region', 'launched', 'class', 'owner', 'project', 'other_tags']

    def _inspect(self):
        self.result = { key: [] for key in [r['RegionName'] for r in self.regions['Regions']] }

        for region in self.regions['Regions']:
            ec2 = boto3.resource(self.aws_resource, region['RegionName'])
            instances = ec2.instances.filter(
                Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])

            for instance in instances:
                if instance.launch_time.replace(tzinfo=None) >= self.A_WHILE:
                    continue

                details = { 'id': instance.id,
                            'region': region['RegionName'],
                            'launched': instance.launch_time.strftime('%Y-%m-%d'),
                            'class': instance.instance_type,
                            'owner': 'None',
                            'project': 'None' }
                tags = { }
                for tag in (instance.tags or []):
                    display_name = tag['Key'].lower()
                    if display_name in self.ABBREVIATIONS:
                        display_name = self.ABBREVIATIONS[display_name]
                    tags[display_name] = tag['Value']

                if 'owner' in tags:
                    details['owner'] = tags['owner']
                if 'project' in tags:
                    details['project'] = tags['project']

                # Filter the dictionary to only certain keys of interest.
                tags = { key: tags[key] for key in self.TAGS_OF_INTEREST if key in tags }
                details['other_tags'] = ', '.join(
                    ['{0}={1}'.format(k, Utility.format_for_display(v)) for (k,v) in sorted(tags.items())])
                if not details['other_tags']:
                    details['other_tags'] = 'None'

                self.result[region['RegionName']].append(details)
