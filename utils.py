import requests




class llm_chatter:
    def __init__(self,host='http://127.0.0.1:5000/v1/chat/completions'):
        self.host = host
        self.msg_history = []
        self.headers = {
            "Content-Type": "application/json"
        }
    def communicate(self,prompt,greedy=False,reset=False,max_tokens=2048,template="Llama-v3"):
        if reset:
            self.msg_history = []
        self.msg_history.append({"role": "user", "content": prompt})
        data = {
            "mode": "instruct",
            "max_tokens": max_tokens,
            "instruction_template":template,
                "messages": self.msg_history
        }
        if greedy:
            data['temperature'] = 0
        response = requests.post(self.host, headers=self.headers, json=data, verify=False)
        answer = response.json()['choices'][0]['message']['content']
        self.msg_history.append({"role": "assistant", "content": answer})
        return answer

class llm_completion:
    def __init__(self,host='http://127.0.0.1:5000/v1/completions'):
        self.host = host
        self.headers = {
            "Content-Type": "application/json"
        }
    def complete(self,prompt,greedy=False,max_tokens=2048):
        data = {
            "max_tokens": max_tokens,
            "prompt": prompt,
            "temperature": 1,
            "top_p": 0.9,
        }
        if greedy:
            data['temperature'] = 0
        response = requests.post(self.host, headers=self.headers, json=data, verify=False)
        answer = response.json()['choices'][0]['text']
        return answer
