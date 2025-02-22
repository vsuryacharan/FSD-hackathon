import os
from django.shortcuts import render
from django.http import JsonResponse
from dotenv import load_dotenv
from langchain import LLMMathChain
from langchain.agents import initialize_agent, Tool, AgentType
from langchain_openai import ChatOpenAI
from langchain.sql_database import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain.memory import ConversationBufferMemory

# Load API key from .env file
load_dotenv()
#openai_api_key = ""  #put ur api

if not openai_api_key:
    raise ValueError("Missing OPENAI_API_KEY! Set it in a .env file or as an environment variable.")

# Create LLM model
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo", openai_api_key=openai_api_key)

# Create LLM math tool
llm_math_chain = LLMMathChain.from_llm(llm=llm, verbose=True)

# Connect to SQLite database
db = SQLDatabase.from_uri("sqlite:///db.sqlite3")  # Django's default SQLite DB

# Create the database chain
db_chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)

# Define tools for the agent
tools = [
    Tool(
        name="MathTool",
        func=llm_math_chain.run,
        description="Useful for answering math-related questions."
    ),
    Tool(
        name="Product_Database",
        func=db_chain.run,
        description="Useful for answering questions about products in the database."
    )
]

# Add memory for conversation history
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Create the agent with memory
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.OPENAI_FUNCTIONS,
    verbose=True,
    memory=memory
)

def chatbot_response(request):
    """
    Django view to handle user queries and return chatbot responses.
    """
    user_input = request.GET.get("message", "")

    if not user_input:
        return JsonResponse({"response": "Please provide a valid query."})

    response = agent.run(user_input)
    
    return JsonResponse({"response": response})

def home(request):
    return render(request, "index.html")

from django.urls import path
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['POST'])
def chatbot_response_api(request):
    """
    REST API endpoint to handle user queries and return chatbot responses.
    """
    user_input = request.data.get("message", "")
    
    if not user_input:
        return Response({"response": "Please provide a valid query."}, status=status.HTTP_400_BAD_REQUEST)
    
    response = agent.run(user_input)
    
    return Response({"response": response}, status=status.HTTP_200_OK)

import os
from django.shortcuts import render
from django.http import JsonResponse
from langchain_openai import ChatOpenAI
from langchain_neo4j import GraphCypherQAChain, Neo4jGraph
from langchain.prompts import PromptTemplate



# Connect to Neo4j Database
graph = Neo4jGraph(
    url="neo4j://localhost:7687",
    username="neo4j",
    password="varactors-photos-priorities"  # Store password in .env
)

# Cypher query template
CYPHER_GENERATION_TEMPLATE = """
You are an expert Neo4j Developer translating user questions into Cypher to answer questions about movies and provide recommendations.
Convert the user's question based on the schema.

Schema: {schema}
Question: {question}
"""

cypher_generation_prompt = PromptTemplate(
    template=CYPHER_GENERATION_TEMPLATE,
    input_variables=["schema", "question"],
)

# LangChain Cypher Query Chain
cypher_chain = GraphCypherQAChain.from_llm(
    llm,
    graph=graph,
    cypher_prompt=cypher_generation_prompt,
    verbose=True,
    allow_dangerous_requests=True
)

def chatbot_response_graph(request):
    """
    Django view to handle user queries and return responses from Neo4j.
    Ensures only movies are returned.
    """
    user_input = request.GET.get("message", "")

    if not user_input:
        return JsonResponse({"response": "Please provide a valid query."})

    result = cypher_chain.invoke({"query": user_input})

    # Extract only movie objects
    if isinstance(result, dict) and "result" in result:
        movies = [{"title": item["title"]} for item in result["result"] if isinstance(item, dict) and "title" in item]

        return JsonResponse({"response": movies})

    return JsonResponse({"response": "No movies found."})


def graph(request):
    return render(request, "graph.html")
