## 简介  
通过配置Tapd的自动话助手，将工单的变更发送至钉钉  
用于将Tapd的自动化助手的webhook回调转换为钉钉消息通知的payload  
当前版本v0.0.1已支持：需求创建、需求状态变更、需求内容更新、

## 转换后的数据样式  
```json
{
  "receiver": ["消息目标接受人"],
  "dingtalk_payload": {
    "msgtype": "text|image|markdown|link|action_card",
    "otherKey": "otherValue"
  },
  "sub_event": "|delete"
}
```
字段解释：  
- 含目标接受人：提取自tapy的payload的event.owner\event.cc\eventcreator，如果上述包含tapd的payload中的event.user，将会剔除。   
即向除了动作的操作人之外的与此工单相关的人发出消息  

- dingtalk_paylod: 转换后的钉钉消息payload，支持上述6种样式的转换。
面向企业应用的[消息通知](https://open.dingtalk.com/document/orgapp-server/message-types-and-data-format)编写，是否兼容钉钉机器人需要请自测。 

- sub_event: 工单变更中，包含一种特殊行为，即删除评论，此种工单变更，不建议播报给通知对象，请根据自己的需求自行判断是否使用此字段

## 使用
暂时未提交pypi，请clone  
```python
from Tapd2DingtalkPayload import metadata2payload
payload = metadata2payload(tapd_data, style=None, status_dict=None)
```
参数说明： 
- tapd_data: tapd的回调数据
- style: 指定转换后的消息样式，当前支持text|image|markdown|link|action_card，如果不指定，除了需求评论默认使用markdown之外，默认使用action_card 
- status_dict: 由于tapd回调的消息自身的限制，对于工单中自定义的状态，会被现实成“status_xxx”的样式，因此在需求状态变更的播报中，显示的的样式可读性较差，可以自行补充状态字典替换，例如
```{"status_19":"处理中"}```

## demo
注：截图仅演示默认样式  







