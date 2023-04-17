import os
import openai

def openaiTest():
    openai.api_key = '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'


    response = openai.Completion.create(
        model="text-davinci-002",
        prompt="Say this is a test",
        temperature=0,
        max_tokens=7,
    )

    print(response)

if __name__ == '__main__':
    openaiTest()
        