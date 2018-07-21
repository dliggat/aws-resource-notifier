import datetime
import boto3

from base import MonitoredResource
from utility import Utility


class RDSResource(MonitoredResource):

    A_WHILE = datetime.datetime.utcnow() - datetime.timedelta(days=3)
    ABBREVIATIONS = { 'aws:cloudformation:stack-name': 'cf' }
    TAGS_OF_INTEREST = ['role', 'owner_slack_username', 'workload-type'] + ABBREVIATIONS.values()

    def __init__(self):
        MonitoredResource.__init__(self, aws_resource='rds')

    def titles(self):
        return ['name', 'region', 'launched', 'class', 'owner', 'project', 'other_tags']

    def _inspect(self):
        self.result = { key: [] for key in [r['RegionName'] for r in self.regions['Regions']] }


        for region in self.regions['Regions']:
            rds = boto3.client(self.aws_resource, region['RegionName'])
            rds_response = rds.describe_db_instances()
            for instance in rds_response['DBInstances']:

                if instance['InstanceCreateTime'].replace(tzinfo=None) >= self.A_WHILE:
                    continue

                arn = 'arn:aws:rds:{0}:{1}:db:{2}'.format(region['RegionName'],
                                                          Utility.aws_account_id(),
                                                          instance['DBInstanceIdentifier'])

                details = { 'name': instance['DBInstanceIdentifier'],
                            'region': region['RegionName'],
                            'launched': instance['InstanceCreateTime'].strftime('%Y-%m-%d'),
                            'class': instance['DBInstanceClass'],
                            'owner': 'None',
                            'project': 'None' }
                tags = { }
                tag_response = rds.list_tags_for_resource(ResourceName=arn)
                for tag in tag_response['TagList']:
                    display_name = tag['Key'].lower()
                    if display_name in self.ABBREVIATIONS:
                        display_name = self.ABBREVIATIONS[display_name]
                    tags[display_name] = tag['Value']

                if 'owner' in tags:
                    details['owner'] = tags['owner']
                if 'project' in tags:
                    details['project'] = tags['project']

                tags = { key: tags[key] for key in self.TAGS_OF_INTEREST if key in tags }
                details['other_tags'] = ', '.join(
                    ['{0}={1}'.format(k, Utility.format_for_display(v)) for (k,v) in sorted(tags.items())])
                if not details['other_tags']:
                    details['other_tags'] = 'None'
                self.result[region['RegionName']].append(details)
