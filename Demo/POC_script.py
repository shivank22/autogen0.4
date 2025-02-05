from dotenv import load_dotenv
load_dotenv()
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken

MODEL = "gpt-4o-mini"
openai = OpenAI()
db_name = "Metadata"


folders = glob.glob("train/*")


text_loader_kwargs = {'encoding': 'utf-8'}

documents2 = []
for folder in folders:
    doc_type = os.path.basename(folder)
    if os.path.isdir(folder):
        loader = DirectoryLoader(folder, glob="**/*", loader_cls=TextLoader, loader_kwargs=text_loader_kwargs)
        folder_docs = loader.load()
    else:
        loader = TextLoader(folder, **text_loader_kwargs)
        folder_docs = loader.load()
    for doc in folder_docs:
        doc.metadata["doc_type"] = doc_type
        documents2.append(doc)

class SQLWriteAgent(BaseChatAgent):
    async def on_messages(self, messages: Sequence[ChatMessage], cancellation_token: CancellationToken) -> Response:
        
        
        return Response(chat_message=TextMessage(content="Custom reply", source=self.name))

    async def on_reset(self, cancellation_token: CancellationToken) -> None:
        pass

    @property
    def produced_message_types(self) -> Sequence[type[ChatMessage]]:
        return (TextMessage,)