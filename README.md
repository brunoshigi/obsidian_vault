# Vault Organizer

Este script organiza seu vault de arquivos, gerando arquivos `README.md`, `INDEX.md` e `vault_structure.json` que ajudam na navegação e visualização da estrutura de pastas e arquivos.

## Funcionalidades

- **Geração de `README.md` em cada pasta**: Facilita a navegação individual nas pastas do vault.
- **Criação de um `INDEX.md` global**: Fornece uma visão geral de todo o vault, permitindo acesso rápido a qualquer arquivo ou pasta.
- **Geração de `vault_structure.json`**: Contém a estrutura completa do vault em formato JSON para uso em ferramentas de visualização.
- **Extração de informações relevantes**:
  - Arquivos `.md` e `.txt`: Lê o conteúdo e apresenta uma descrição resumida.
  - Arquivos `.py`: Extrai e lista as funções definidas.
  - Arquivos `.ipynb`: Identifica e lista as bibliotecas importadas.

## Como usar

1. **Clone ou faça o download deste repositório**:

   ```bash
   git clone https://github.com/SeuNomeDeUsuario/vault-organizer.git
   ```

2. **Instale as dependências necessárias**:

   Certifique-se de ter o Python 3.6 ou superior instalado. Em seguida, instale a biblioteca nbformat:

   ```bash
   pip install nbformat
   ```

3. **Atualize o caminho do vault no script**:

   Abra o arquivo `vault_organizer.py` em um editor de texto e substitua o caminho do vault pela localização correta:

   ```python
   vault_path = Path(r"C:\Users\seu_usuario\caminho\para\seu\vault")
   ```

   Certifique-se de usar o prefixo `r` antes das aspas para indicar uma string bruta, especialmente se estiver usando barras invertidas `\` em caminhos do Windows.

4. **Execute o script**:

   No terminal ou prompt de comando, navegue até o diretório do projeto e execute:

   ```bash
   python vault_organizer.py
   ```

   O script irá percorrer o seu vault, gerar os arquivos necessários e apresentar uma mensagem ao concluir.

## Dependências

- **Python**: Versão 3.6 ou superior.
- **nbformat**: Para manipulação de arquivos Jupyter Notebook (.ipynb).

### Instalação:

   ```bash
   pip install nbformat
   ```

## Personalização

- **Tipos de arquivos suportados**: Você pode estender o script para suportar mais tipos de arquivos, adicionando funções de extração de conteúdo específicas.
- **Limite de descrição**: O limite de caracteres para as descrições pode ser ajustado nas funções `limpar_descricao` e `extrair_conteudo_arquivo`.

## Licença

Este projeto está licenciado sob os termos da licença MIT. Veja o arquivo LICENSE para mais detalhes.

**Nota**: Certifique-se de revisar e testar o script em um ambiente seguro antes de executá-lo em seu vault principal. Faça backups regulares dos seus dados para evitar perdas acidentais.

Se tiver dúvidas ou encontrar problemas, fique à vontade para abrir uma issue ou enviar uma pull request no repositório.

## Contribuições

Contribuições são bem-vindas! Se você deseja melhorar este projeto, siga estes passos:

1. Faça um fork do repositório.

2. Crie uma nova branch:

   ```bash
   git checkout -b feature/nova-funcionalidade
   ```

3. Faça suas alterações e commit:

   ```bash
   git commit -m "Adiciona nova funcionalidade"
   ```

4. Envie para o seu fork:

   ```bash
   git push origin feature/nova-funcionalidade
   ```

5. Abra um Pull Request no GitHub.