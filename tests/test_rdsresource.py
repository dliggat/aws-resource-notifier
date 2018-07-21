import unittest
import pytest

from aws_resource_notifier import RDSResource

class TestRDSResource(unittest.TestCase):

    def setUp(self):
        self.obj = RDSResource()


    def testNormalSummary(self):
        self.obj.result = {   'ap-northeast-1': [],
                              'ap-northeast-2': [],
                              'ap-southeast-1': [],
                              'ap-southeast-2': [],
                              'eu-central-1': [],
                              'eu-west-1': [],
                              'sa-east-1': [],
                              'us-east-1': [   {   'launched': '2016-04-18',
                                                   'class': 'db.t2.medium',
                                                   'name': 'foobarfoobarfo',
                                                   'owner': 'None',
                                                   'project': 'None',
                                                   'region': 'us-east-1',
                                                   'other_tags': 'abc'}],
                              'us-west-1': [],
                              'us-west-2': []}


        expected="""*RDS Instances*
The following RDS instances have been running for a while:
```
  Name           : Region    : Launched   : Class        : Owner : Project : Other Tags
  -------------- : --------- : ---------- : ------------ : ----- : ------- : ----------
* foobarfoobarfo : us-east-1 : 2016-04-18 : db.t2.medium : None  : None    : abc
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
        expected="""*RDS Instances*
_Nothing to report._
"""
        self.assertEqual(self.obj.summary(), expected)


def main():
    unittest.main()

if __name__ == '__main__':
    main()
