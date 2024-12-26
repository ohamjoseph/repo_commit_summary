from langgraph.prebuilt import create_react_agent

from llm import llm
from tools import get_commit_in_repo, generate_commit_summary


tools = [get_commit_in_repo]

prompt =\
    f'''
    You're an intelligent assistant.
    Your role is to retrieve the commits and summary of one or more repositories for a given period in order to take stock of the work for that period.
    
    In french please.
'''

react_search_agent = create_react_agent(llm, tools, state_modifier= prompt)


