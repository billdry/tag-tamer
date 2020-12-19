# Tag Tamer IAM permission policies & roles

## Tag Tamer web app instance profile

### IAM Permission policy

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "cognito-identity:GetId",
                "cognito-identity:GetCredentialsForIdentity"
            ],
            "Resource": "*"
        },
        {
            "Sid": "VisualEditor1",
            "Effect": "Allow",
            "Action": [
                "ssm:GetParametersByPath",
                "cognito-idp:AdminListGroupsForUser"
            ],
            "Resource": [
                "arn:aws:ssm:*:*:parameter/*",
                "arn:aws:cognito-idp:us-east-1:*:userpool/<YOUR_USER_POOL_ID>"
            ]
        }
    ]
}
```
### IAM Role

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