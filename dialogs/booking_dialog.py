# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
"""Flight booking dialog."""

from datatypes_date_time.timex import Timex
import csv

from botbuilder.dialogs import WaterfallDialog, WaterfallStepContext, DialogTurnResult
from botbuilder.dialogs.prompts import ConfirmPrompt, TextPrompt, PromptOptions
from botbuilder.schema import InputHints
from botbuilder.core import MessageFactory, BotTelemetryClient, NullTelemetryClient
from .cancel_and_help_dialog import CancelAndHelpDialog
from .start_date_resolver_dialog import StartDateResolverDialog
from .end_date_resolver_dialog import EndDateResolverDialog
import sys
import os
import glob



class BookingDialog(CancelAndHelpDialog):
    """Flight booking implementation."""

    # ==== Initialization === #
    def __init__(
        self,
        unvalidated_dialogs,
        dialog_id: str = None,
        telemetry_client: BotTelemetryClient = NullTelemetryClient(),
        
        ):

        super(BookingDialog, self).__init__(
            dialog_id or BookingDialog.__name__, telemetry_client)
        self.telemetry_client = telemetry_client

        text_prompt = TextPrompt(TextPrompt.__name__)
        text_prompt.telemetry_client = telemetry_client
        self.add_dialog(text_prompt)

        # Correct Waterfall Dialog with the 5 requested entities
        waterfall_dialog = WaterfallDialog(
            WaterfallDialog.__name__,
            [
                self.origin_step,
                self.destination_step,
                self.start_date_step,
                self.end_date_step,
                self.budget_step,
                self.confirm_step,
                self.note_step,
                self.final_step,
            ])
        waterfall_dialog.telemetry_client = telemetry_client
        self.add_dialog(waterfall_dialog)
        
        self.initial_dialog_id = WaterfallDialog.__name__
        self.add_dialog(ConfirmPrompt(ConfirmPrompt.__name__))
        self.add_dialog(StartDateResolverDialog(StartDateResolverDialog.__name__, self.telemetry_client))
        self.add_dialog(EndDateResolverDialog(EndDateResolverDialog.__name__, self.telemetry_client))  

        self.dialogs = []
        self.unvalidated_dialogs = unvalidated_dialogs
        self.confirm = True #bool

    
    # ==== Origine ==== # 
    async def origin_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        """Prompt for origin city."""

        booking_details = step_context.options
        
        dir = sys.path[0]
        print(dir, "dir")
        
        for fn in glob.glob(os.path.join(dir, "*.csv")):
            with open(fn, "a") as f:
                writer = f.writelines("\n test")
                f.close()

        #Initialize dialog
        msg = "What do you want me to do ?"
        self.unvalidated_dialogs.append({"Bot": msg})

        if booking_details.origin is None:
            msg = "From which city would you be leaving from?"
            prompt_message = MessageFactory.text(msg, msg, InputHints.expecting_input)

            #Update unvalidated_dialogs
            self.unvalidated_dialogs.append({"User": step_context.context.activity.text})
            self.unvalidated_dialogs.append({"Bot": msg})

            return await step_context.prompt(TextPrompt.__name__, PromptOptions(prompt=prompt_message)) # pylint: disable=line-too-long,bad-continuation
        
        #Update unvalidated_dialogs
        self.unvalidated_dialogs.append({"User": step_context.context.activity.text})
        print(self.unvalidated_dialogs, "Origin")

        return await step_context.next(booking_details.origin)
        
    
    # ==== Destination ==== # 
    async def destination_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        """Prompt for destination city."""
        
        booking_details = step_context.options

        # Capture the response to the previous step's prompt
        booking_details.origin = step_context.result

        if booking_details.destination is None:
            msg = "Where would you like to go?"
            prompt_message = MessageFactory.text(msg, msg, InputHints.expecting_input)

            #Update unvalidated_dialogs
            self.unvalidated_dialogs.append({"User": step_context.context.activity.text})
            if self.unvalidated_dialogs[-1] == self.unvalidated_dialogs[-2]:
                self.unvalidated_dialogs.pop()
            self.unvalidated_dialogs.append({"Bot": msg})

            return await step_context.prompt(TextPrompt.__name__, PromptOptions(prompt=prompt_message))  # pylint: disable=line-too-long,bad-continuation

        return await step_context.next(booking_details.destination)

    
    # ==== Start Date ==== # 
    async def start_date_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        """Prompt for departure date.
        This will use the DATE_RESOLVER_DIALOG."""

        booking_details = step_context.options

        # Capture the response to the previous step's prompt
        booking_details.destination = step_context.result

        if not booking_details.start_date or self.is_ambiguous(booking_details.start_date):

            #Update unvalidated_dialogs
            self.unvalidated_dialogs.append({"User": step_context.context.activity.text})
            msg = "Could you give me a date of departure?"
            self.unvalidated_dialogs.append({"Bot": msg})

            return await step_context.begin_dialog(StartDateResolverDialog.__name__, booking_details.start_date)  # pylint: disable=line-too-long

        return await step_context.next(booking_details.start_date)


    # ==== End Date ==== # 
    async def end_date_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        """Prompt for departure date.
        This will use the DATE_RESOLVER_DIALOG."""

        booking_details = step_context.options

        # Capture the response to the previous step's prompt
        booking_details.start_date = step_context.result

        if not booking_details.end_date or self.is_ambiguous(booking_details.end_date):

            #Update unvalidated_dialogs
            self.unvalidated_dialogs.append({"User": step_context.context.activity.text})
            msg = "And when would you like to return?"
            self.unvalidated_dialogs.append({"Bot": msg})

            return await step_context.begin_dialog(EndDateResolverDialog.__name__, booking_details.end_date)  # pylint: disable=line-too-long

        return await step_context.next(booking_details.end_date)
    

    # ==== Budget ==== # 
    async def budget_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        """Prompt for budget."""
        
        booking_details = step_context.options

        # Capture the response to the previous step's prompt
        booking_details.end_date = step_context.result

        if booking_details.budget is None:
            msg = "Great! Do you have a budget in mind?"
            prompt_message = MessageFactory.text(msg, msg, InputHints.expecting_input)   

            #Update unvalidated_dialogs
            self.unvalidated_dialogs.append({"User": step_context.context.activity.text})
            self.unvalidated_dialogs.append({"Bot": msg})

            return await step_context.prompt(TextPrompt.__name__, PromptOptions(prompt=prompt_message))  # pylint: disable=line-too-long,bad-continuation

        return await step_context.next(booking_details.budget)


    # ==== Confirm ==== # 
    async def confirm_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        """Confirm the information the user has provided."""
        
        booking_details = step_context.options

        # Capture the results of the previous step's prompt
        booking_details.budget = step_context.result
        
        # Offer a YES/NO prompt.
        msg = (
            f"Please confirm that you would like to book a flight from { booking_details.origin } "
            f"to { booking_details.destination }, "
            f"starting on { booking_details.start_date} and ending on {booking_details.end_date}, "
            f"for a budget of {booking_details.budget}.")


        #Update unvalidated_dialogs
        self.unvalidated_dialogs.append({"User": step_context.context.activity.text})
        self.unvalidated_dialogs.append({"Bot": msg})
        
        prompt_message = MessageFactory.text(msg, msg, InputHints.expecting_input)
        return await step_context.prompt(ConfirmPrompt.__name__, PromptOptions(prompt=prompt_message))

    # === Note === #
    async def note_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        """Rate the bot service"""

        booking_details = step_context.options

        if step_context.result:
            self.confirm = False

            #Update unvalidated_dialogs
            self.unvalidated_dialogs.append({"User": "Yes"})
            print(self.unvalidated_dialogs, "Yes")
        
        else:
            self.confirm = True

            #Update unvalidated_dialogs
            self.unvalidated_dialogs.append({"User": "No"})
            print(self.unvalidated_dialogs, "No")
        
        if booking_details.note is None:
            rate_message = "Rate the bot service between 1 and 5"

            #Update unvalidated_dialogs
            self.unvalidated_dialogs.append({"Bot": rate_message})
            print(self.unvalidated_dialogs, "No note")

            prompt_rate_message = MessageFactory.text(rate_message, rate_message, InputHints.expecting_input)
            return await step_context.prompt(TextPrompt.__name__, PromptOptions(prompt=prompt_rate_message))

        return await step_context.next(booking_details.note)

    
    # ==== Final ==== #
    async def final_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        """Complete the interaction, track data, and end the dialog."""

        # Create data to track in App Insights
        booking_details = step_context.options
        booking_details.note = step_context.result

        properties = {}
        properties["origin"] = booking_details.origin
        properties["destination"] = booking_details.destination
        properties["departure_date"] = booking_details.start_date
        properties["return_date"] = booking_details.end_date
        properties["budget"] = booking_details.budget
        properties["note"] = booking_details.note


        #Send Trace with telemetry if note given is 1 or 2
        if int(booking_details.note) < 3:
            self.telemetry_client.track_trace("Note 1 or 2", properties, "WARNING")
            self.telemetry_client.flush()
        
#         elif type(booking_details.note) != int:
#             self.telemetry_client.track_trace("Bug", properties, "WARNING")

        
        # If the BOT is successful
        if self.confirm:
            
            #Add unvalidated_dialogs to CSV file
            with open("./unvalidated_dialogs2.csv", "a") as f:
                writer = csv.writer(f)
                writer.writerow(self.unvalidated_dialogs)
                f.close()
            
            #Re-initialize unvalidated_dialogs as empty list for next conversation 
            self.unvalidated_dialogs = []
            self.unvalidated_dialogs.append({"Bot": "What do you want me to do ?"})

            # Track YES data
            self.telemetry_client.track_trace("YES answer", properties, "INFO")
            self.telemetry_client.flush()
            
        # If the BOT is NOT successful
        else:
            # Send a "sorry" message to the user
            sorry_msg = "I'm sorry I couldn't help you"
            
            whole_dialog = MessageFactory.text(self.unvalidated_dialogs, self.unvalidated_dialogs, InputHints.ignoring_input)
            await step_context.context.send_activity(whole_dialog)

            #Update unvalidated_dialogs
            self.unvalidated_dialogs.append({"User": step_context.context.activity.text})
            self.unvalidated_dialogs.append({"Bot": sorry_msg})
            print(self.unvalidated_dialogs, "No No")

            #Add unvalidated_dialogs to CSV file
            with open("./unvalidated_dialogs2.csv", "a") as f:
                writer = csv.writer(f)
                writer.writerow(self.unvalidated_dialogs)
                f.close()

            #Re-initialize unvalidated_dialogs as empty list for next conversation 
            self.unvalidated_dialogs = []
            self.unvalidated_dialogs.append({"Bot": "What do you want me to do ?"})

            prompt_sorry_msg = MessageFactory.text(sorry_msg, sorry_msg, InputHints.expecting_input)
            await step_context.context.send_activity(prompt_sorry_msg)

            # Track NO data
            self.telemetry_client.track_trace("NO answer", properties, severity="WARNING")
            self.telemetry_client.flush()

        return await step_context.end_dialog()

    # # ==== Final2 ==== #
    # async def final_step2(self, step_context: WaterfallStepContext) -> DialogTurnResult:

    
    # ==== Ambiguous date ==== #
    def is_ambiguous(self, timex: str) -> bool:
        """Ensure time is correct."""
        
        timex_property = Timex(timex)
        return "definite" not in timex_property.types
