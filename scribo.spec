# -*- mode: python ; coding: utf-8 -*-

# Bloco para importar dependências extras, caso necessário
block_cipher = None

# Configurações principais do executável
a = Analysis(
    ['gui.py'],  # Arquivo principal do aplicativo
    pathex=[],  # Caminho adicional (pode ser vazio)
    binaries=[],  # Dependências de binários adicionais, se houver
    datas=[],  # Dependências de arquivos de dados, se houver
    hiddenimports=[],  # Importações ocultas (use se precisar importar algo manualmente)
    hookspath=[],  # Hooks personalizados (se necessário)
    hooksconfig={},
    runtime_hooks=[],  # Gancho de execução, caso precise configurar algo antes de rodar o código principal
    excludes=[],  # Módulos excluídos, caso haja algum
    win_no_prefer_redirects=False,  # Preferências do Windows para binários de 32 bits
    win_private_assemblies=False,  # Configuração para montagens privadas do Windows
    cipher=block_cipher,  # Ciframento para código adicional
    noarchive=False,  # Se true, não agrupa arquivos no executável
)

# Construção do executável sem o console
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,  # Scripts que vão compor o executável
    a.binaries,  # Binários adicionais
    a.zipfiles,  # Arquivos zip incluídos
    a.datas,  # Dados adicionais (ex: imagens, configurações, etc.)
    [],
    name='scribo',  # Nome do executável
    debug=False,  # Desativar modo debug
    bootloader_ignore_signals=False,  # Permitir controle sobre sinais do bootloader
    strip=False,  # Remover símbolos de debug para otimizar o tamanho
    upx=True,  # Compactar o executável com UPX, se instalado
    upx_exclude=[],  # Excluir arquivos da compressão UPX, se necessário
    runtime_tmpdir=None,  # Diretório temporário em tempo de execução
    console=False,  # **Não abrir o console**
    icon='scribo.ico'  # Ícone do aplicativo, opcional (use o caminho para o ícone)
)

# Bloco para criação de instaladores adicionais (se necessário)
coll = COLLECT(
    exe,
    a.binaries,  # Arquivos binários
    a.zipfiles,  # Arquivos zip
    a.datas,  # Arquivos de dados (ex: imagens, ícones, etc.)
    strip=False,  # Remover símbolos de debug (opcional)
    upx=True,  # Compactar com UPX, se disponível
    upx_exclude=[],  # Excluir arquivos da compressão UPX
    name='scribo'  # Nome final do conjunto de arquivos
)
