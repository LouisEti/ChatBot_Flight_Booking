# :dart: A chatbot to book flights
The goal of this project is to prototype a 1st version of FlyMe chatbot, which will help customers to book a vacation package.

The MVP (*Minimum Viable Product*) should help us to identify the "BookFlight" intent and return the 5 main entities which constitutes flight's details:
- origin city;
- destination city;
- departure date;
- return date;
- bugdet.

**Expected output**: the Bot should be able to reformulate the flight's details, ask confirmation (yes/no) from the user, then, if correct, end conversation with a booking message.

# :card_index_dividers: Dataset
[Microsoft Frames Dataset](https://www.microsoft.com/en-us/research/project/frames-dataset/#!download)

<img src='/static\frames_dataset.png'>

The dialogues were built with 2 humans' talk via a chat interface, one was playing the role of the user and the other one was playing the role of the conversational agent (a database of 250+ packages was available to compose of a hotel and round-trip flights). 

The dialogues are more complex than what we need for the MVP, thus, it's very good basis for the next steps of the project.

# :scroll: Tasks
- :heavy_check_mark: Perform Exploratory Data Analysis (EDA) and Data wrangling;
- :heavy_check_mark: Build LUIS App, including train-test-publish-predict part;
- :heavy_check_mark: Copy [Microsoft Core Bot Python Samples, including App Insights](https://github.com/microsoft/BotBuilder-Samples/tree/main/samples/python/21.corebot-app-insights) from Github, and adapt the scripts to the project's objectives;
- :heavy_check_mark: Monitor the performance of the chatbot with App Insights;
- :heavy_check_mark: Plan and integrate automated testing;
- :heavy_check_mark: Embed in Azure Web App for model serving (deploy).
