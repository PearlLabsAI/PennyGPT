# chat_litellm.py
import sys
import os
from litellm import completion
import pynvim


class ChatMessage:
    def __init__(self, content, sender):
        self.content = content
        self.sender = sender


class ChatHistory:
    def __init__(self):
        self.messages = []

    def add_message(self, message):
        self.messages.append(message)

    def to_list(self):
        return [msg.content for msg in self.messages]


chat_history = ChatHistory()


def send_message():
    user_message = pynvim.eval('input("Message: ")')
    if user_message:
        chat_history.add_message(ChatMessage(user_message, "user"))
        update_chat_display()
        get_litellm_response(user_message)


def get_litellm_response(user_message):
    context = get_file_contents()
    messages = [{"role": "user", "content": user_message}]
    if context:
        messages.append({"role": "system", "content": context})

    response = completion(model="gpt-4", messages=messages)

    assistant_message = response.choices[0].message["content"]
    chat_history.add_message(ChatMessage(assistant_message, "assistant"))
    update_chat_display()


def update_chat_display():
    nvim.command("silent! %d")  # Clear the buffer
    for message in chat_history.messages:
        nvim.command(f'call append(line("$"), "{message.sender}: {message.content}")')
    nvim.command("normal! G")


context_files = []


def add_file_to_context():
    file_path = nvim.eval('input("File path: ")')
    if os.path.exists(file_path) and file_path not in context_files:
        context_files.append(file_path)
        nvim.command(f'echo "Added {file_path} to context files."')


def remove_file_from_context():
    file_path = nvim.eval('input("File path to remove: ")')
    if file_path in context_files:
        context_files.remove(file_path)
        nvim.command(f'echo "Removed {file_path} from context files."')
    else:
        nvim.command(f'echo "File {file_path} not found in context files."')


def get_file_contents():
    contents = []
    for file_path in context_files:
        try:
            with open(file_path, "r") as file:
                contents.append(f"File: {file_path}\n{file.read()}\n")
        except Exception as e:
            contents.append(f"Error reading {file_path}: {str(e)}\n")
    return "\n".join(contents)
