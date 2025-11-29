from django.db import models

class Colaborador(models.Model):
    nome = models.CharField(max_length=255)
    email = models.EmailField(unique=True, help_text="Email único do colaborador")
    funcao = models.CharField(max_length=255, blank=True, null=True)
    # Adicione outros campos se precisar (ex: matrícula, cargo, etc.)

    def __str__(self):
        return self.nome

class Equipamento(models.Model):
    nome = models.CharField(max_length=255)
    marca = models.CharField(max_length=100)
    quantidade = models.PositiveIntegerField(default=0) # Garante que a quantidade não seja negativa

    def __str__(self):
        return f"{self.nome} ({self.marca})"

class Emprestimos(models.Model):
    nome = models.ForeignKey(Colaborador, on_delete=models.PROTECT, verbose_name="Colaborador")
    equipamento = models.ForeignKey(Equipamento, on_delete=models.PROTECT, verbose_name="Equipamento")
    quantidade = models.PositiveIntegerField(default=1, help_text="Quantidade emprestada")
    data_emprestimo = models.DateTimeField(auto_now_add=True, verbose_name="Data do Empréstimo")
    data_prazo = models.DateTimeField(verbose_name="Data de Devolução Prevista")
    estoque_disponivel = models.PositiveIntegerField(default=0, help_text="Quantidade disponível no estoque após empréstimo")
    
    def __str__(self):
        return f"{self.nome.nome} - {self.equipamento.nome} ({self.quantidade})"

