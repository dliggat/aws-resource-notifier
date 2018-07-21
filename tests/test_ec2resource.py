import unittest
import pytest

from aws_resource_notifier import EC2Resource

class TestEC2Resource(unittest.TestCase):

    def setUp(self):
        self.obj = EC2Resource()


    def testNormalSummary(self):

        self.obj.result = {   'ap-northeast-1': [],
                              'ap-northeast-2': [],
                              'ap-southeast-1': [],
                              'ap-southeast-2': [],
                              'eu-central-1': [],
                              'eu-west-1': [],
                              'sa-east-1': [],
                              'us-east-1': [   {   'id': 'i-0e2c2b95',
                                                   'launched': '2016-04-24',
                                                   'class': 't2.micro',
                                                   'owner': 'None',
                                                   'project': 'None',
                                                   'region': 'us-east-1',
                                                   'other_tags': 'cf=Robert-ApplicationStack-1IBBJEUL26QSB'}],
                              'us-west-1': [],
                              'us-west-2': [   {   'id': 'i-0fc3e9d7',
                                                   'launched': '2016-04-27',
                                                   'class': 't2.micro',
                                                   'owner': 'None',
                                                   'project': 'None',
                                                   'region': 'us-west-2',
                                                   'other_tags': 'name=andrej-lambda'},
                                               {   'id': 'i-4deced95',
                                                   'launched': '2016-04-29',
                                                   'class': 't2.micro',
                                                   'owner': 'None',
                                                   'project': 'None',
                                                   'region': 'us-west-2',
                                                   'other_tags': 'asg=dark-side-nat-NatAsgAZ1-12AF3JLDLY6YH, cf=dark-side-nat, name=Dark-Side_NatAsgAZ1'},
                                               {   'id': 'i-96779f50',
                                                   'launched': '2016-04-29',
                                                   'class': 't2.micro',
                                                   'owner': 'None',
                                                   'project': 'None',
                                                   'region': 'us-west-2',
                                                   'other_tags': 'asg=dark-side-salt-master-SaltMasterAsg-7JMD9F8R583L, cf=dark-side-salt-master, name=Dark-Side_SaltMasterAsg'},
                                               {   'id': 'i-cd2d2815',
                                                   'launched': '2016-04-27',
                                                   'class': 't2.micro',
                                                   'owner': 'None',
                                                   'project': 'None',
                                                   'region': 'us-west-2',
                                                   'other_tags': 'name=bast-mgmt-bryan-dev'},
                                               {   'id': 'i-f0759d36',
                                                   'launched': '2016-04-29',
                                                   'class': 't2.micro',
                                                   'owner': 'None',
                                                   'project': 'None',
                                                   'region': 'us-west-2',
                                                   'other_tags': 'asg=dark-side-nat-NatAsgAZ2-12MWTQ5E61HX6, cf=dark-side-nat, name=Dark-Side_NatAsgAZ2'},
                                               {   'id': 'i-9eaa5d43',
                                                   'launched': '2016-04-29',
                                                   'class': 't2.micro',
                                                   'owner': 'None',
                                                   'project': 'None',
                                                   'region': 'us-west-2',
                                                   'other_tags': 'asg=dark-side-nat-NatAsgAZ3-1ENG440KUIZN7, cf=dark-side-nat, name=Dark-Side_NatAsgAZ3'}]}

        expected="""*EC2 Instances*
The following instances have been running for a while:
```
  Id         : Region    : Launched   : Class    : Owner : Project : Other Tags
  ---------- : --------- : ---------- : -------- : ----- : ------- : ----------
* i-0e2c2b95 : us-east-1 : 2016-04-24 : t2.micro : None  : None    : cf=Robert-ApplicationStack-1IBBJEUL26QSB
* i-0fc3e9d7 : us-west-2 : 2016-04-27 : t2.micro : None  : None    : name=andrej-lambda
* i-4deced95 : us-west-2 : 2016-04-29 : t2.micro : None  : None    : asg=dark-side-nat-NatAsgAZ1-12AF3JLDLY6YH, cf=dark-side-nat, name=Dark-Side_NatAsgAZ1
* i-96779f50 : us-west-2 : 2016-04-29 : t2.micro : None  : None    : asg=dark-side-salt-master-SaltMasterAsg-7JMD9F8R583L, cf=dark-side-salt-master, name=Dark-Side_SaltMasterAsg
* i-cd2d2815 : us-west-2 : 2016-04-27 : t2.micro : None  : None    : name=bast-mgmt-bryan-dev
* i-f0759d36 : us-west-2 : 2016-04-29 : t2.micro : None  : None    : asg=dark-side-nat-NatAsgAZ2-12MWTQ5E61HX6, cf=dark-side-nat, name=Dark-Side_NatAsgAZ2
* i-9eaa5d43 : us-west-2 : 2016-04-29 : t2.micro : None  : None    : asg=dark-side-nat-NatAsgAZ3-1ENG440KUIZN7, cf=dark-side-nat, name=Dark-Side_NatAsgAZ3
```
"""
        self.assertEqual(self.obj.summary(), expected)

    def testEmptySummary(self):
        self.obj.result = {'us-east-1': [],
                           'ap-northeast-2': [],
                           'ap-northeast-1': [],
                           'sa-east-1': [],
                           'ap-southeast-1': [],
                           'ap-southeast-2': [],
                           'us-west-2': [],
                           'us-west-1': [],
                           'eu-central-1': [],
                           'eu-west-1': []}
        expected="""*EC2 Instances*
_Nothing to report._
"""
        self.assertEqual(self.obj.summary(), expected)



def main():
    unittest.main()

if __name__ == '__main__':
    main()
