import copy
from .function import to_text, to_link, to_oa, to_markdown, to_action_card
from .function import MESSAGE


class Story:
    def __init__(self, metadata, api_key=None, api_secret=None, user_file=None, name_key=None):
        self.metadata = metadata
        self.message_body = copy.deepcopy(MESSAGE)
        self.api_key = api_key
        self.api_secret = api_secret
        self.user_file = user_file
        self.name_key = name_key
        self.message_content = ""
        self.message_url = ""
        self.read_type = ""
        self.at_user = []
        self.sub_event = ""

        # 基础类属性
        self.type = self.metadata["event"]["event_key"]
        self.user = self.metadata["event"]["user"]
        self.workspace_id = self.metadata["event"]["workspace_id"]
        self.story_id = self.metadata["event"]["id"]
        self.message_body_metadata = {}
        # owner代表需求的当前处理人
        # attchment\create\status_change\update
        #

        # cc 代表抄送人
        # attchment\status_change\update
        #

        # name 代表需求名称
        # attchment\create\status_change\update

    def get_type(self):
        return self.type

    # 触发每一个事件的用户
    def get_user(self):
        return self.user

    def get_workspace_id(self):
        return self.workspace_id

    def get_story_id(self):
        return self.story_id

    def get_message_body_metadata(self):
        return self.message_body_metadata

    def get_message_body(self,  dingding_style, with_metadata=False):
        if with_metadata:
            self.message_body["metadata"] = self.message_body_metadata
        if self.api_key and self.api_key:
            # todo
            # 键值转换
            pass
        elif self.user_file and self.name_key:
            # todo
            # 键值转换
            pass
        if self.sub_event == "delete":
            self.message_body["sub_event"] = "delete"
        if dingding_style == "text":
            to_text(self.message_body, type_title=self.read_type, content=self.message_content, url=self.message_url)
            return self.message_body
        if dingding_style == "link":
            to_link(self.message_body, type_title=self.read_type, content=self.message_content, url=self.message_url)
            return self.message_body
        if dingding_style == "oa":
            to_oa(self.message_body, type_title=self.read_type, content=self.message_content, url=self.message_url)
            return self.message_body
        if dingding_style == "markdown":
            to_markdown(self.message_body, type_title=self.read_type, content=self.message_content, url=self.message_url)
            return self.message_body
        if dingding_style == "action_card":
            to_action_card(self.message_body, type_title=self.read_type, content=self.message_content, url=self.message_url)
            return self.message_body


