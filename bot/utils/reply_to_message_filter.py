
from typing import Dict, Optional, Union
from telegram import Update
from telegram.ext import BaseFilter, UpdateFilter


class ReplyToMessageFilter(UpdateFilter):
    """
    Applies filters to ``update.effective_message.reply_to_message``.
    Args:
        filters (:class:`telegram.ext.BaseFilter`): The filters to apply. Pass exactly like passing
            filters to :class:`telegram.ext.MessageHandler`.
    Attributes:
        filters (:class:`telegram.ext.BaseFilter`): The filters to apply.
    """

    def __init__(self, filters: BaseFilter):
        self.filters = filters
        self.data_filter = self.filters.data_filter

    def filter(self, update: Update) -> Optional[Union[bool, Dict]]:
        if not update.effective_message.reply_to_message:
            return False

        reply_to_message = update.effective_message.reply_to_message
        if update.channel_post:
            return self.filters(Update(1, channel_post=reply_to_message))
        if update.edited_channel_post:
            return self.filters(Update(1, edited_channel_post=reply_to_message))
        if update.message:
            return self.filters(Update(1, message=reply_to_message))
        if update.edited_message:
            return self.filters(Update(1, edited_message=reply_to_message))
        return False
