from ..story_data import Story
from ..function import general_url, get_receiver, to_text


class StoryCreate(Story):
    def __init__(self, metadata, api_key=None, api_secret=None, user_file=None, name_key=None):
        super().__init__(metadata, api_key, api_secret, user_file, name_key)
        self.creator = self.metadata["event"]["creator"]

        self.owner = []
        if "owner" in self.metadata.keys():
            self.owner = self.metadata["event"]["owner"]
        self.name = self.metadata["event"]["name"]
        self.read_type = "需求创建"

        # todo
        # 改成语法糖
        self.message_body["receiver"] = get_receiver(self.metadata)
        self.message_url = general_url(self.workspace_id, self.story_id)
        self.creator_name = ""
        if isinstance(self.creator, str):
            tmp = self.creator.split(";")
            for name in tmp:
                self.creator_name = self.creator_name + name + ","
        elif isinstance(self.creator, list):
            for name in self.creator:
                self.creator_name = self.creator_name + name + ","

        if self.creator_name:
            self.creator_name = self.creator_name[:-1]
        self.message_content = self.creator_name + "创建了需求【" + self.name + "】"
        self.message_body_metadata = {
            "type": self.type,
            "user": self.user,
            "workspace_id": self.workspace_id,
            "story_id": self.story_id,
            "creator": self.creator,
            "owner": self.owner,
            "name": self.name
        }

    def get_creator(self):
        return self.creator

    def get_owner(self):
        return self.owner

    def get_name(self):
        return self.name








