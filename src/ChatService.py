import asyncio
from typing import List, Dict, AsyncGenerator
from litellm import completion


class ChatService:
    """Handles interactions with the chat API."""

    @staticmethod
    async def get_chat_response(
        messages: List[Dict[str, str]], context: str
    ) -> AsyncGenerator[str, None]:
        try:
            system_message = {"role": "system",
                              "content": f"Context:\n{context}"}
            all_messages = [system_message] + messages

            stream = await asyncio.to_thread(
                completion,
                model="bedrock/anthropic.claude-3-sonnet-20240229-v1:0",
                messages=all_messages,
                max_tokens=1000,
                temperature=0.2,
                stream=True,
            )

            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    yield chunk.choices[0].delta.content
                await asyncio.sleep(0)  # Allow other tasks to run

        except Exception as e:
            yield f"Error: {str(e)}"
