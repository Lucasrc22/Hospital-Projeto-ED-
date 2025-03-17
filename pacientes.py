class Paciente:
    def __init__(self, nome, prioridade):
        self.nome = nome
        self.prioridade = prioridade

    def __repr__(self):
        return f"{self.nome} (Prioridade: {self.prioridade})"