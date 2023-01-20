#!/usr/bin/env python
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
"""Configuration for the bot."""

import os


class DefaultConfig:
    """Bot Configuration"""

    ############## Azure Bot Service ###############
    PORT = 3978
    # APP_ID = os.environ.get("MicrosoftAppId", "") 
    # APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "")
    APP_ID = os.environ.get("MicrosoftAppId", "e1028877-1f92-4f3f-b783-851b6585d5be") 
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "87C8Q~zNB0fHRT1Szo4qrt43.1MV8ZlXZ2AKxc4q")

    ############## LUIS Service ###############
    LUIS_APP_ID = os.environ.get("LuisAppId", "c9636815-553b-46c8-84aa-900dea6f373a")
    LUIS_API_KEY = os.environ.get("LuisAPIKey", "0fa672cf0afb4c13831dafac089ac1bb")
    LUIS_API_HOST_NAME = os.environ.get("LuisAPIHostName", "https://flymeluis-authoring.cognitiveservices.azure.com/")

    ############## App Insights Service ###############
    APPINSIGHTS_INSTRUMENTATION_KEY = os.environ.get(
        "AppInsightsInstrumentationKey", "01f3ccc8-3d16-4998-9291-d2c773383390")