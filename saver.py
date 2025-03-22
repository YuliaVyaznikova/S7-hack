from smolagents import Tool

class SavingResponsesTool(Tool):
    name = "saving_responses_tool"
    description = """
    This tool save responses until there are enough responses, 
    in this case you will informed about it by return value"""
    
    inputs = {
        "response": {
            "type": "any",
            "description": """ tuple should consist of 3 elements. Only three.
            element 1 is user emotion (e.g. positive or negative or neutral - only theese), 
            element 2 is theme of the user's response (one or two words),
            element 3 is summary of the user's response (sentence or two)""",
        }
    }

    output_type = "string"


    def __init__(self):
        super().__init__()
        self.maxlen = 200
        self.response_list = []

    def forward(self, response):
        self.response_list.append(response)
        if len(self.response_list) <= self.maxlen:
            return f'{len(self.response_list)} responses from {self.maxlen} we need more responses, add them only from web pages.'
        else:
            print(f'end. response list of {self.maxlen} responses was made.')
            for row in self.response_list:
                print(row)
            return 'it is enough of responses, you can stop adding them and provide final answer'

    def get_response_list(self):
        return self.response_list