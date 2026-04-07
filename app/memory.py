
class ConversationMemory:
    def __init__(self, system_prompt=None):
        self.messages = []
        if system_prompt:
            self.set_system_prompt(system_prompt)

    def set_system_prompt(self, prompt):
        self.messages = [{"role": "system", "content": prompt}]

    def add_user_input(self, text):
        self.messages.append({"role": "user", "content": text})

    def add_assistant_response(self, text):
        self.messages.append({"role": "assistant", "content": text})

    def get_messages(self):
        return self.messages
