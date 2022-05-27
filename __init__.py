from .story_data import Story
from .story_create import StoryCreate
from .story_status_change import StoryStatusChange
from .story_comment import StoryComment
from .story_attachment import StoryAttachment
from .story_update import StoryUpdate
from function.logs_record import log2file


def metadata2payload(metadata, style=None, status_dict=None):
    default_style = "action_card"
    story = {}
    if metadata["event"]["event_key"] == "story::create":
        story = StoryCreate(metadata)

    if metadata["event"]["event_key"] == "story::status_change":
        story = StoryStatusChange(metadata, status_dict=status_dict)

    if metadata["event"]["event_key"] == "story::comment":
        default_style = "action_card"
        story = StoryComment(metadata)

    if metadata["event"]["event_key"] == "story::attachment":
        story = StoryAttachment(metadata)

    if metadata["event"]["event_key"] == "story::update":
        story = StoryUpdate(metadata)

    if not story:
        log2file("tapd2payload.log", "消息转换失败：初始化阶段" + str(metadata), "ERROR")
        return None

    if not style:
        style = default_style

    payload = story.get_message_body(style)

    if not payload:
        log2file("tapd2payload.log", "消息转换失败：生成消息阶段" + str(metadata), "ERROR")
        return payload

    return payload

