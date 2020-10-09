#How to install the Tag Tamer solution

Version - 3

Author: Bill Dry - bdry@amazon.com - +1-919-345-7347

#Tag Tamer Installation Procedure

##Before you begin (Prerequisites):

a) Identity the target AWS account where you would like to deploy Tag Tamer

b) Identify the EC2 Key Pair you will use to access the Tag Tamer Web App EC2 instance ("Web App")

c) Identify the IAM role that AWS CloudFormation will use to deploy DynamoDB, EC2 & IAM resources

d) Identify the X.509 certificate to use for ALB if loadbalancer needs to be deployed in public subnet. If you plan to install a self-signed certificate, instructions are provided below.


##Installation option #1: Web App deployed in a private subnet

Step 1 - Download the AWS CloudFormation template at the following link. It specifies the Tag Tamer solution infrastructure.

https://github.com/billdry/tag-tamer/blob/master/installation%20procedures/tagtamer_private.yaml

Step 2 - Deploy the CloudFormation Template downloaded in step 1 into your AWS account. You will need an EC2 Key Pair, am AMI ID such as amzn2-ami-hvm-x86_64-gp2, a VPC ID, Private Subnet, a source IP range for incoming management connections and an AWS SES validated email address.

Step 3 - Verify the correct operation of the Tag Tamer Web App by browsing to https://<EC2Instance.PrivateDnsName>/sign-in The CloudFormation outputs list the exact sign-in URL you must use.

##Installation option #2: Web App deployed in a private subnet behind ALB in a public subnet

Step 1 - Download the AWS CloudFormation template at the following link. It specifies the Tag Tamer solution infrastructure.

https://github.com/billdry/tag-tamer/blob/master/installation%20procedures/tagtamer_public.yaml

Step 2 - Deploy the CloudFormation Template downloaded in step 1 into your AWS account. You will need an EC2 Key Pair, am AMI ID such as amzn2-ami-hvm-x86_64-gp2, an X.509 certificate, a source IP range for incoming management connections and an AWS SES validated email address.

Step 3 - Verify the correct operation of the Tag Tamer Web App by browsing to https://<EC2Instance.PublicDnsName>/sign-in The CloudFormation outputs list the exact sign-in URL you must use.

###How to create a self-signed certificate and import it to your AWS account

openssl genrsa 2048 > my-aws-private.key
openssl req -new -x509 -nodes -sha1 -days 3650 -extensions v3_ca -key my-aws-private.key > my-aws-public.crt
openssl pkcs12 -inkey my-aws-private.key -in my-aws-public.crt -export -out my-aws-public.p12
aws acm import-certificate --certificate fileb://my-aws-public.crt --private-key fileb://my-aws-private.key

END OF PROCEDURE
