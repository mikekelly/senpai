import sys
import openai
sys.path.append("senpai")
import senpai

openai.api_key = senpai.config.OPENAI_API_KEY
initial_objective = senpai.config.INITIAL_OBJECTIVE
agent = senpai.Agent()
print(f"Starting SENPAI with the following task:\n{initial_objective}")
agent.give_objective(initial_objective)
