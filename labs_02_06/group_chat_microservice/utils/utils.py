from schemas import GroupChatSchema


async def convert_group_model_to_dict(group: GroupChatSchema):
    group.members = [member.model_dump() for member in group.members]
    group.messages = [message.model_dump() for message in group.messages]

    return group
