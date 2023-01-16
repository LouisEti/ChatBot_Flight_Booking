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
    APP_ID = os.environ.get("MicrosoftAppId", "") 
    APP_PASSWORD = os.environ.get("MicrosoftAppPassword", "")

    ############## LUIS Service ###############
    LUIS_APP_ID = os.environ.get("LuisAppId", "109b72ce-ba2e-48f4-b3e6-06889b9320a4")
    LUIS_API_KEY = os.environ.get("LuisAPIKey", "10cf4c925d3640e39afc9c76af3488c8")
    LUIS_API_HOST_NAME = os.environ.get("LuisAPIHostName", "https://luis-oc.cognitiveservices.azure.com/")

    ############## App Insights Service ###############
    APPINSIGHTS_INSTRUMENTATION_KEY = os.environ.get(
        "AppInsightsInstrumentationKey", "a19f3cda-7f37-4f23-b477-3957a640e706")
    # AppInsight API Key: leidc4yesmvlrjy8u3n0b78l6s0s2z1e4cnnxrb1
