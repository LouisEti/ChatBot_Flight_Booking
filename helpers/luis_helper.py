# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
from enum import Enum
from typing import Dict
from datatypes_date_time.timex import Timex
from botbuilder.ai.luis import LuisRecognizer
from botbuilder.core import IntentScore, TopIntent, TurnContext

from booking_details import BookingDetails


class Intent(Enum):
    BOOK_FLIGHT = "BookFlight"
    NONE_INTENT = "None"


def top_intent(intents: Dict[Intent, dict]) -> TopIntent:
    max_intent = Intent.NONE_INTENT
    max_value = 0.0

    for intent, value in intents:
        intent_score = IntentScore(value)
        if intent_score.score > max_value:
            max_intent, max_value = intent, intent_score.score

    return TopIntent(max_intent, max_value)


class LuisHelper:
    @staticmethod
    async def execute_luis_query(luis_recognizer: LuisRecognizer, turn_context: TurnContext, unvalidated_dialogs) -> (Intent, object):
        """
        Returns an object with preformatted LUIS results for the bot's dialogs to consume.
        """
        result = None
        intent = None

        try:
            recognizer_result = await luis_recognizer.recognize(turn_context)

            intent = (
                sorted(recognizer_result.intents, key=recognizer_result.intents.get, reverse=True)[:1][0]

                if recognizer_result.intents
                else None)

            if intent == Intent.BOOK_FLIGHT.value:
                result = BookingDetails()

                # We need to get the result from the LUIS JSON which at every level returns an array.
                # ==== Origin ==== #
                or_entities = recognizer_result.entities.get("$instance", {}).get("or_city", [])
                if len(or_entities) > 0:
                    result.origin = or_entities[0]["text"].capitalize()
                
                # ==== Destination ==== #
                dst_entities = recognizer_result.entities.get("$instance", {}).get("dst_city", [])
                if len(dst_entities) > 0:
                    result.destination = dst_entities[0]["text"].capitalize()
                

                # ==== Dates 1==== # 

                datetime_start = None
                datetime_end = None
                str_date_entities = recognizer_result.entities.get("$instance", {}).get("str_date", [])
                end_date_entities = recognizer_result.entities.get("$instance", {}).get("end_date", [])
                date_entities = recognizer_result.entities.get("datetime", {})
                if date_entities:
                    if len(date_entities) > 0 and (len(str_date_entities)==0 or len(end_date_entities)== 0)  :
                        timex = date_entities[0]["timex"]
                        
                        # If LUIS detects a date range format
                        if date_entities[0]["type"] == "daterange":
                            datetime_value = timex[0].replace("(", "").replace(")", "").split(",")
                            datetime_start = datetime_value[0]
                            datetime_end = datetime_value[1]
                        
                        # If LUIS detects date format
                        elif date_entities[0]["type"] == "date":
                            datetime_start = timex[0]
                            if len(date_entities) > 1:
                                timex = date_entities[1]["timex"]
                                datetime_end = timex[0]

                        result.start_date = datetime_start
                        result.end_date = datetime_end

                    elif len(str_date_entities)>0 and len(end_date_entities)>0:
                        date = str_date_entities[0]["text"]
                        # datetime_value = date.replace("(", "").replace(")", "").split(",")
                        # print(result.start_date)
                        # result.start_date = datetime_value[0]
                        result.start_date = date
                        end_date = end_date_entities[0]["text"]
                        # end_datetime_value = end_date.replace("(", "").replace(")", "").split(",")
                        # print(result.end_date)
                        # result.end_date = end_datetime_value[0]
                        result.end_date = end_date

                    else:
                        result.start_date = datetime_start
                        result.end_date = datetime_end
                

                # ==== Dates 3==== #
                # datetime_start = None
                # datetime_end = None

                # date_entities = recognizer_result.entities.get("datetime", {})

                # def time_index(i):
                #     timex = date_entities[i]["timex"]
                #     return timex

                

                # if len(date_entities) > 0 :
                #     if date_entities[0]["type"] == "date":                    
                #         timex = time_index(0)
                #         result.start_date = timex[0]
                #         if len(date_entities) > 1:
                #             timex = time_index(1)
                #             result.end_date = timex[0]
                #         else :
                #             result.end_date = None
                    
                #     elif date_entities[0]["type"] == "daterange":
                #         timex = time_index(0)
                #         datetime_value = timex[0].replace("(", "").replace(")", "").split(",")
                #         result.start_date = datetime_value[0]
                #         if len(date_entities) > 1:
                #             timex = time_index(1)
                #             datetime_value = timex[0].replace("(", "").replace(")", "").split(",")
                #             result.end_date = datetime_value[1]

                # else:
                #     result.start_date = datetime_start
                #     result.end_date = datetime_end



                    


                # ==== Budget ==== #
                budget_entities = recognizer_result.entities.get("$instance", {}).get("budget", [])
                if len(budget_entities) > 0:

                    #Get top score text if multiple budget objects
                    score = []
                    for i, info in enumerate(budget_entities):
                         score_i = info["score"]
                         score.append(score_i)
                    
                    index_max_score = score.index(max(score))
                    result.budget = budget_entities[index_max_score]["text"]


        
        except Exception as exception:
            print(exception)

        return intent, result
