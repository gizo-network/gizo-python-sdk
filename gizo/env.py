class Env:
    def __init__(self, key: str, value):
        self.key = key
        self.value = value
    def env(self):
        return {self.key: self.value}

class Envs:
    def __init__(self, *envs: Env):
        self.envs = []
        for env in envs:
            self.envs.append(env.env())
