#!/usr/bin/env python3
"""
Script de inicialização do Libras Bridge
Verifica dependências e inicia o servidor
"""

import sys
import os
import subprocess

def check_python_version():
    """Verifica se a versão do Python é compatível"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ ERRO: Python 3.8+ é necessário")
        print(f"   Versão atual: {version.major}.{version.minor}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    return True

def check_dependencies():
    """Verifica se as dependências estão instaladas"""
    required = [
        'flask',
        'flask_socketio',
        'cv2',
        'mediapipe',
        'numpy',
        'joblib',
        'sklearn'
    ]
    
    missing = []
    for module in required:
        try:
            __import__(module)
            print(f"✅ {module}")
        except ImportError:
            missing.append(module)
            print(f"❌ {module} não encontrado")
    
    if missing:
        print("\n⚠️  Instale as dependências faltantes:")
        print("   pip install -r requirements.txt")
        return False
    
    return True

def check_model():
    """Verifica se o modelo treinado existe"""
    if not os.path.exists("modelo_libras.pkl"):
        print("\n⚠️  AVISO: Modelo não encontrado!")
        print("   Execute os seguintes comandos:")
        print("   1. python coleta_dados.py  (para cada gesto)")
        print("   2. python preprocessamento.py")
        print("   3. python treinamento.py")
        print("\n   O servidor será iniciado, mas não fará predições.")
        return False
    
    print("✅ Modelo encontrado")
    return True

def check_structure():
    """Verifica a estrutura de pastas"""
    folders = ['templates', 'static', 'static/assets', 'dataset']
    files = ['templates/index.html', 'static/styles.css', 'static/script.js']
    
    all_ok = True
    
    for folder in folders:
        if not os.path.exists(folder):
            print(f"❌ Pasta não encontrada: {folder}")
            all_ok = False
        else:
            print(f"✅ {folder}/")
    
    for file in files:
        if not os.path.exists(file):
            print(f"❌ Arquivo não encontrado: {file}")
            all_ok = False
        else:
            print(f"✅ {file}")
    
    return all_ok

def start_server():
    """Inicia o servidor Flask"""
    print("\n" + "="*50)
    print("🌉 INICIANDO LIBRAS BRIDGE")
    print("="*50 + "\n")
    
    try:
        subprocess.run([sys.executable, "app.py"])
    except KeyboardInterrupt:
        print("\n\n✋ Servidor encerrado pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro ao iniciar servidor: {e}")

def main():
    print("="*50)
    print("🔍 VERIFICANDO SISTEMA")
    print("="*50 + "\n")
    
    # Verificações
    checks = [
        ("Python", check_python_version()),
        ("Dependências", check_dependencies()),
        ("Estrutura", check_structure()),
        ("Modelo", check_model())
    ]
    
    print("\n" + "="*50)
    print("📊 RESUMO")
    print("="*50)
    
    for name, status in checks:
        icon = "✅" if status else "⚠️"
        print(f"{icon} {name}")
    
    # Verificar se há erros críticos (exceto modelo)
    critical_checks = checks[:-1]  # Todos exceto modelo
    if not all(status for _, status in critical_checks):
        print("\n❌ Corrija os erros acima antes de continuar.")
        sys.exit(1)
    
    # Perguntar se quer continuar sem modelo
    if not checks[-1][1]:  # Se modelo não existe
        response = input("\nDeseja iniciar mesmo assim? (s/n): ")
        if response.lower() != 's':
            print("Execução cancelada.")
            sys.exit(0)
    
    # Iniciar servidor
    start_server()

if __name__ == "__main__":
    main()