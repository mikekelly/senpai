import traceback
import random
import string
import openai
from colorama import Fore
import config
import prompts

def generate_context_messages(id):
    return [
        {
            "role": "system",
            "content": f"You are {id}, an AI agent able to control a debian server by providing responses in python which are evaluated by a python3 interpreter running as root."
        }
    ]

def exception_as_string(ex):
    lines = traceback.format_exception(ex, chain=False)
    lines_without_agent = lines[:1] + lines[3:]
    return ''.join(lines_without_agent)

def generate_random_id():
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choices(characters, k=4))

class Agent:
    def __init__(self):
        self.locals = None
        self.id = "SENPAI-" + generate_random_id()
        self.messages = generate_context_messages(self.id)
        self.logger = AgentLogger(self.id)
        self.runtime_print(f"{self.id} initiated")

    def give_objective(self, objective):
        no_op = lambda *args: None
        self.prompt(prompts.initiate_with_objective(objective), on_prompt=no_op)

    def prompt(self, prompt, on_prompt=None):
        self.logger.debug(f'PROMPT:\n{prompt}')
        if on_prompt:
            on_prompt(prompt)
        else:
            self.on_prompt(prompt)

        ai_response = self.get_response_from_ai(prompt)
        self.logger.debug(f'AI RESPONSE:\n{ai_response}')
        self.on_ai_response(ai_response)
        self.record_interaction(prompt, ai_response)

        try:
            print = self.runtime_print # special print for AI's code
            feedback_runtime_value_to_senpai = self.feedback_runtime_value_to_senpai # avoid AI having to specify self when calling feedback
            if not self.locals:
                self.locals = locals()
            # TODO: capture all stdout & stderr using redirect_stdout & redirect_stderr
            exec(ai_response, globals(), self.locals)
        except FeedbackHalt:
            return ai_response
        except Exception as exception:
            exception_message = self.feedback_that_python_code_raised_an_exception(exception)
            self.prompt(exception_message)
        else:
            self.logger.debug("SESSION END")
            return ai_response

    def on_prompt(self, prompt):
        print(Fore.RESET + self.prefix_text(prompt, ">"))

    def on_ai_response(self, ai_response):
        print(Fore.GREEN + self.prefix_text(ai_response, "<") + Fore.RESET)

    def runtime_print(self, text):
        print(Fore.BLUE + self.prefix_text(text, "*") + Fore.RESET)

    def prefix_text(self, text, indicator):
        prefix = f"{self.id} {indicator} "
        lines = text.split("\n")
        prefixed_lines = [prefix + line for line in lines]
        return "\n".join(prefixed_lines)

    def feedback_runtime_value_to_senpai(self, text):
        self.prompt(text)
        raise FeedbackHalt

    def get_response_from_ai(self, prompt, temperature=0.5, max_tokens=1000, role="user"):
        prompt_message = {"role": role, "content": prompt}

        messages = self.messages + [prompt_message]

        self.logger.debug(f'MESSAGES SENT TO OPENAI: \n{messages}')

        response = openai.ChatCompletion.create(
            model=config.OPENAI_MODEL,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            n=1,
        )

        self.logger.debug(f'RAW JSON RESPONSE FROM OPENAI: \n{response}')
        text = response.choices[0].message.content.strip()
        return text

    def record_interaction(self, prompt, ai_response):
        self.messages.append({"role": "user", "content": prompt})
        self.messages.append({"role": "assistant", "content": ai_response})
        # TODO: persist to state file somewhere (which agent should check when it's created)

    def feedback_that_python_code_raised_an_exception(self, exception):
        return f'RUNTIME ERROR. Your code produced this exception:\n\n{exception_as_string(exception)}\n\nAdjust the code to try and avoid this error'

class AgentLogger:
    def __init__(self, agent_id):
        self.agent_id = agent_id

    def debug(self, text):
        with open(f'logs/{self.agent_id}_debug.log','a') as f:
            f.write("\n" + text)

class FeedbackHalt(Exception):
    "Raised when the feedback function is called to halt further processing"
    pass
