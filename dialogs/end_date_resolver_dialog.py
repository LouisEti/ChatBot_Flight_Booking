# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
"""Handle date/time resolution for booking dialog."""

from datatypes_date_time.timex import Timex

from botbuilder.core import MessageFactory, BotTelemetryClient, NullTelemetryClient
from botbuilder.dialogs import WaterfallDialog, DialogTurnResult, WaterfallStepContext
from botbuilder.dialogs.prompts import (
    DateTimePrompt,
    PromptValidatorContext,
    PromptOptions,
    DateTimeResolution)
from botbuilder.schema import InputHints
from .cancel_and_help_dialog import CancelAndHelpDialog


class EndDateResolverDialog(CancelAndHelpDialog):
    """Resolve the date"""

    # ==== Initialization ==== #
    def __init__(
        self,
        dialog_id: str = None,
        telemetry_client: BotTelemetryClient = NullTelemetryClient()):
        
        super(EndDateResolverDialog, self).__init__(dialog_id or EndDateResolverDialog.__name__, telemetry_client)
        self.telemetry_client = telemetry_client

        date_time_prompt = DateTimePrompt(DateTimePrompt.__name__, EndDateResolverDialog.datetime_prompt_validator)
        date_time_prompt.telemetry_client = telemetry_client
        self.add_dialog(date_time_prompt)

        waterfall_dialog = WaterfallDialog(WaterfallDialog.__name__ + "2", [self.initial_step, self.final_step])
        waterfall_dialog.telemetry_client = telemetry_client       
        self.add_dialog(waterfall_dialog)
        self.initial_dialog_id = WaterfallDialog.__name__ + "2"

    
    # ==== Initial step ==== #
    async def initial_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        """Prompt for the end date."""
        
        timex = step_context.options

        msg = "And when would you like to return?"
        prompt_msg = MessageFactory.text(msg, msg, InputHints.expecting_input)
        
        msg_text = (
            "I'm sorry, for best results, please enter your travel "
            "date including the day, month and year, e.g. 10 January 2022")
        reprompt_msg = MessageFactory.text(msg_text, msg_text, InputHints.expecting_input)

        # Scenario 1: No given date -> Prompt to user
        if timex is None:
            return await step_context.prompt(
                DateTimePrompt.__name__,
                PromptOptions(prompt=prompt_msg, retry_prompt=reprompt_msg))

        # Scenario 2: We have a date -> Check if it is ambiguous
        if "definite" in Timex(timex).types:
            # This is essentially a "reprompt" of the data we were given up front.
            return await step_context.prompt(DateTimePrompt.__name__, PromptOptions(prompt=reprompt_msg))

        return await step_context.next(DateTimeResolution(timex=timex))

    
    # ==== Final Step ==== #
    async def final_step(self, step_context: WaterfallStepContext):
        """Cleanup - set final return value and end dialog."""
        
        if type(step_context.result)==list:
        
            timex = step_context.result[0].timex
        else:
            timex = step_context.result.timex
        return await step_context.end_dialog(timex)

    
    
    @staticmethod
    async def datetime_prompt_validator(prompt_context: PromptValidatorContext) -> bool:
        """ Validate the date provided is in proper form. """
        
        if prompt_context.recognized.succeeded:
            timex = prompt_context.recognized.value[0].timex.split("T")[0]

            # TODO: Needs TimexProperty
            return "definite" in Timex(timex).types

        return False
