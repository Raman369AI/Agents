from zoneinfo import ZoneInfo
from google.adk.agents import Agent,BaseAgent,LlmAgent
from google.adk.tools import google_search
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
import google.genai.types as types
import requests
from google.adk.events import Event, EventActions
from google.adk.agents.invocation_context import InvocationContext
from typing import AsyncGenerator
from google.genai import types as genai_types 
from google.adk.tools import ToolContext, FunctionTool
import logging
from google.adk.tools import built_in_code_execution
from google.adk.tools import agent_tool








logging.basicConfig(level=logging.ERROR)
#from google.adk.tools import agent_tool
url = 'https://agents-course-unit4-scoring.hf.space/questions'
headers = {'accept': 'application/json'}
response = requests.get(url, headers=headers)

APP_NAME="weather_sentiment_agent"
USER_ID="user1234"
SESSION_ID="1234"
# class responses_api(BaseAgent):
#     async def _run_async_impl(self, ctx: InvocationContext)-> AsyncGenerator[Event, None]:
#         # This method is called when the agent is run
#         # You can implement your logic here
#         # For example, you can call an external API or perform some calculations
#         # and return the result
#         url = 'https://agents-course-unit4-scoring.hf.space/questions'
#         headers = {'accept': 'application/json'}
#         response = requests.get(url, headers=headers)
#         for i in response.json():
#             if i['file_name'] != '':
#                 url_file = f"https://agents-course-unit4-scoring.hf.space/files/{i['task_id']}"
#                 question = i['question']
#                 prompt = f"{question} and the file is {url_file}, give the final answer only"
#             else:
#                 question = i['question']
#                 prompt = f"{question} give the final answer only"
#             existing_responses = ctx.session.state.get("user:responses", [])
#             existing_responses.append(prompt)
#             ctx.session_state["user:responses"] = existing_responses

#             # Optionally, yield a single event to indicate completion or provide some output
#             yield Event(author=self.name, content=types.Content(parts=[types.Part(text=f"Fetched {len(questions_data)} questions."))])



def answer_questions():
    url = 'https://agents-course-unit4-scoring.hf.space/questions'
    headers = {'accept': 'application/json'}
    response = requests.get(url, headers=headers)
    prompts = []
    for i in response.json():
        task_id = i['task_id']
        if i['file_name'] != '':
            url_file = f"https://agents-course-unit4-scoring.hf.space/files/{i['task_id']}"
            question = i['question']
            prompt = f"{task_id}:{question} and the file is {url_file}, give the final answer only"
        else:
            question = i['question']
            prompt = f"{task_id}:{question} give the final answer only"
        prompts.append(prompt)
    return prompts
#responses_api = responses_api(name= 'responses_api_1')
from typing import Dict, Any
def submit_questions(answers: list[str]) -> Dict[str, Any]:
    url = 'https://agents-course-unit4-scoring.hf.space/submit'
    payload = {
    "username": "raman-ai-369",
    "agent_code": "your_agent_code",
    "answers": answers}
    headers = {'accept': 'application/json', "Content-Type": "application/json"}
    response = requests.post(url, headers=headers, json =payload)
    import json
    print(json.dumps(payload, indent=2))
    if response.status_code == 200:
        return response.json()
    else:
        response.raise_for_status()




responses_api = FunctionTool(func= answer_questions)
submit_api = FunctionTool(func=submit_questions)

# class QuestionAnswerer(LlmAgent):
#     async def _run_async_impl(self, ctx: InvocationContext) -> AsyncGenerator[Event, None]:
#         questions_to_answer = ctx.session_service.get('fetched_questions', [])
#         for q in questions_to_answer:
#             answer = await self._llm(messages=[types.ChatMessage(role="user", parts=[types.Part(text=q)])])
#             yield Event(author=self.name, content=answer.content)

# qa = QuestionAnswerer(name = 'qa_1', model="gemini-2.0-flash", description="Question Answerer")








APP_NAME="weather_sentiment_agent"
USER_ID="user1234"
SESSION_ID="1234"


code_agent = LlmAgent(
    name='codegaiaAgent',
    model="gemini-2.5-pro-preview-05-06",
    description=(
        "You are a smart agent that can write and execute code and answer any questions provided access the given files and answer"
    ),
    instruction = (
"if the question contains a file with .py ,Get the code file and depending on the question and the file provided, execute the code and provide the final answer. "
"If the question contains a spreadsheet file like .xlsx and .csv among others, get the file and depending on the question and the file provided, execute the code and provide the final answer. "
"use code like import pandas as pd , file = pd.read_csv('file.csv') and then use the file to answer the question. "
"if the question contains a file with .txt ,Get the code file and depending on the question and the file provided, execute the code and provide the final answer. "
"if the question contains a file with .json ,Get the code file and depending on the question and the file provided, execute the code and provide the final answer. "
"If you are writing code or if you get a code file, use the code execution tool to run the code and provide the final answer. "
)

,
    tools=[built_in_code_execution], 
    # Add the responses_api agent as a tool
    #sub_agents=[responses_api]
)


search_agent = LlmAgent(
    name='searchgaiaAgent',
    model="gemini-2.5-pro-preview-05-06",
    description=(
        "You are a smart agent that can search the web and answer any questions provided access the given files and answer"
    ),
    instruction = (
    "Get the url associated perform a search and consolidate the information provided and answer the provided question "
)

,
    tools=[google_search], 
    # Add the responses_api agent as a tool
    #sub_agents=[responses_api]
)

image_agent = LlmAgent(
    name='imagegaiaAgent',
    model="gemini-2.5-pro-preview-05-06",
    description=(
        "You are a smart agent that can when given a image file and answer any questions related to it"
    ),
    instruction = (
    "Get the image file from the link associated in the prompt use Gemini to watch the video and answer the provided question ")

,
   # tools=[google_search], 
    # Add the responses_api agent as a tool
    #sub_agents=[responses_api]
)


youtube_agent = LlmAgent(
    name='youtubegaiaAgent',
    model="gemini-2.5-pro-preview-05-06",
    description=(
        "You are a smart agent that can when given a youtube link watch it and answer any questions related to it"
    ),
    instruction = (
    "Get the youtube link associated use Gemini to watch the video and answer the provided question ")

,
   # tools=[google_search], 
    # Add the responses_api agent as a tool
    #sub_agents=[responses_api]
)

root_agent = LlmAgent(
    name='basegaiaAgent',
    model="gemini-2.5-pro-preview-05-06",
    description=(
        "You are a smart agent that can answer any questions provided access the given files and answer"
    ),
    instruction = (
    "You are a helpful agent. When the user asks to get the questions or makes a similar request, "
    "invoke your tool 'responses_api' to retrieve the questions. "
    "Once you receive the list of questions, loop over each question and provide a concise answer for each based on the question and any provided file. "
    "For every answer, return a dictionary with the keys task_id and submitted_answer, for example: "
    "{'task_id': 'the-task-id', 'submitted_answer': 'your answer'}. "
    "Collect all such dictionaries in a list (do not include any backslashes), and pass this list to the 'submit_api' tool to submit the answers."
)

,
    tools=[responses_api,submit_api,agent_tool.AgentTool(agent = code_agent),\
           agent_tool.AgentTool(agent = search_agent), agent_tool.AgentTool(youtube_agent), agent_tool.AgentTool(image_agent)], 
    # Add the responses_api agent as a tool
    #sub_agents=[responses_api]
)

# root_agent = LlmAgent(
#     name='gaiaAgent',
#     model="gemini-2.5-pro-preview-05-06",
#     description=(
#         "You are a smart agent that can answer any questions provided access the given files and answer"
#     ),
#     instruction = (
#     "You are a helpful agent. When the user asks to get the questions or makes a similar request, "
#     "invoke base agent. "
#     "Once you the answers check if are in correct format. "
#     #"Collect all such dictionaries in a list (do not include any backslashes), and pass this list to the 'submit_api' tool to submit the answers."
# )

# ,
#     #tools=[submit_api], 
#     # Add the responses_api agent as a tool
#     sub_agents=[base_agent]
# )

session_service = InMemorySessionService()
session = session_service.create_session(app_name=APP_NAME, \
                                        user_id=USER_ID,\
                                        session_id=SESSION_ID)

runner = Runner(agent=root_agent, app_name=APP_NAME, session_service=session_service)
# # def send_query_to_agent(root_agent, query, session):
# #     session = session
# #     content = types.Content(role='user', parts=[types.Part(text=query)])




# # async def main():
# #     await process_questions_and_answer()

# # if __name__ == "__main__":
# #     import asyncio
# #     asyncio.run(main())









        

   











