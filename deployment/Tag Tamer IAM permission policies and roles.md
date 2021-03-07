# Tag Tamer IAM permission policies & roles

## Tag Tamer AWS CloudFormation IAM permission policy to deploy Tag Tamer stack templates

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "lambda:CreateFunction",
                "ec2:AuthorizeSecurityGroupIngress",
                "ec2:DeleteSubnet",
                "wafv2:AssociateWebACL",
                "ec2:DescribeInstances",
                "iam:RemoveRoleFromInstanceProfile",
                "iam:CreateRole",
                "wafv2:CreateWebACL",
                "iam:AttachRolePolicy",
                "dynamodb:DeleteTable",
                "cognito-idp:CreateIdentityProvider",
                "cognito-idp:DeleteUserPoolDomain",
                "iam:AddRoleToInstanceProfile",
                "ec2:DeleteRouteTable",
                "elasticloadbalancing:DeleteLoadBalancer",
                "ec2:DescribeInternetGateways",
                "ec2:DeleteVolume",
                "ssm:DeleteParameter",
                "iam:DetachRolePolicy",
                "dynamodb:DescribeTable",
                "ssm:AddTagsToResource",
                "ec2:CreateRoute",
                "ec2:CreateInternetGateway",
                "ec2:RevokeSecurityGroupEgress",
                "ec2:DescribeVolumes",
                "elasticloadbalancing:CreateRule",
                "dynamodb:DescribeContinuousBackups",
                "ec2:DeleteInternetGateway",
                "lambda:DeleteFunction",
                "ec2:DescribeKeyPairs",
                "ec2:DescribeRouteTables",
                "cognito-idp:DeleteGroup",
                "ec2:DetachVolume",
                "iam:GetRole",
                "wafv2:DisassociateWebACL",
                "lambda:InvokeFunction",
                "ec2:CreateTags",
                "cognito-idp:DeleteUserPoolClient",
                "elasticloadbalancing:CreateTargetGroup",
                "ec2:CreateRouteTable",
                "iam:DeleteRole",
                "ec2:RunInstances",
                "elasticloadbalancing:DeregisterTargets",
                "ssm:GetParameters",
                "ec2:DisassociateRouteTable",
                "ssm:DeleteParameters",
                "ssm:PutParameter",
                "ec2:RevokeSecurityGroupIngress",
                "dynamodb:CreateTable",
                "lambda:UpdateFunctionCode",
                "cognito-idp:CreateUserPoolClient",
                "ec2:DeleteNatGateway",
                "lambda:PublishVersion",
                "ec2:DeleteVpc",
                "ec2:CreateSubnet",
                "ec2:DescribeSubnets",
                "ec2:DeleteKeyPair",
                "iam:CreateInstanceProfile",
                "cognito-idp:DeleteUserPool",
                "ec2:DescribeAddresses",
                "ec2:DeleteTags",
                "ec2:CreateNatGateway",
                "cognito-idp:CreateGroup",
                "cognito-idp:CreateUserPool",
                "ec2:CreateVpc",
                "iam:DeletePolicy",
                "cognito-idp:CreateUserPoolDomain",
                "iam:PassRole",
                "elasticloadbalancing:CreateListener",
                "ec2:CreateSecurityGroup",
                "ec2:ModifyVpcAttribute",
                "elasticloadbalancing:DeleteRule",
                "iam:DeleteInstanceProfile",
                "ec2:ReleaseAddress",
                "ec2:AuthorizeSecurityGroupEgress",
                "cognito-idp:DeleteIdentityProvider",
                "elasticloadbalancing:CreateLoadBalancer",
                "ec2:TerminateInstances",
                "ec2:DescribeTags",
                "ec2:DeleteRoute",
                "lambda:UpdateFunctionConfiguration",
                "ec2:DescribeNatGateways",
                "elasticloadbalancing:DeleteTargetGroup",
                "ec2:AllocateAddress",
                "ec2:DescribeSecurityGroups",
                "iam:CreatePolicy",
                "ec2:DescribeImages",
                "ec2:DescribeVpcs",
                "ec2:DeleteSecurityGroup",
                "elasticloadbalancing:DeleteListener"
            ],
            "Resource": "*"
        }
    ]
}
```
## Tag Tamer web app instance profile

### IAM Permission policy for instance profile IAM role

#### Inline Policies attached to instance profile IAM role
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": [
                "cognito-identity:GetId",
                "cognito-identity:GetCredentialsForIdentity"
            ],
            "Resource": "*",
            "Effect": "Allow",
            "Sid": "CognitoIdentity"
        },
        {
            "Action": [
                "ssm:GetParametersByPath"
            ],
            "Resource": "arn:aws:ssm:<YOUR_SSM_REGION>:<YOUR_AWS_ACCOUNT>:parameter/tag-tamer/*",
            "Effect": "Allow",
            "Sid": "SSMParameters"
        },
        {
            "Action": [
                "cognito-idp:AdminListGroupsForUser"
            ],
            "Resource": "arn:aws:cognito-idp:<YOUR_COGNITO_REGION>:<YOUR_AWS_ACCOUNT>:userpool/<YOUR_USER_POOL_ID>",
            "Effect": "Allow",
            "Sid": "CognitoUserPool"
        }
    ]
}
```
#### AWS managed policies attached to instance profile IAM role

```
arn:aws:iam::aws:policy/CloudWatchAgentServerPolicy
arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore
```

#### IAM role trust policy

```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "ec2.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

## role-based-tagger.py

### IAM permission policy

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": "dynamodb:GetItem",
            "Resource": "arn:aws:dynamodb:*:*:table/tag_tamer_roles"
        },
        {
            "Sid": "VisualEditor1",
            "Effect": "Allow",
            "Action": [
                "iam:ListPolicies",
                "ec2:DescribeInstances",
                "iam:ListRoleTags",
                "ec2:DeleteTags",
                "ec2:DescribeTags",
                "ec2:CreateTags",
                "iam:TagRole",
                "ec2:DescribeVolumes",
                "iam:ListRoles",
                "iam:ListRolePolicies",
                "iam:TagUser"
            ],
            "Resource": "*"
        }
    ]
}
```

### IAM role trust policy

```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

## Example Cognito User Pool Groups
### Example IAM role permissions policy allowing Amazon Cognito User Pool Group to perform all Tag Tamer web app actions

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "dynamodb:PutItem",
                "dynamodb:GetItem",
                "dynamodb:Scan",
                "dynamodb:UpdateItem"
            ],
            "Resource": [
                "arn:aws:dynamodb:*:*:table/tag_tamer_roles",
                "arn:aws:dynamodb:*:*:table/tag_tamer_tag_groups"
            ]
        },
        {
            "Sid": "VisualEditor1",
            "Effect": "Allow",
            "Action": [
                "sts:AssumeRole",
                "lambda:TagResource",
                "ec2:DescribeInstances",
                "servicecatalog:SearchProducts",
                "iam:GetRole",
                "iam:ListRoleTags",
                "eks:ListTagsForResource",
                "rds:DescribeGlobalClusters",
                "servicecatalog:UntagResource",
                "eks:DescribeNodegroup",
                "ec2:DescribeVolumes",
                "config:DescribeConfigRules",
                "s3:PutObjectTagging",
                "iam:ListRolePolicies",
                "servicecatalog:DisassociateTagOptionFromResource",
                "servicecatalog:UpdateTagOption",
                "s3:DeleteObjectTagging",
                "iam:ListPolicies",
                "eks:ListNodegroups",
                "lambda:ListFunctions",
                "config:PutConfigRule",
                "ec2:CreateTags",
                "servicecatalog:ListTagsForResource",
                "s3:GetObject",
                "eks:DescribeCluster",
                "eks:ListClusters",
                "rds:RemoveTagsFromResource",
                "config:UntagResource",
                "rds:DescribeOptionGroups",
                "servicecatalog:DeleteTagOption",
                "s3:GetBucketTagging",
                "ec2:DeleteTags",
                "iam:TagRole",
                "s3:ReplicateTags",
                "s3:ListBucket",
                "servicecatalog:ListTagOptions",
                "s3:PutBucketTagging",
                "servicecatalog:DescribeTagOption",
                "lambda:ListTags",
                "servicecatalog:DescribeProduct",
                "rds:DescribeDBInstances",
                "s3:GetObjectTagging",
                "servicecatalog:AssociateTagOptionWithResource",
                "rds:AddTagsToResource",
                "servicecatalog:CreateTagOption",
                "eks:UntagResource",
                "ec2:DescribeTags",
                "lambda:GetFunction",
                "iam:ListRoles",
                "servicecatalog:TagResource",
                "iam:TagUser",
                "config:ListTagsForResource",
                "servicecatalog:SearchProductsAsAdmin",
                "servicecatalog:DescribeProductAsAdmin",
                "s3:ListAllMyBuckets",
                "rds:ListTagsForResource",
                "config:TagResource",
                "eks:TagResource",
                "rds:DescribeDBClusterEndpoints",
                "rds:DescribeDBClusters"
            ],
            "Resource": "*"
        }
    ]
}
```

### Example IAM role permissions policy allowing user to perform all Tag Tamer web app actions except change Tag Groups

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "dynamodb:GetItem",
                "dynamodb:Scan"
            ],
            "Resource": [
                "arn:aws:dynamodb:*:*:table/tag_tamer_roles",
                "arn:aws:dynamodb:*:*:table/tag_tamer_tag_groups"
            ]
        },
        {
            "Sid": "VisualEditor1",
            "Effect": "Allow",
            "Action": [
                "sts:AssumeRole",
                "lambda:TagResource",
                "ec2:DescribeInstances",
                "servicecatalog:SearchProducts",
                "iam:ListRoleTags",
                "eks:ListTagsForResource",
                "rds:DescribeGlobalClusters",
                "servicecatalog:UntagResource",
                "eks:DescribeNodegroup",
                "ec2:DescribeVolumes",
                "config:DescribeConfigRules",
                "s3:PutObjectTagging",
                "iam:ListRolePolicies",
                "servicecatalog:UpdateTagOption",
                "s3:DeleteObjectTagging",
                "iam:ListPolicies",
                "eks:ListNodegroups",
                "lambda:ListFunctions",
                "config:PutConfigRule",
                "ec2:CreateTags",
                "servicecatalog:ListTagsForResource",
                "s3:GetObject",
                "eks:DescribeCluster",
                "eks:ListClusters",
                "rds:RemoveTagsFromResource",
                "config:UntagResource",
                "rds:DescribeOptionGroups",
                "servicecatalog:DeleteTagOption",
                "s3:GetBucketTagging",
                "ec2:DeleteTags",
                "iam:TagRole",
                "s3:ReplicateTags",
                "s3:ListBucket",
                "servicecatalog:ListTagOptions",
                "s3:PutBucketTagging",
                "servicecatalog:DescribeTagOption",
                "lambda:ListTags",
                "servicecatalog:DescribeProduct",
                "rds:DescribeDBInstances",
                "s3:GetObjectTagging",
                "servicecatalog:AssociateTagOptionWithResource",
                "rds:AddTagsToResource",
                "servicecatalog:CreateTagOption",
                "eks:UntagResource",
                "ec2:DescribeTags",
                "lambda:GetFunction",
                "iam:ListRoles",
                "servicecatalog:TagResource",
                "iam:TagUser",
                "config:ListTagsForResource",
                "servicecatalog:SearchProductsAsAdmin",
                "servicecatalog:DescribeProductAsAdmin",
                "s3:ListAllMyBuckets",
                "rds:ListTagsForResource",
                "config:TagResource",
                "eks:TagResource",
                "rds:DescribeDBClusterEndpoints",
                "rds:DescribeDBClusters"
            ],
            "Resource": "*"
        }
    ]
}
```

### Example IAM role trust policy

```
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::123456789012:role/DEMOTagTamerAllAdminActionsRole"
      },
      "Action": "sts:AssumeRole",
      "Condition": {}
    },
    {
      "Sid": "",
      "Effect": "Allow",
      "Principal": {
        "Federated": "cognito-identity.amazonaws.com"
      },
      "Action": "sts:AssumeRoleWithWebIdentity"
    }
  ]
}
```

