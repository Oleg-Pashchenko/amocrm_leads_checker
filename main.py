import openai
import json
import dotenv
import os

dotenv.load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')





def run_conversation():
    # Step 1: send the conversation and available functions to GPT
    messages = [{"role": "system", "content": "Подходит ли сделка под требования?"}]
    functions = [
        {
            "name": "get_is_lead_real_deal",
            "description": "Определить по сообщениям соответствует ли лид правилам сделки",
            "parameters": {
                "type": "object",
                "properties": {
                    "answer": {"type": "string", "enum": ["Да", "Нет", "Не знаю"]},
                },
                "required": ["answer"],
            },
        }
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
        functions=functions,
        function_call="auto",  # auto is default, but we'll be explicit
    )
    response_message = response["choices"][0]["message"]
    print(response_message)
    # Step 2: check if GPT wanted to call a function
    if response_message.get("function_call"):
        print(response_message['function_call']['arguments'])
        exit(0)
        # Step 3: call the function
        # Note: the JSON response may not always be valid; be sure to handle errors
        available_functions = {
            "get_current_weather": get_current_weather,
        }  # only one function in this example, but you can have multiple
        function_name = response_message["function_call"]["name"]
        fuction_to_call = available_functions[function_name]
        function_args = json.loads(response_message["function_call"]["arguments"])
        function_response = fuction_to_call(
            location=function_args.get("location"),
            unit=function_args.get("unit"),
        )

        # Step 4: send the info on the function call and function response to GPT
        messages.append(response_message)  # extend conversation with assistant's reply
        messages.append(
            {
                "role": "function",
                "name": function_name,
                "content": function_response,
            }
        )  # extend conversation with function response
        second_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=messages,
        )  # get a new response from GPT where it can see the function response
        return second_response


print(run_conversation())