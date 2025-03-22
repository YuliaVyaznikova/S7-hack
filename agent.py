from huggingface_hub import login
from smolagents import CodeAgent, DuckDuckGoSearchTool, HfApiModel, tool

from visiter import visit_web_page
from saver import SavingResponsesTool
from finder import search_tool

login()

saving_responses_tool = SavingResponsesTool()
agent = CodeAgent(tools=[saving_responses_tool, search_tool, visit_web_page], model=HfApiModel(), 
                  additional_authorized_imports=['os', 'open', 'io', 'close', 'write'],
                  max_steps=50)

prompt = '''Search in internet some responses on S7 airlines company.
Based on what you find, formulate table of responses, (by rows, using saving_responses_tool) consist of 3 columns: 
client emotion (positive, negative or neutral), object of response (for example: food on the plane, attitude of screening staff or other)
and summary of user's response (one sentence).
If there are multiple objects of response in one response, split it to three rows of table. 
If there are no date, write NaN. Use saving responses tool, add responses to it until it will say you that there is enough responses.
don't write so much code. Visit web page tool don't give you html, it gives you text of the page. Don't generate samples manually.
Don't classify responses by code, do it by yourself.

Firstly use search tool to find the links to websites with responses.
Next go to that links and find responses. Some links may not work, use different.
Add what you get to the table.
Repeat until table tool will not say you that it is enough.

Add only real responses! Search for them if you don't have them.
Don't hallucinate reviews please. Add them only based on the info from web.
please read return value from saving response tool. It will tell you when it is enough.
Add responses manually (not automated) as soon as you finded them.'''

# agent.run(input("prompt: "))
agent.run(prompt)
