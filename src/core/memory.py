class MemoryManager:
    def __init__(self, sys_prompt: str, max_msg: int = 20):
        self.sys_prompt = sys_prompt
        self.max_msg = max_msg
        self.messages = [{"role": "system", "content": sys_prompt}]

    def add_msg(self, role, content):
        self.messages.append({"role": role, "content": content})
        self._prune()

    def _prune(self):
        if len(self.messages) > self.max_msg + 1:
            self.messages = [self.messages[0]] + self.messages[-self.max_msg:]

    def get_messages(self):
        return self.messages