# macie-auto-scan-public
通过监听macie policy finding,从securityhub中提取finding发送至eventbridge,触发Lambda调用Macie进行敏感数据扫描
## 架构图
TBD
## 部署方法
### Step 1 打开macie和securityhub
详见:https://github.com/jessicawyc/aws-enable-ess
### Step 2 配置Securityhub输出

参数设置
```
region='聚合后的region名:us-east-1'
rulename='maciealerts3'
email='**@qq.com'
```
其它Steps请使用[原文]中的CLI(https://github.com/jessicawyc/securityhub-alert/blob/main/README.md#2%E8%87%AA%E5%8A%A8%E5%8F%91%E9%80%81%E5%91%8A%E8%AD%A6%E6%A8%A1%E5%BC%8F)


修改Eventbridge中的event pattern替换成下方的内容
```
{
  "source": ["aws.securityhub"],
  "detail-type": ["Security Hub Findings - Imported"],
  "detail": {
    "findings": {
      "RecordState": ["ACTIVE"],
      "ProductName": ["Macie"],
      "Title": ["Block Public Access settings are disabled for the S3 bucket"],
      "Severity": {
        "Label": ["HIGH"]
      },
      "Workflow": {
        "Status": ["NEW"]
      }
    }
  }
}
```

### Step 3 配置Lambda
配置Lambda要使用的IAM Role
请下载[lambdapolicy.json](/lambdapolicy.json)
下载[trust-lambda.json](/trust-lambda.json)

```
lambdapolicy='lambda-auto-s3'
rolename='lambda-auto-s3'
rolearn=$(aws iam create-role --role-name $rolename --assume-role-policy-document file://trust-lambda.json --query 'Role.Arn' --output text)
aws iam put-role-policy --role-name=$rolename --policy-name $lambdapolicy --policy-document file://lambdapolicy.json
```

## Create Lambda
```
function='auto-s3-public'
lambdaarn=$(aws lambda create-function \
    --function-name $function \
    --runtime python3.9 \
    --zip-file fileb://FSBP-S3public-lambda.zip \
    --handler FSBP-S3public-lambda.lambda_handler \
    --role $rolearn --region=$region --no-cli-pager --query 'FunctionArn' --output text)
```
