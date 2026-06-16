# 🐶 Tindog Automation  
Automação em Python + Selenium para fazer login automático no Tindog e dar likes de forma contínua, lidando com popups e falhas temporárias.

---

## 🚀 Funcionalidades

- **Login automático** via Facebark  
- **Gestão de popups** (permissões, cookies, match)  
- **Swipe automático** (20 likes por execução)  
- **Sistema de retry** para tornar o fluxo resiliente  
- **Chrome persistente** com perfil dedicado  

---

## 📦 Requisitos

- Python 3.10+
- Selenium
- python-dotenv
- Chrome + ChromeDriver compatível

Instalação:

```bash
pip install selenium python-dotenv
```

---

## 🔧 Configuração

Cria um ficheiro `.env` com:

```
TINDOG_URL=https://tindog.example.com
TINDOG_EMAIL=teu_email
TINDOG_PASSWORD=tua_password
```

O script cria automaticamente um perfil Chrome persistente em `./chrome_profile`.

---

## 🧠 Como funciona

### 1. Inicialização do WebDriver
- Carrega variáveis do `.env`
- Cria um perfil Chrome dedicado
- Abre o site do Tindog

### 2. Login Automático
A função `login_automatically()`:

- Clica no botão **Log in**
- Seleciona **Facebark**
- Troca para a janela de autenticação
- Preenche email e password
- Submete o formulário
- Regressa à janela principal
- Fecha popups iniciais
- Aguarda até a homepage carregar (`main.tindog-swipe-container`)

### 3. Dar Likes
A função `like_dog()`:

- Tenta clicar no botão **Like**
- Se houver popup de match → fecha
- Se o botão ainda não existir → espera até aparecer
- Repete o processo 20 vezes

### 4. Retry Automático
A função `retry(func)`:

- Executa a função
- Se falhar por timeout, elemento inexistente ou clique bloqueado → tenta novamente
- Após várias tentativas falhadas → lança erro

---

## ▶️ Execução

O script corre automaticamente:

```python
retry(login_automatically, description="Login")
retry(like_dog, description="Like a dog")
```

---

## 📁 Estrutura do Projeto

```
.
├── chrome_profile/      # Perfil persistente do Chrome
├── .env                 # Credenciais e URL
├── script.py            # Código principal
└── README.md            # Este ficheiro
```

---

## 📝 Notas

- O script evita `time.sleep()` sempre que possível, usando esperas explícitas do Selenium.
- O retry torna o fluxo robusto contra popups, delays e falhas temporárias.
- O perfil Chrome permite manter sessões e cookies entre execuções.
