""" chat.py
A single line function. Lets you chat to ChatGPT from the terminal.
Using council for this is extremely overkill, probably!
"""

from collections import defaultdict
from typing import List
import sys

import dotenv

# from council import Chain, LLMSkill, LLMController, LLMEvaluator, Agent, BasicFilter
from council.chains import Chain
from council.skills import LLMSkill
from council.controllers import LLMController
from council.evaluators import LLMEvaluator
from council.agents import Agent
from council.filters import BasicFilter
from council.llm import OpenAILLM


# NOTE: Could also just be an environmental variable, no?
dotenv.load_dotenv()

class LLMCaller:
    def __init__(self,
                 prompt: str,
                 model: str='openai',
                 name: str='Caller',
                 description: str='Calls prompt.',
                 response_threshold: int=5):
        if model == 'openai':
            pass
        model = OpenAILLM.from_env()

        self.skill = LLMSkill(llm=model, system_prompt=prompt)
        self.chain = Chain(name=name, description=description,
                           runners=[self.skill])
        self.controller = LLMController(llm=model,
                                        chains=[self.chain],
                                        response_threshold=response_threshold)
        self.evaluator = LLMEvaluator(llm=model)
        self.agent = Agent(controller=self.controller,
                           evaluator=self.evaluator,
                           filter=BasicFilter())

    def prompt_model(self, input: str) -> str:
        result = self.agent.execute_from_user_message(input)  # agents.AgentResult
        self.last_result = result  # Save for later reference.
        best_message = result.try_best_message  # Option[ChatResult]
        # NOTE: `try_best_message` should just be Optional[ChatResult].
        if best_message.is_some():
            return best_message.unwrap().message
        else:
            print("No messages returned.")
            return ''


def read_prompt_db() -> List[str]:
    """ NOTE: Could be expanded, but wasn't worth the effort. """
    with open('prompts.txt') as t:
        return ''.join(t.readlines())



if __name__ == "__main__":
    prompt = read_prompt_db()
    if len(sys.argv) > 1:
        uinput = ' '.join(sys.argv[1:])
    else:
        uinput = input(">> ")
    print('Asking...')
    rc = LLMCaller(prompt)
    response = rc.prompt_model(uinput)
    print(response)
    print()
