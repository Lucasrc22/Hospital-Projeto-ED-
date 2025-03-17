class No:
    def __init__(self, paciente, prioridade):
        self.paciente = paciente
        self.prioridade = prioridade
        self.proximo = None

    def mostrar_no(self):
        print(f"Paciente: {self.paciente.nome}, Prioridade: {self.prioridade}")


class FilaAtendimento:
    def __init__(self):
        self.primeiro = None
        self.ultimo = None

    def adicionar_paciente(self, paciente):
        novo = No(paciente, paciente.prioridade)
        
        if self.primeiro is None:  
            self.primeiro = novo
            self.ultimo = novo
        else:
            atual = self.primeiro
            anterior = None

            while atual is not None and atual.prioridade >= novo.prioridade:
                anterior = atual
                atual = atual.proximo

            if anterior is None:  
                novo.proximo = self.primeiro
                self.primeiro = novo
            else:  
                novo.proximo = atual
                anterior.proximo = novo
                if atual is None:  
                    self.ultimo = novo

        print(f"Paciente {paciente.nome} adicionado à fila com prioridade {paciente.prioridade}.\n")

    def chamar_proximo(self):
        
        if self.primeiro is None:
            print("Nenhum paciente na fila de atendimento.")
            return None
        
        paciente_atendido = self.primeiro
        self.primeiro = self.primeiro.proximo

        if self.primeiro is None:  
            self.ultimo = None

        print(f"Atendendo paciente: {paciente_atendido.paciente.nome}")
        return paciente_atendido.paciente

    def visualizar_fila(self):
        
        if self.primeiro is None:
            print("A fila de atendimento está vazia.")
            return
        
        print("Fila de Atendimento:")
        atual = self.primeiro
        while atual is not None:
            atual.mostrar_no()
            atual = atual.proximo
