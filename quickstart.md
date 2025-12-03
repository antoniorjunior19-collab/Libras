# ⚡ Libras Bridge - Início Rápido

## 🎯 Para Começar AGORA (5 minutos)

### 1. Instalar
```bash
pip install -r requirements.txt
```

### 2. Treinar (escolha uma opção)

**Opção A: Treinar seu próprio modelo** (recomendado para TCC)
```bash
# Coletar dados (repita para cada gesto)
python coleta_dados.py  # Edite: gesto = "ola"
python coleta_dados.py  # Edite: gesto = "sim"  
python coleta_dados.py  # Edite: gesto = "nao"

# Processar e treinar
python preprocessamento.py
python treinamento.py
```

**Opção B: Usar modelo pré-treinado** (se disponível)
```bash
# Apenas copie o arquivo modelo_libras.pkl para a pasta raiz
```

### 3. Executar
```bash
python run.py
# OU
python app.py
```

### 4. Acessar
```
http://localhost:5000
```

---

## 📂 Estrutura Mínima Necessária

```
libras-bridge/
├── app.py                    ✅ OBRIGATÓRIO
├── requirements.txt          ✅ OBRIGATÓRIO
├── modelo_libras.pkl         ✅ OBRIGATÓRIO (gerado no passo 2)
├── templates/
│   └── index.html           ✅ OBRIGATÓRIO
└── static/
    ├── styles.css           ✅ OBRIGATÓRIO
    ├── script.js            ✅ OBRIGATÓRIO
    ├── logolibras.png       ⚠️ RECOMENDADO
    └── computadorlibras.png ⚠️ RECOMENDADO
```

---

## 🚨 Problemas Comuns

| Problema | Solução Rápida |
|----------|----------------|
| ❌ Modelo não encontrado | Execute: `python treinamento.py` |
| ❌ Câmera não abre | Feche Zoom/Teams/Skype |
| ❌ Página em branco | Verifique pastas `templates/` e `static/` |
| ❌ ImportError | Execute: `pip install -r requirements.txt` |
| ❌ Porta 5000 ocupada | Mude em `config.py`: `SERVER_PORT = 5001` |

---

## 💡 Dicas para Coleta de Dados

✅ **FAÇA:**
- Colete 50-100 clips por gesto
- Varie a posição da mão
- Use boa iluminação
- Mantenha fundo neutro

❌ **NÃO FAÇA:**
- Movimentos muito rápidos
- Iluminação fraca/escura
- Fundo muito confuso
- Gestos muito parecidos

---

## 🎨 Personalização Rápida

### Adicionar Novo Gesto

1. **Coletar:**
```python
# coleta_dados.py, linha 7:
gesto = "obrigado"  # Novo gesto
```

2. **Atualizar lista:**
```python
# preprocessamento.py, linha 5:
gestos = ["ola", "sim", "nao", "obrigado"]
```

3. **Retreinar:**
```bash
python coleta_dados.py
python preprocessamento.py
python treinamento.py
```

### Mudar Cores

Edite `static/styles.css`:
```css
:root {
  --teal: #6ea9a0;        /* Cor principal */
  --accent: #2b8b8a;      /* Cor de destaque */
  --hero-bg: #bdd6ea;     /* Fundo hero */
}
```

---

## 📊 Comandos Úteis

```bash
# Verificar instalação
python run.py

# Ver configurações
python config.py

# Testar câmera (sem web)
python realtime.py

# Verificar acurácia
python treinamento.py

# Coletar mais dados
python coleta_dados.py
```

---

## 🎓 Para o TCC

### Checklist de Apresentação

- [ ] Modelo treinado com boa acurácia (>85%)
- [ ] Pelo menos 3 gestos diferentes
- [ ] Interface funcionando sem erros
- [ ] Demonstração ao vivo preparada
- [ ] Backup do modelo (`modelo_libras.pkl`)
- [ ] Screenshots da interface
- [ ] Vídeo demo (opcional)

### Dados para Incluir no TCC

Execute `python treinamento.py` e anote:
- ✅ Acurácia do modelo: **_____%**
- ✅ Número de amostras: **_____**
- ✅ Gestos treinados: **_____**
- ✅ Tempo de resposta: **_____s**

---

## 🆘 Suporte Rápido

**Erro?** Verifique na ordem:

1. ✅ Python 3.8+ instalado?
2. ✅ `pip install -r requirements.txt` executado?
3. ✅ Estrutura de pastas correta?
4. ✅ `modelo_libras.pkl` existe?
5. ✅ Webcam funcionando?

**Ainda com problema?**
- Veja logs no terminal
- Teste com `python realtime.py`
- Recrie o ambiente virtual

---

## 🚀 Próximos Passos

Depois que tudo funcionar:

1. **Melhorar modelo:** Coletar mais dados
2. **Adicionar gestos:** Ampliar vocabulário
3. **Otimizar:** Aumentar FPS e acurácia
4. **Exportar:** Adicionar salvamento de traduções
5. **TTS:** Implementar texto-para-voz

---

**Tempo estimado:** 10-30 minutos (dependendo da coleta de dados)

**Boa sorte com o TCC! 🎓🌉**