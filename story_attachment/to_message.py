from ..story_data import Story
from ..function import general_url, get_receiver, to_text


class StoryAttachment(Story):
    def __init__(self, metadata, api_key=None, api_secret=None, user_file=None, name_key=None):
        super().__init__(metadata, api_key, api_secret, user_file, name_key)
        self.creator = self.metadata["event"]["creator"]
        self.owner = self.metadata["event"]["owner"]
        self.name = self.metadata["event"]["name"]
        self.attachment_file_name = self.metadata["event"]["filename"]
        self.cc = self.metadata["event"]["cc"]
        self.read_type = "需求附件变更"

        # todo
        # 改成语法糖
        self.message_body["receiver"] = get_receiver(self.metadata)
        self.message_url = general_url(self.workspace_id, self.story_id)
        self.message_content = self.user + "变更了需求【" + self.name + "】的附件" + self.attachment_file_name
        self.message_body_metadata = {
            "type": self.type,
            "user": self.user,
            "workspace_id": self.workspace_id,
            "story_id": self.story_id,
            "creator": self.creator,
            "owner": self.owner,
            "name": self.name,
            "cc": self.cc,
            "attachment_file_name": self.attachment_file_name
        }

    def get_creator(self):
        return self.creator

    def get_owner(self):
        return self.owner

    def get_name(self):
        return self.name

    def get_cc(self):
        return self.cc

    def get_attachment_file_name(self):
        return self.attachment_file_name


