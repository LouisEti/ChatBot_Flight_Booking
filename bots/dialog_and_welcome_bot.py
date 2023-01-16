# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
"""Main dialog to welcome users."""
import json

from typing import List
from botbuilder.dialogs import Dialog
from botbuilder.core import (
    TurnContext,
    ConversationState,
    UserState,
    BotTelemetryClient)
from botbuilder.schema import Activity, Attachment, ChannelAccount
from helpers.activity_helper import create_activity_reply
from .dialog_bot import DialogBot


class DialogAndWelcomeBot(DialogBot):
    """Main dialog to welcome users."""

    # ==== Initialization ==== #
    def __init__(
        self,
        conversation_state: ConversationState,
        user_state: UserState,
        dialog: Dialog,
        telemetry_client: BotTelemetryClient):

        super(DialogAndWelcomeBot, self).__init__(
            conversation_state, user_state, dialog, telemetry_client)
        self.telemetry_client = telemetry_client

    
    # ==== On Member Added Activity ==== #
    async def on_members_added_activity(self, members_added: List[ChannelAccount], turn_context: TurnContext):
        for member in members_added:
            # Greet anyone that was not the target (recipient) of this message.
            # To learn more about Adaptive Cards, see https://aka.ms/msbot-adaptivecards
            # for more details.
            if member.id != turn_context.activity.recipient.id:
                # welcome_card = self.create_adaptive_card_attachment()
                # response = self.create_response(turn_context.activity, welcome_card)
                # await turn_context.send_activity(response)
                await turn_context.send_activity('Hello')

    
    # ==== Response ==== #
    def create_response(self, activity: Activity, attachment: Attachment):
        """Create an attachment message response."""
        
        response = create_activity_reply(activity)
        response.attachments = [attachment]
        return response

    
    # ==== Adaptative Card ==== #
    def create_adaptive_card_attachment(self):
        """Create an adaptive card."""
        
        # Load attachment from file
        path = "cards/welcomeCard.json"
        with open(path) as card_file:
            card = json.load(card_file)

        return Attachment(
            content_type="application/vnd.microsoft.card.adaptive", content=card)