# AWS Vault App

## Table of Contents
1. [Introduction](#intro)
2. [Getting Started](#getting-started)
3. [Deploying](#deploying)
4. [Contributing](#deploying)

<a name="intro"></a>
## INTRODUCTION

This is a simple Python Lambda function that pulls secrets from the **EC2 SSM Param Store** and connects to a MySQL RDS. The source is used in conjuction with the following blog article, <a href="http://blog.justinplute.com/ec2-ssm-param-store-the-aws-vault-for-storing-secrets/" target="_blank">EC2 SSM Param Store: The AWS Vault for storing secrets</a>.

<a name="getting-started"></a>
## GETTING STARTED

To get started locally, create a Python virtual environment and install the requirements:

```bash
$ virtualenv -p python3 ssm
$ source ssm/bin/activate
$ pip install -r requirements.txt
```

<a name="deploying"></a>
## DEPLOYING

### Deploying MySQL RDS:

Upload the CloudFormation template included in this project in AWS Web Console or use the AWS CLI:

```bash
$ aws cloudformation deploy --template-file /cloudformation/mysql.rds.yaml \
  --stack-name my-mysql-rds --parameter-overrides DBUsername=Value1 DBPassword=Value2
```

Upon creation, take note of the RDS endpoint and update the `db_host` value in the `rds_config.py` file.

### Deploying Python App:

This project uses the [serverless framework](https://serverless.com/) and the plug-in, [serverless-python-requirements](https://www.npmjs.com/package/serverless-python-requirements) for deploying to AWS. You'll need to install them using `npm`:

```bash
# installs serverless framework and python-requirements plugin
$ npm i
```

**Prequisite:** <a href="https://nodejs.org/en/" target="_blank">Node.js</a> and `npm` must be installed on your computer.

**Deploy Project:**

```bash
# deploy with serverless to dev (or other environment)
$ sls deploy --stage dev
```

### Deploying Secrets into SSM

[Amazon EC2 Systems Manager Parameter Store](https://aws.amazon.com/ec2/systems-manager/parameter-store/) can centrally and securely manage secrets. And with IAM roles, you can restrict AWS resources to only access the secrets it needs for any particular environment.

The AWS Lambda function needs to fetch the MySQL Username and Redshift Password from AWS Parameter Store. There is a helper script in the project to create (and/or update) the values stored in the Parameter Store.

```bash
# example using dev environment
$ ./scripts/deploy_secrets.sh -e dev -u myuser -p mypassword
```

This will deploy secrets under the path `/env/dev`. **NOTE:** `-e` is for environment, `-u` is for user, and `-p` is for password.

<a name="contributing"></a>
## Contributing

Please [create a new GitHub issue](https://github.com/rplute/aws-vault-app/issues/new) for any feature requests, bugs, or documentation improvements.

Where possible, please also [submit a pull request](https://help.github.com/articles/creating-a-pull-request-from-a-fork/) for the change.
