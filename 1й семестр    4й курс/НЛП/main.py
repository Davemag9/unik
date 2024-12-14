import numpy as np
import json
import torch
import torch.nn as nn
import torch.optim as optim

# Повідомлення для тренування
message = "Нарди грати будеш?"  # Можна змінити на будь-яке інше

# Створення словника символів
vocab = sorted(set(message))
vocab_size = len(vocab) + 2  # +2 для токенів [ і ]
vocab = ["["] + vocab + ["]"]  # Додаємо токени початку і кінця
vocab_dict = {ch: i for i, ch in enumerate(vocab)}
inv_vocab_dict = {i: ch for i, ch in enumerate(vocab)}

# Гіперпараметри
embedding_dim = 96
hidden_dim = 160
learning_rate = 0.01
num_epochs = 500

# Закодування повідомлення в індекси
encoded_message = [vocab_dict[ch] for ch in message]
encoded_message = [vocab_dict["["]] + encoded_message + [vocab_dict["]"]]

# Модель Elman RNN
class ElmanRNN(nn.Module):
    def __init__(self, vocab_size, embedding_dim, hidden_dim):
        super(ElmanRNN, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        self.rnn_cell = nn.RNNCell(embedding_dim, hidden_dim)
        self.fc = nn.Linear(hidden_dim, vocab_size)
    
    def forward(self, input_seq):
        h_t = torch.zeros((1, hidden_dim))  # Початковий прихований стан
        output_seq = []
        for token in input_seq:
            x_t = self.embedding(token)
            h_t = self.rnn_cell(x_t, h_t)
            y_t = self.fc(h_t)
            output_seq.append(y_t)
        return output_seq

# Підготовка даних для PyTorch
input_seq = torch.tensor(encoded_message[:-1]).unsqueeze(1)  # Вхідні дані (без останнього символу)
target_seq = torch.tensor(encoded_message[1:]).unsqueeze(1)  # Цільові дані (без першого символу)

# Ініціалізація моделі, втрат та оптимізатора
model = ElmanRNN(vocab_size, embedding_dim, hidden_dim)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=learning_rate)

# Тренування
for epoch in range(num_epochs):
    model.train()
    optimizer.zero_grad()
    output_seq = model(input_seq)
    loss = sum(criterion(output.view(1, -1), target_seq[i]) for i, output in enumerate(output_seq))
    loss.backward()
    optimizer.step()
    if (epoch + 1) % 50 == 0:
        print(f'Epoch [{epoch + 1}/{num_epochs}], Loss: {loss.item():.4f}')

# Збереження ваг у форматі JSON
def save_weights(model):
    weights = {
        "embedding.weight": model.embedding.weight.detach().numpy().tolist(),
        "U_h.weight": model.rnn_cell.weight_hh.detach().numpy().tolist(),
        "U_h.bias": model.rnn_cell.bias_hh.detach().numpy().tolist(),
        "W_h.weight": model.rnn_cell.weight_ih.detach().numpy().tolist(),
        "W_h.bias": model.rnn_cell.bias_ih.detach().numpy().tolist(),
        "W_y.weight": model.fc.weight.detach().numpy().tolist(),
        "W_y.bias": model.fc.bias.detach().numpy().tolist(),
        "vocab": vocab
    }
    for name, weight in weights.items():
        with open(f"{name}.json", "w") as f:
            json.dump(weight, f)

save_weights(model)
print("Ваги збережено у форматі JSON.")
