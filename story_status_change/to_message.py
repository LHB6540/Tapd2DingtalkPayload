import copy

from ..story_data import Story
from ..function import general_url, get_receiver


class StoryStatusChange(Story):
    def __init__(self, metadata, api_key=None, api_secret=None, user_file=None, name_key=None, status_dict={}):
        super().__init__(metadata, api_key, api_secret, user_file, name_key)
        self.creator = self.metadata["event"]["creator"]
        self.owner = self.metadata["event"]["owner"]
        self.name = self.metadata["event"]["name"]
        self.cc = self.metadata["event"]["cc"]
        self.status = self.metadata["event"]["status"]
        if status_dict and self.status in status_dict.keys():
            tmp_status = copy.deepcopy(self.status)
            self.status = status_dict[tmp_status]
        self.read_type = "需求状态变更"
        # todo
        # 改成语法糖
        self.message_body["receiver"] = get_receiver(self.metadata)
        self.message_url = general_url(self.workspace_id, self.story_id)
        self.message_content = self.user + "更新了需求:【" + self.name + "】的状态为" + self.status
        self.message_body_metadata = {
            "type": self.type,
            "user": self.user,
            "workspace_id": self.workspace_id,
            "story_id": self.story_id,
            "creator": self.creator,
            "owner": self.owner,
            "cc": self.cc,
            "name": self.name,
            "status": self.status
        }

    def get_creator(self):
        return self.creator

    def get_owner(self):
        return self.owner

    def get_cc(self):
        return self.cc

    def get_name(self):
        return self.name

    def get_status(self):
        return self.status


