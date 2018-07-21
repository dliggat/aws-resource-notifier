import boto3

from base import MonitoredResource


class EIPResource(MonitoredResource):

    def __init__(self):
        MonitoredResource.__init__(self, aws_resource='ec2')

    def titles(self):
        return ['id', 'region', 'public_ip']

    def _inspect(self):
        self.result = { key: [] for key in [r['RegionName'] for r in self.regions['Regions']] }

        for region in self.regions['Regions']:
            ec2eipclient = boto3.client(self.aws_resource, region['RegionName'])
            eip_response = ec2eipclient.describe_addresses()
            for eip in eip_response['Addresses']:
                if 'AssociationId' not in eip:
                    details = { 'id': eip.get('AllocationId', 'None'),
                                'region': region['RegionName'],
                                'public_ip': eip['PublicIp']}
                    self.result[region['RegionName']].append(details)
