# AWS CDK Private Web Service

This project deploys a private web service hosted on an EC2 instance using AWS CDK. The web server runs in an isolated subnet within a VPC and is accessible only within the same VPC. It also includes AWS Systems Manager (SSM) integration for secure management of the EC2 instance.

---

## Features

- **VPC**: A private VPC with isolated subnets across 2 Availability Zones.
- **EC2 Instance**: The web service is hosted on an EC2 instance in an isolated subnet.
- **Security Group**: Configured to allow HTTP traffic (port 80) only from within the VPC.
- **IAM Role**: Grants SSM permissions to the EC2 instance for secure management.
- **SSM VPC Endpoints**: Enables the use of AWS Systems Manager in the isolated environment without internet access.

---

## Availability and Redundancy !!!
- The VPC spans **2 Availability Zones (AZs)**, creating subnets in each AZ.
- While the current setup deploys a **single EC2 instance**, the availability can be improved by:
  - Deploying additional instances in the other AZ.
  - Introducing an **Auto Scaling Group** and a **Load Balancer** for redundancy and fault tolerance.

---

## Prerequisites

Before you can deploy this project, ensure the following are installed and set up:

1. **AWS CLI**:
   - Install and configure it with your AWS credentials.
   - Run:
     ```bash
     aws configure
     ```

2. **AWS CDK**:
   - Install AWS CDK globally:
     ```bash
     npm install -g aws-cdk
     ```

3. **Python**:
   - Ensure Python 3.7 or later is installed.

  
4. **Node.js**:
   - Required for the AWS CDK CLI. Install Node.js from [here](https://nodejs.org/).

---

## How to Run This Code

Follow these steps to clone the repository and deploy the stack:

### 1. Clone the Repository

### 2.Create a Virtual enivronment

To manually create a virtualenv on MacOS and Linux:

```
$ python -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!
