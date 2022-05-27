from ..story_data import Story
from ..function import general_url, get_receiver


class StoryUpdate(Story):
    def __init__(self, metadata, api_key=None, api_secret=None, user_file=None, name_key=None):
        super().__init__(metadata, api_key, api_secret, user_file, name_key)
        self.creator = self.metadata["event"]["creator"]
        self.owner = self.metadata["event"]["owner"]
        self.name = self.metadata["event"]["name"]
        self.cc = self.metadata["event"]["cc"]
        self.read_type = "需求更新"

        self.message_body["receiver"] = get_receiver(self.metadata)
        self.message_url = general_url(self.workspace_id, self.story_id)
        self.message_content = self.user + "更新了需求  \n【" + self.name + "】  \n的内容，请点击详情查看变更历史选项卡"
        self.message_body_metadata = {
            "type": self.type,
            "user": self.user,
            "workspace_id": self.workspace_id,
            "story_id": self.story_id,
            "creator": self.creator,
            "owner": self.owner,
            "cc": self.cc,
            "name": self.name
        }

    def get_creator(self):
        return self.creator

    def get_owner(self):
        return self.owner

    def get_name(self):
        return self.name

    def get_cc(self):
        return self.cc

