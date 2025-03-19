
from openai import AsyncOpenAI
from scripts.tools import format_message, construct_prompt, LIMIT_EXCEEDED_MSG

class OpenRouterAPI:
    def __init__(self, token, model):
        self.model = model
        self.client = AsyncOpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=str(token),
        )
    
    async def get_response(self, message) -> str:
        completion = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": construct_prompt(message)
                }
            ]
        )
        if not completion.choices: return LIMIT_EXCEEDED_MSG, False
        response = completion.choices[0].message.content
        
        # Format the response
        return format_message(response)
