import datetime
import uuid
from bs4 import BeautifulSoup


MESSAGE = {
    "receiver": ["消息目标接受人"],
    "metadata": {},
    "dingtalk_payload": {
        "msgtype": "text|image|markdown|link|action_card",
    }
}

RECEIVER_KYE = ["owner", "cc", "creator", "developer"]


def get_receiver(metadata):
    receiver = []
    for item in RECEIVER_KYE:
        if item in metadata["event"]:
            receiver = receiver + metadata["event"][item]
    receiver = list(set(receiver))
    if metadata["event"]["event_key"] == "story::create":
        for creator in metadata["event"]["creator"]:
            receiver.remove(creator)
    elif metadata["event"]["user"] in receiver:
        receiver.remove(metadata["event"]["user"])
    return receiver


def get_recursion_receiver(self, workspace_id, story_id):
    # todo
    # 递归获取父子需求所有的receiver
    return None


def general_url(workspace, story):
    return "dingtalk://dingtalkclient/page/link?url=https%3A%2F%2Fwww.tapd.cn%2F" + str(workspace) + \
           "%2Fprong%2Fstories%2Fview%2F" + str(story) +"&pc_slide=false&rp=" + str(uuid.uuid4())[:4]


def to_text(message_body, type_title, content, url):
    message_body["dingtalk_payload"]["msgtype"] = "text"
    message_body["dingtalk_payload"]["text"] = {"content": type_title + ": " + content + "，详情点击：" + url}
    return message_body


def to_link(message_body, type_title, content, url):
    message_body["dingtalk_payload"]["msgtype"] = "link"
    message_body["dingtalk_payload"]["link"] = {
        "messageUrl": url,
        "picUrl": "请替换为企业应用媒体文件id",
        "title": type_title,
        "text": content
    }
    return message_body


def to_oa(message_body, type_title, content, url):
    message_body["dingtalk_payload"]["msgtype"] = "oa"
    message_body["dingtalk_payload"]["oa"] = {
        "message_url": url,
        "head": {
            "bgcolor": "FFBBBBBB",
            "text": type_title
        },
        "body": {
            # "author": datetime.datetime.now().strftime("%H:%M"),
            # "author": type_title,
            # "title": type_title,
            "content": content
        },
        "status_bar": {
            "status_value": "hold住，明天就放假了",
            "status_bg": "FFBBBBBB"
        }
    }
    return message_body


def to_markdown(message_body, type_title, content, url):
    message_body["dingtalk_payload"]["msgtype"] = "markdown"
    message_body["dingtalk_payload"]["markdown"] = {
        "title": type_title,
        "text": content + "  \n  " + "[查看详情](" + url + ")"
    }
    return message_body


def to_action_card(message_body, type_title, content, url):
    message_body["dingtalk_payload"]["msgtype"] = "action_card"
    message_body["dingtalk_payload"]["action_card"] = {
        "title": type_title,
        "single_title": "查看详情",
        "single_url": url,
        "markdown": "# " + type_title + "\n" + content
    }
    return message_body


def get_at_user(comment):
    user_list = []
    if "data-userid" in comment:
        soup = BeautifulSoup(comment, 'lxml')
        tar_list = soup.find_all('b')
        for tar in tar_list:
            if tar.get('data-userid'):
                user_list.append(tar.string[1:])
    else:
        pass
    return user_list

