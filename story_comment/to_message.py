import re

from ..story_data import Story
from ..function import general_url, get_receiver, get_at_user
import html2text


class StoryComment(Story):
    def __init__(self, metadata, api_key=None, api_secret=None, user_file=None, name_key=None):
        super().__init__(metadata, api_key, api_secret, user_file, name_key)
        # self.creator = self.metadata["event"]["creator"]
        # self.owner = self.metadata["event"]["owner"]
        # self.cc = self.metadata["event"]["cc"]
        # self.name = self.metadata["event"]["name"]
        # todo 获取@的人员，额外补充一个字段，标识@对象
        self.at_user = get_at_user(self.metadata["event"]["description:fromto"]["to"])
        self.sub_event = self.metadata["event"]["sub_event"]
        self.description = html2text.html2text(self.metadata["event"]["description:fromto"]["to"])
        self.description = re.sub(r'/tfl', "https://file.tapd.cn/tfl", self.description)
        self.read_type = "需求评论"
        # todo
        # 从历史消息中获取需求id对应的name，应该放置在另一个模块中
        self.message_body["receiver"] = get_receiver(self.metadata)
        self.message_body["receiver"] = self.message_body["receiver"] + self.at_user
        self.message_url = general_url(self.workspace_id, self.story_id)
        self.message_content = self.user + "评论了需求  " + ": \n\n---\n\n " + self.description
        if self.sub_event == "delete":
            self.message_content = self.user + "删除了评论 " + ": \n\n---\n\n " + self.description
        if "![]" in self.message_content:
            self.message_content = self.message_content + " \n (图片评论暂时无法正常显示，请点击详情查看)"

        self.message_body_metadata = {
            "type": self.type,
            "user": self.user,
            "at_user": self.at_user,
            "workspace_id": self.workspace_id,
            "story_id": self.story_id,
            "description": self.description
        }

    def get_at_user(self):
        return self.at_user

    def get_description(self):
        return self.description
