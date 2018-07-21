import os
import boto3
import collections as c
from abc import ABCMeta, abstractmethod

from jinja2 import Template
from jinja2 import Environment, FileSystemLoader


def column_display_name(value):
    return value.replace('-', ' ').replace('_', ' ').title()


class MonitoredResource(object):
    __metaclass__ = ABCMeta

    def __init__(self, aws_resource=None):
        self.aws_resource = aws_resource
        self.client = boto3.client(self.aws_resource)
        self.regions = boto3.client('ec2').describe_regions()
        self._result = None

    def summary(self):
        env = Environment(trim_blocks=True, lstrip_blocks=True)
        env.filters['column_display_name'] = column_display_name
        env.loader = FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates'))
        template = env.get_template('{0}.markdown.jinja'.format(self.__class__.__name__.lower()))
        rendered = template.render(result=self.result,
                                   titles=self._format_titles,
                                   is_empty=self._is_empty)
        return rendered

    @property
    def _is_empty(self):
        return sum([len(items) for _, items in self.result.iteritems()]) == 0

    @property
    def _format_titles(self):
        format_dict = c.OrderedDict()
        for title in self.titles():
            # Set the left-adjustment size for the columns as the max(value, column_name).
            format_dict[title] = max(
                max([len(k[title]) for k in sum([self.result[d] for d in self.result], [])] or [0]),
                len(column_display_name(title)))
            # We don't need a left-adjustment for the final title.
            if title == self.titles()[-1]:
                format_dict[title] = len(title)
        return format_dict

    @abstractmethod
    def _inspect(self):
        pass

    @abstractmethod
    def titles(self):
        pass

    @property
    def result(self):
        if not self._result:
            self._inspect()
        return self._result

    @result.setter
    def result(self, value):
        self._result = value
