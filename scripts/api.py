
from openai import AsyncOpenAI
from scripts.tools import format_message, construct_prompt, LIMIT_EXCEEDED_MSG, OPENROUTER_TOKEN, AI_MODEL, AI_MODEL_IS_VISION, API_URL

class LLM_API:
    def __init__(self, api_url, token, model):
        self.model = model
        self.client = AsyncOpenAI(
            base_url=api_url,
            api_key=str(token),
        )
    
    async def get_response(self, message) -> str:
        completion = await self.client.chat.completions.create(
            model = self.model,
            messages = construct_prompt(message, openai_vision_api_format=AI_MODEL_IS_VISION),
        )
        if not completion.choices: return LIMIT_EXCEEDED_MSG, False
        response = completion.choices[0].message.content
        
        # Format the response
        return format_message(response)

def load_api() -> LLM_API:
    return LLM_API(api_url=API_URL, model=AI_MODEL, token=OPENROUTER_TOKEN)
