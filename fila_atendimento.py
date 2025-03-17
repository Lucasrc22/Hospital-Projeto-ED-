from collections import deque

class FilaAtendimento:
    def __init__(self):
        self.fila = deque()
    
    def adicionar_paciente(self, paciente):
    
        self.fila.append(paciente)
        print(f"Paciente {paciente.nome} adicionado à fila de atendimento.")
    
    def chamar_proximo(self):

        if self.fila:
            paciente = self.fila.popleft()
            print(f"Atendendo paciente: {paciente.nome}")
            return paciente
        else:
            print("Nenhum paciente na fila de atendimento.")
            return None
    
    def visualizar_fila(self):

        if self.fila:
            print("Fila de Atendimento:")
            for paciente in self.fila:
                print(f"- {paciente}")
        else:
            print("A fila de atendimento está vazia.")

