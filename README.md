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

# :computer: Tools and Dependencies
Azure Portal, Azure LUIS cognitive services (Language Understanding), Microsoft Bot Framework SDK, Azure Bot, Azure Web App, Azure Application Insights, VS Code, Github (CI/CD)

<code>pip install botbuilder-core</code><br>
<code>pip install botbuilder-ai</code><br>
<code>pip install botbuilder-dialogs</code><br>
<code>pip install botbuilder-applicationinsights</code><br>
<code>pip install botbuilder-integration-applicationinsights-aiohttp</code><br>
<code>pip install datatypes-date-time</code><br>

or in the terminal, type : <code>pip install -r requirements.txt</code>

# :pushpin: References 
- [Azure for developers](https://azure.microsoft.com/en-us/developer/#featured-resources);
- [Azure LUIS quickstart with SDK](https://docs.microsoft.com/en-us/azure/cognitive-services/luis/client-libraries-rest-api?tabs=windows&pivots=programming-language-python);
- [Azure Bot Framework SDK documentation](https://docs.microsoft.com/en-us/azure/bot-service/index-bf-sdk?view=azure-bot-service-4.0); [Bot Framework Solutions - Overview](https://microsoft.github.io/botframework-solutions/index);
- Bot concepts: [How bots work](https://docs.microsoft.com/en-us/azure/bot-service/bot-builder-basics?view=azure-bot-service-4.0), [Managing state](https://docs.microsoft.com/en-us/azure/bot-service/bot-builder-concept-state?view=azure-bot-service-4.0), [Event / Activity handler](https://docs.microsoft.com/en-us/azure/bot-service/bot-activity-handler-concept?view=azure-bot-service-4.0&tabs=python), [Dialogs library](https://docs.microsoft.com/en-us/azure/bot-service/bot-builder-concept-dialog?view=azure-bot-service-4.0), [Waterfall dialogs](https://docs.microsoft.com/en-us/azure/bot-service/bot-builder-concept-waterfall-dialogs?view=azure-bot-service-4.0)
- [Azure App Service documentation](https://docs.microsoft.com/en-us/azure/app-service/);
- [What is Github Actions for Azure - Microsoft](https://docs.microsoft.com/en-us/azure/developer/github/github-actions); [Github Actions to build, test and deploy an application to Azure App Service - Github](https://docs.github.com/en/actions/deployment/deploying-to-azure-app-service);
- [Python Testing Frameworks](https://www.softwaretestinghelp.com/python-testing-frameworks/) - Sept. 2021: Robot, PyTest, Unittest, etc.;
- [Azure App Insights documentation](https://docs.microsoft.com/en-us/azure/azure-monitor/app/app-insights-overview);


