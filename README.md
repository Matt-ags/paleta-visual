# 🎨 Paleta Visual - Gerador de Paletas de Cores com Gatos

Um aplicativo visual interativo construído com Flet que permite gerar paletas de cores a partir de imagens de gatos (via Cataas API), salvar paletas localmente em um banco de dados SQLite, copiar cores para a área de transferência e explorar imagens adoráveis

# 📸 Demonstração
![Demonstracao](https://github.com/user-attachments/assets/6c2d0fa1-2b8b-4f20-9e20-2e7df0aef4f2)

## 🚀 Funcionalidades

- 🔍 Exploração de imagens aleatórias de gatos via API do Cataas.

- 🎨 Geração de paletas de cores a partir de imagens utilizando a biblioteca colorgram.

- 💾 Armazenamento de paletas no banco de dados SQLite local.

- 📋 Copia rápida de cores HEX clicando na cor desejada.

- ❌ Exclusão de paletas salvas diretamente pela interface.

- 🖼️ Anexar imagem local para gerar uma paleta personalizada.

- ✨ Interface moderna com layout responsivo via Flet.

## 🛠️ Tecnologias Utilizadas

- Python 3

- Flet — para interface gráfica

- colorgram.py — para extração de cores

- Cataas API — para imagens de gatos

- sqlite3 — banco de dados local

- pyperclip — para cópia de valores para a área de transferência

## 🧪 Como executar localmente:

1. Clone o repositório:
``` bash
  git clone https://github.com/Matt-ags/paleta-visual.git
  cd paleta-visual
```

2. Crie um ambiente virtual e ative:
```bash
  python -m venv venv
  # Windows:
  venv\Scripts\activate
  # Linux/macOS:
  source venv/bin/activate
```

3. Instale as dependências:

```bash
  pip install -r requirements.txt
```

4. Execute o projeto:

```bash
  flet run main.py
```
  | 💡 O suporte para imagem local (anexar arquivo) funciona apenas em modo local (não via navegador/web).
