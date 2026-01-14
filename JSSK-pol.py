import os
import ast
from llama_index.llms.ollama import Ollama
from llama_parse import LlamaParse
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader,SummaryIndex
from llama_index.core.tools import QueryEngineTool
from dotenv import load_dotenv
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.query_engine.router_query_engine import RouterQueryEngine
from llama_index.core.selectors import LLMSingleSelector


load_dotenv()
documents = SimpleDirectoryReader(input_files=["final-jssk.pdf"]).load_data()
 
splitter = SentenceSplitter(chunk_size=1024)
nodes = splitter.get_nodes_from_documents(documents)
llm = Ollama(model="llama2")

summary_index = SummaryIndex(nodes)
vector_index = VectorStoreIndex(nodes)

summary_query_engine = summary_index.as_query_engine(
    response_mode="simple_summarize",
    use_async=True,
)
vector_query_engine = vector_index.as_query_engine()
from llama_index.core.tools import QueryEngineTool


summary_tool = QueryEngineTool.from_defaults(
    query_engine=summary_query_engine,
    description=(
        """Useful for summarization questions related to RKSK policy from multiple papers
        Also useful for making a list of all the analysis done based on the query."""
    ),
)

vector_tool = QueryEngineTool.from_defaults(
    query_engine=vector_query_engine,
    description=(
        "Useful for retrieving specific context from the RKSK policy from multiple papers"
    ),
)



query_engine = RouterQueryEngine(
    selector=LLMSingleSelector.from_defaults()  ,
    query_engine_tools=[
        summary_tool,
        vector_tool,
    ],
    verbose=True
)
response = query_engine.query("sum up the numerical results of this policy for me and give me the final analysis on how effective this policy was across the country.")
print(str(response))