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
## 其它标准Step请使用
https://github.com/jessicawyc/securityhub-alert/blob/main/README.md#%E8%87%AA%E5%8A%A8%E5%8F%91%E9%80%81%E5%91%8A%E8%AD%A6%E6%A8%A1%E5%BC%8F

## 修改Eventbridge中的event pattern
```

```

Step 3 配置Lambda
