# macie-auto-scan-public
通过监听macie policy finding,从securityhub中提取finding发送至eventbridge,触发Lambda调用Macie进行敏感数据扫描
## 架构图
[architecture](/architecture.png)
## 部署方法
### Step 1 打开macie和securityhub
详见:https://github.com/jessicawyc/aws-enable-ess
### Step 2 配置Lambda
#### 配置Lambda要使用的IAM Role
下载两个文件到本地
[lambdapolicy.json](/lambdapolicy.json)
[trust-lambda.json](/trust-lambda.json)

变量设置
```
lambdapolicy='lambda-macie'
rolename='lambda-macie'
```
运行CLI命令

```
rolearn=$(aws iam create-role --role-name $rolename --assume-role-policy-document file://trust-lambda.json --query 'Role.Arn' --output text)
aws iam put-role-policy --role-name=$rolename --policy-name $lambdapolicy --policy-document file://lambdapolicy.json
```

#### Create Lambda function
变量设置
```
function='macie-scan-s3'
```
运行CLI命令
```
lambdaarn=$(aws lambda create-function \
    --function-name $function \
    --runtime python3.9 \
    --zip-file fileb://maciescan.zip \
    --handler maciescan.lambda_handler \
    --role $rolearn --region=$region --no-cli-pager --query 'FunctionArn' --output text)
```

### Step 3 配置Securityhub输出

变量设置
```
region='us-east-1'
rulename='sechub-macie-alert'
email='**@qq.com'
```
其它Steps请使用[原文中的CLI](https://github.com/jessicawyc/securityhub-alert/blob/main/README.md#2%E8%87%AA%E5%8A%A8%E5%8F%91%E9%80%81%E5%91%8A%E8%AD%A6%E6%A8%A1%E5%BC%8F)

完成Input transforner之后还要
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
并将lambda加入Target 2中,部署完成
aws events put-targets --rule $rulename  --targets "Id"="2","Arn"=$lambdaarn --region=$region
如果想要lambda rolearn查询可以使用
```
rolearn=$(aws iam get-role   --role-name $rolename --query 'Role.Arn' --output text)
```

