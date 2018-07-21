import unittest
import pytest

from aws_resource_notifier import EIPResource

class TestEIPResource(unittest.TestCase):

    def setUp(self):
        self.obj = EIPResource()


    def testNormalSummary(self):
        self.obj.result = {   'ap-northeast-1': [],
                              'ap-northeast-2': [],
                              'ap-southeast-1': [],
                              'ap-southeast-2': [],
                              'eu-central-1': [],
                              'eu-west-1': [],
                              'sa-east-1': [],
                              'us-east-1': [],
                              'us-west-1': [],
                              'us-west-2': [   {   'id': 'eipalloc-61c95105',
                                                   'public_ip': '52.24.52.59',
                                                   'region': 'us-west-2'},
                                               {   'id': 'eipalloc-b5dc44d1',
                                                   'public_ip': '52.24.97.229',
                                                   'region': 'us-west-2'}]}

        expected="""*Elastic IPs*
The following EIPs are not associated with an instance:
```
  Id                : Region    : Public Ip
  ----------------- : --------- : ---------
* eipalloc-61c95105 : us-west-2 : 52.24.52.59
* eipalloc-b5dc44d1 : us-west-2 : 52.24.97.229
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
        expected="""*Elastic IPs*
_Nothing to report._
"""
        self.assertEqual(self.obj.summary(), expected)



def main():
    unittest.main()

if __name__ == '__main__':
    main()
