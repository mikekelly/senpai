import openai
import senpai
from senpai import config

def get_user_input():
    print("Prompt SENPAI:")
    return input()

def issue_prompt_to_fresh_agent(prompt):
    agent = senpai.Agent()
    agent.prompt(prompt)
    issue_prompt_to_fresh_agent(get_user_input())

openai.api_key = config.OPENAI_API_KEY
issue_prompt_to_fresh_agent(get_user_input())
