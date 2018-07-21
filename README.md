AWS Nag
========

[![Build Status](https://travis-ci.com/TriNimbus/aws-nag.svg?token=qUgWaG44GiU7kPHZFG3v&branch=master)](https://travis-ci.com/TriNimbus/aws-nag)

## Setting Up on an AWS Account

1) Launch the `aws-nagbot-stack` into an account:

```bash
aws cloudformation create-stack --stack-name aws-nagbot-stack \
--template-body file://cloudformation/stack.yaml \
--capabilities CAPABILITY_IAM \
--parameters ParameterKey=ScheduleExpression,ParameterValue='cron(49 23 ? * MON-FRI *)'
```

2) Encrypt the Slack URL and place `CiphertextBlob` into a new entry in `config/config.yml`:

```bash
aws kms encrypt --key-id alias/aws-nagbot-key \
--plaintext hooks.slack.com/services/FOO/BAR/BAZ
```

3) Grab the Travis credentials for the newly created TravisCI IAM user; e.g. `aws-nagbot-stack-TravisCIUser-SWL0NR4GUNVA` (available in the CF stack outputs)

4) Encrypt the credentials for Travis, and place the result under `env` into the `.travis.yml` file. The `ARN` of the Lambda function is also necessary (available in the CF stack outputs):

```bash
travis encrypt AWS_ACCESS_KEY_ID=key \
AWS_SECRET_ACCESS_KEY=secret \
ARN=arn:aws:lambda:us-west-2:000000000000:function:AWS-Nagbot
```

## Running Unit Tests

```bash
make test
```

## Invoking the Lambda Function Locally

Note that the `Makefile` target sets `DRY_RUN=true`, so this will not directly post to the Slack endpoint configured in `conf/config.yml` without modification.

```
make invoke
```

## Updating the Slack Post Event
Each configured AWS environment has a `AWS::Events::Rule` that invokes the Lambda function at a certain time each day. This can be updated with a Cloudformation `update-stack`:

```bash
aws cloudformation update-stack --stack-name aws-nagbot-stack \
--template-body file://cloudformation/stack.yaml \
--capabilities CAPABILITY_IAM \
--parameters ParameterKey=ScheduleExpression,ParameterValue='cron(21 0 ? * MON-FRI *)'
```

Note that the `ScheduleExpression` is written in UTC-terms; i.e. `cron(21 0 ? * MON-FRI *)` refers to once-daily during weekdays at 00:21 UTC, or 17:21 PDT.

## Deploying Code Changes
To deploy changes **to all configured AWS accounts**, simply merge `master` into `release`. This can be done directly in `git` in a shell, or on GitHub by creating a `release <= master` Pull Request. In general, favour the latter.

Deployment is intended to happen from within TravisCI, but it will work locally provided `ARN` is `export`-ed and set correctly in the current shell. Simply run:

```bash
make deploy
```

In general, this should not be necessary, however.



