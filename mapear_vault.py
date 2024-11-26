import os
import json
import re
from datetime import datetime
from pathlib import Path
import nbformat  # Para manipular arquivos .ipynb
import ast  # Para analisar código Python

def obter_informacoes_arquivo(caminho_arquivo):
    """Obtém tamanho, datas de criação/modificação e tipo de arquivo."""
    try:
        stat = caminho_arquivo.stat()
        tamanho = stat.st_size
        data_criacao = datetime.fromtimestamp(stat.st_ctime).strftime('%Y-%m-%d %H:%M:%S')
        data_modificacao = datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
        tipo = caminho_arquivo.suffix.lower()
        return tamanho, data_criacao, data_modificacao, tipo
    except Exception as e:
        print(f"Erro ao obter informações do arquivo {caminho_arquivo}: {e}")
        return 0, "N/A", "N/A", "N/A"

def limpar_descricao(descricao, limite=100):
    """Trunca descrições longas."""
    return (descricao[:limite] + " [...]") if len(descricao) > limite else descricao

def extrair_conteudo_arquivo(caminho_arquivo):
    """Lê o conteúdo de arquivos e extrai informações relevantes."""
    extensao = caminho_arquivo.suffix.lower()
    try:
        if extensao in [".md", ".txt"]:
            with caminho_arquivo.open("r", encoding="utf-8") as f:
                return limpar_descricao(f.read(), 300)
        elif extensao == ".py":
            with caminho_arquivo.open("r", encoding="utf-8") as f:
                source = f.read()
                tree = ast.parse(source)
                funcoes = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
                return f"Funções detectadas: {', '.join(funcoes)}" if funcoes else "Sem funções detectadas"
        elif extensao == ".ipynb":
            with caminho_arquivo.open("r", encoding="utf-8") as f:
                notebook = nbformat.read(f, as_version=4)
                bibliotecas = set()
                for cell in notebook.cells:
                    if cell.cell_type == 'code':
                        imports = re.findall(r'^\s*(?:from\s+(\S+)|import\s+(\S+))', cell.source, re.MULTILINE)
                        for imp in imports:
                            bibliotecas.update(filter(None, imp))
                return f"Bibliotecas: {', '.join(bibliotecas)}" if bibliotecas else "Sem bibliotecas detectadas"
        else:
            return "Tipo de arquivo não suportado para leitura"
    except Exception as e:
        return f"Erro ao processar arquivo: {e}"

def criar_readme(pasta, subpastas, arquivos):
    """Gera um README.md para a pasta especificada."""
    readme_path = pasta / "README.md"
    with readme_path.open("w", encoding="utf-8") as readme:
        readme.write(f"# {pasta.name}\n\n")
        readme.write(f"**Gerado em:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        if subpastas:
            readme.write("## Subpastas:\n")
            for subpasta in subpastas:
                relative_path = subpasta.relative_to(pasta)
                readme.write(f"- [{subpasta.name}]({relative_path / 'README.md'})\n")
            readme.write("\n")

        if arquivos:
            readme.write("## Arquivos:\n")
            readme.write("| Nome do Arquivo                     | Tipo   | Tamanho   | Criado em           | Modificado em       | Descrição                  |\n")
            readme.write("|-------------------------------------|--------|-----------|---------------------|---------------------|----------------------------|\n")
            for arquivo in arquivos:
                caminho_arquivo = pasta / arquivo
                tamanho, criacao, modificacao, tipo = obter_informacoes_arquivo(caminho_arquivo)
                descricao = extrair_conteudo_arquivo(caminho_arquivo)
                descricao_limpa = limpar_descricao(descricao, 80)
                relative_path = arquivo.relative_to(pasta)
                readme.write(f"| [{arquivo.name}]({relative_path}) | {tipo} | {tamanho / 1024:.2f} KB | {criacao} | {modificacao} | {descricao_limpa} |\n")
            readme.write("\n")

def criar_indice_geral(vault_path):
    """Gera um arquivo INDEX.md no diretório raiz para navegação global."""
    index_path = vault_path / "INDEX.md"
    with index_path.open("w", encoding="utf-8") as index:
        index.write("# Índice Geral do Vault\n\n")
        index.write(f"**Gerado em:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        for root, dirs, files in os.walk(vault_path):
            root_path = Path(root)
            nivel = len(root_path.relative_to(vault_path).parts)
            prefixo = "  " * nivel
            pasta_nome = root_path.name
            index.write(f"{prefixo}- **{pasta_nome}**\n")
            for file in files:
                if file not in ["README.md", "INDEX.md", "vault_structure.json"]:
                    caminho_relativo = Path(root_path / file).relative_to(vault_path)
                    index.write(f"{prefixo}  - [{file}]({caminho_relativo.as_posix()})\n")
            index.write("\n")

def gerar_estrutura_vault(vault_path):
    """Gera uma estrutura do vault em formato de dicionário para visualização."""
    estrutura = {}

    def walk_directory(pasta):
        conteudo = {'subpastas': {}, 'arquivos': []}
        for item in pasta.iterdir():
            if item.is_dir():
                conteudo['subpastas'][item.name] = walk_directory(item)
            elif item.is_file() and item.name not in ["README.md", "INDEX.md", "vault_structure.json"]:
                tamanho, criacao, modificacao, tipo = obter_informacoes_arquivo(item)
                descricao = extrair_conteudo_arquivo(item)
                conteudo['arquivos'].append({
                    'nome': item.name,
                    'caminho': str(item.relative_to(vault_path)),
                    'tamanho': tamanho,
                    'data_criacao': criacao,
                    'data_modificacao': modificacao,
                    'tipo': tipo,
                    'descricao': descricao
                })
        return conteudo

    estrutura = walk_directory(vault_path)
    return estrutura

def salvar_estrutura_json(estrutura, vault_path):
    """Salva a estrutura do vault em um arquivo JSON para visualização."""
    json_path = vault_path / "vault_structure.json"
    with json_path.open("w", encoding="utf-8") as json_file:
        json.dump(estrutura, json_file, ensure_ascii=False, indent=4)
    print(f"Estrutura do vault salva em {json_path}")

def organizar_vault(vault_path):
    """Organiza o Vault e gera os arquivos README.md, INDEX.md e vault_structure.json."""
    for root, dirs, files in os.walk(vault_path):
        root_path = Path(root)
        subpastas = [root_path / d for d in dirs]
        arquivos = [root_path / f for f in files if f not in ["README.md", "INDEX.md", "vault_structure.json"]]

        criar_readme(root_path, subpastas, arquivos)

    criar_indice_geral(vault_path)
    estrutura = gerar_estrutura_vault(vault_path)
    salvar_estrutura_json(estrutura, vault_path)
    print(f"Organização concluída! Arquivos README.md, INDEX.md e vault_structure.json gerados no Vault.")

# Caminho do Vault
vault_path = Path(r"C:\Users\geren\OneDrive\Documentos\Obsidian Vault\shigi.md")  # Substitua pelo caminho correto

# Executar organização
organizar_vault(vault_path)
