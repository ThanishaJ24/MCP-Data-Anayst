from typing import TypedDict

from langgraph.graph import StateGraph, END

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

from app.sql_tools import run_sql, get_schema

import os
from dotenv import load_dotenv

load_dotenv()


# ---------------------------------
# LLM
# ---------------------------------

llm = ChatOpenAI(
    model="gpt-4o-mini",
    api_key=os.getenv("OPENAI_API_KEY")
)


# ---------------------------------
# STATE
# ---------------------------------

class AgentState(TypedDict):

    question: str
    schema: str
    sql_query: str
    sql_result: list
    insights: str
    error: str
    retry_count: int


# ---------------------------------
# NODE 1
# LOAD SCHEMA
# ---------------------------------

def load_schema(state: AgentState):

    schema = get_schema()

    return {
        "schema": schema
    }


# ---------------------------------
# NODE 2
# GENERATE SQL
# ---------------------------------

def generate_sql(state: AgentState):

    question = state["question"]

    schema = state["schema"]

    previous_error = state.get("error", "")

    prompt = f"""
    You are a SQLite SQL expert.

    Database Schema:
    {schema}

    Convert the user question into correct SQLite SQL.

    Question:
    {question}
    """

    # Retry correction
    if previous_error:

        prompt += f"""

        Previous SQL generated this error:
        {previous_error}

        Fix the SQL query.
        """

    prompt += """

    Return ONLY SQL query without ```sql```.
    """

    response = llm.invoke([
        HumanMessage(content=prompt)
    ])

    return {
        "sql_query": response.content
    }


# ---------------------------------
# NODE 3
# EXECUTE SQL
# ---------------------------------

def execute_sql(state: AgentState):

    query = state["sql_query"]

    result = run_sql(query)

    # Success
    if result["success"]:

        return {
            "sql_result": result["data"],
            "error": ""
        }

    # Failure
    return {
        "error": result["error"]
    }


# ---------------------------------
# CONDITIONAL CHECK
# ---------------------------------

def check_sql_status(state: AgentState):

    if state.get("error"):

        retry_count = state.get("retry_count", 0)

        # Max retries
        if retry_count >= 2:

            return "failed"

        return "retry"

    return "success"


# ---------------------------------
# NODE 4
# RETRY NODE
# ---------------------------------

def retry_sql(state: AgentState):

    retry_count = state.get("retry_count", 0)

    return {
        "retry_count": retry_count + 1
    }


# ---------------------------------
# NODE 5
# GENERATE INSIGHTS
# ---------------------------------

def generate_insights(state: AgentState):

    prompt = f"""
    Question:
    {state['question']}

    SQL Result:
    {state['sql_result']}

    Generate short business insights.
    """

    response = llm.invoke([
        HumanMessage(content=prompt)
    ])

    return {
        "insights": response.content
    }


# ---------------------------------
# BUILD LANGGRAPH
# ---------------------------------

graph = StateGraph(AgentState)


# Add Nodes
graph.add_node("load_schema", load_schema)

graph.add_node("generate_sql", generate_sql)

graph.add_node("execute_sql", execute_sql)

graph.add_node("retry_sql", retry_sql)

graph.add_node("generate_insights", generate_insights)


# Entry Point
graph.set_entry_point("load_schema")


# Main Flow
graph.add_edge("load_schema", "generate_sql")

graph.add_edge("generate_sql", "execute_sql")


# Conditional Retry Logic
graph.add_conditional_edges(
    "execute_sql",
    check_sql_status,
    {
        "retry": "retry_sql",
        "success": "generate_insights",
        "failed": END
    }
)


# Retry Flow
graph.add_edge("retry_sql", "generate_sql")


# Final Flow
graph.add_edge("generate_insights", END)


# Compile Graph
app_graph = graph.compile()


# ---------------------------------
# MAIN FUNCTION
# ---------------------------------

def ask_agent(question: str):

    result = app_graph.invoke({

        "question": question,

        "retry_count": 0

    })

    return result