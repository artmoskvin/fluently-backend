import openai
from openai.error import AuthenticationError
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential, retry_if_not_exception_type,
)


@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6),
       retry=retry_if_not_exception_type(AuthenticationError))
def get_completion(text: str) -> str:
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=text,
        temperature=0.5,
        max_tokens=32,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=[".", "\n"]
    )
    return response['choices'][0]['text']
