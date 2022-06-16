# macie-auto-scan-public
通过监听macie policy finding,从securityhub中提取finding发送至eventbridge,触发Lambda调用Macie进行敏感数据扫描
## 架构图
TBD
## 部署方法
Step 1 打开macie和securityhub
详见:https://github.com/jessicawyc/aws-enable-ess
Step 2 配置Securityhub输出

## 参数设置
```
region='聚合后的region名:us-east-1'
rulename='maciealerts3'
email='**@qq.com'
```
## CLI 命令复制粘贴,
```
snsarn=$(aws sns create-topic   --name  $rulename  --region=$region  --output text --query 'TopicArn')
aws sns subscribe --topic-arn $snsarn --protocol email --notification-endpoint  $email --region=$region
aws events put-rule \
--name $rulename \
--event-pattern \
"{\"source\": [\"aws.securityhub\"],\"detail-type\": [\"Security Hub Findings - Imported\"],\"detail\": {\"findings\":{\"RecordState\": [\"ACTIVE\"],\"Severity\": {\"Label\": [\"HIGH\", \"CRITICAL\"]},\"Workflow\": {\"Status\": [\"NEW\"]}}}}" --region=$region

aws events put-targets --rule $rulename  --targets "Id"="1","Arn"=$snsarn --region=$region
```
[打开新建好的rule,进行配置详见](https://github.com/jessicawyc/securityhub-alert/blob/main/README.md#%E6%89%93%E5%BC%80eventbridge-rule%E5%A4%8D%E5%88%B6%E4%BB%A5%E4%B8%8B%E5%86%85%E5%AE%B9%E8%87%B3target-input-transformer-config-input-transformer)


Step 3 配置Lambda
