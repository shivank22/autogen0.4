from dotenv import load_dotenv
load_dotenv()
import pandas as pd
from autogen_ext.tools.langchain import LangChainToolAdapter
from langchain_experimental.tools.python.tool import PythonAstREPLTool
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken

df = pd.read_csv("vm_data_final.csv")
tool = LangChainToolAdapter(PythonAstREPLTool(locals={"df": df}))
model_client = OpenAIChatCompletionClient(model="gpt-4o-mini")
DataLoaderAgent = AssistantAgent(
    "assistant", tools=[tool], model_client=model_client, system_message="Use the `df` variable to access the dataset."
)
import asyncio

asyncio.run(Console(
    DataLoaderAgent.on_messages_stream(
        [TextMessage(content="What's the Trend for Decom_date of VMs?", source="user")], CancellationToken()
    )
))