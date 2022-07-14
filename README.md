## 简介  
通过配置Tapd的自动化助手，将工单的变更发送至钉钉  
用于将Tapd的自动化助手的webhook回调转换为钉钉消息通知/钉钉机器人的payload  
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
- receiver: 目标接受人：提取自tapy的payload的event.owner\event.cc\event.creator，如果上述包含tapd的payload中的event.user，将会剔除。   
即向除了动作的操作人之外的与此工单相关的人发出消息  

- dingtalk_paylod: 转换后的钉钉消息payload，支持上述6种样式的转换。
面向企业应用的[消息通知](https://open.dingtalk.com/document/orgapp-server/message-types-and-data-format)编写，是否兼容钉钉机器人需要请自测。 

- sub_event: 工单变更中，包含一种特殊行为，即删除评论，此种工单变更，不建议播报给通知对象，请根据自己的需求自行判断是否使用此字段



## 效果演示
注：截图仅演示默认样式  
![image](https://user-images.githubusercontent.com/41095303/178666581-53cca58c-1572-40c6-964b-ebb579adbf41.png)
![image](https://user-images.githubusercontent.com/41095303/178666604-c57f7700-1015-4e65-aa5e-f7edf03265f1.png)
![image](https://user-images.githubusercontent.com/41095303/178666621-bd016239-b0ae-45b8-838e-9e02dcfb1707.png)
![image](https://user-images.githubusercontent.com/41095303/178666632-7d479b57-905d-401e-9402-043746e88ce6.png)
![image](https://user-images.githubusercontent.com/41095303/178666653-aaba7ce3-72e9-451e-8d95-a332ec501767.png)



## 接入demo
暂时未提交pypi，请下载最新tag至项目中 
```python
from Tapd2DingtalkPayload import metadata2payload
payload = metadata2payload(tapd_data, style=None, status_dict=None)
```
参数说明： 
- tapd_data: tapd的回调数据
- style: 指定转换后的消息样式，当前支持text|image|markdown|link|action_card，如果不指定，除了需求评论默认使用markdown之外，默认使用action_card 
- status_dict: 由于tapd回调的消息自身的限制，对于工单中自定义的状态，会被现实成“status_xxx”的样式，因此在需求状态变更的播报中，显示的的样式可读性较差，可以自行补充状态字典替换，例如
```{"status_19":"处理中"}```

1、假设你拥有一个Python Web程序，用于接收Tapd回调的消息，Tapd的回调配置请参考官方文档https://www.tapd.cn/help/show#1120003271001000703  
2、将接收到的payload存储到变量tapd_payload中  
3、为了将消息发送到钉钉，我们需要将tapd_payload语义化，并转换为钉钉工作通知的所需的payload样式。  
钉钉工作通知样式文档：https://open.dingtalk.com/document/orgapp-server/message-types-and-data-format  
钉钉群机器人样式文档：https://open.dingtalk.com/document/robots/custom-robot-access（不维护群机器人与消息通知样式的payload格式一致，需考虑钉钉官方变动）  
4、在web程序中引入本库，并获取钉钉payload和目标接收人
```python
from Tapd2DingtalkPayload import metadata2payload
dingtalk_payload = metadata2payload(tapd_data, style=None, status_dict=None)
```
例如  
```json
{
    "receiver": [
        "Jerry",
        "Tom"
    ],
    "metadata": {},
    "dingtalk_payload": {
        "msgtype": "action_card",
        "action_card": {
            "title": "需求创建",
            "single_title": "查看详情",
            "single_url": "dingtalk://dingtalkclient/page/link?url=https%3A%2F%2Fwww.tapd.cn%2Fxxxx&pc_slide=false&rp=3296",
            "markdown": "# Miki需求创建了需求\n【今天加个鸡腿】"
        }
    }
}
```
如果你只是希望将消息发送到固定的群机器人中，只需要将dingtalk_payload字段内的内容传递给dingding的api即可。  
除非你希望通过receiver获取目标发送的群机器人或者工作通知对应的用户，你才需要使用receiver字段，receiver的内容与目标群机器人或者工作通知的用户ID的映射关系，请在自己的web应用中维护



