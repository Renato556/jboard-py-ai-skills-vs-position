# JBoard - AI Skills vs Position Analyzer

Uma API REST robusta e escalável para análise de compatibilidade entre habilidades de candidatos e requisitos de vagas de emprego, desenvolvida em Python com Flask e IA, focada especialmente em oportunidades "Brazilian Friendly" para desenvolvedores brasileiros.

## 🎯 Objetivo da Aplicação

O JBoard AI Skills vs Position Analyzer é uma aplicação backend completa que permite:
- Analisar compatibilidade entre habilidades de candidatos e vagas usando IA
- Processar e extrair informações de páginas de vagas via web scraping
- Fornecer recomendações personalizadas baseadas em análise por OpenAI GPT
- Identificar oportunidades "Brazilian Friendly" para desenvolvedores brasileiros
- Fornecer arquitetura escalável preparada para deploy em Azure Container Apps

## 🚀 Funcionalidades

### Endpoints da API

#### **Análise de Compatibilidade (Analysis)**
- **POST** `/analyse` - Analisar compatibilidade entre habilidades e vaga

**Campos Suportados:**
- Lista de habilidades do candidato
- URL da vaga de emprego para análise
- Extração automática de descrição da vaga
- Análise por IA com porcentagem de compatibilidade
- **Brazilian Friendly**: Recomendações específicas para o mercado brasileiro

#### **Processamento Inteligente**
- **Web Scraping**: Extração automática de meta descriptions
- **Text Processing**: Limpeza e formatação de texto otimizada
- **AI Analysis**: Integração com OpenAI GPT para análise contextual
- **Recommendations**: Sugestões personalizadas para melhoria de perfil

**Exemplo de Requisição:**
```json
{
  "position": "https://exemplo.com/vaga-desenvolvedor-python",
  "skills": ["Python", "Flask", "Docker", "Azure", "MongoDB"]
}
```

### Características Técnicas

#### **Arquitetura Limpa**
- **Controllers**: Handlers HTTP para processamento de requisições
- **Services**: Lógica de negócio centralizada (Analysis, OpenAI, Web Scraping, Text Processing)
- **Models**: Estruturas de dados e entidades (Request/Response DTOs)
- **Utils**: Utilitários para logging e validação
- **Config**: Configurações centralizadas da aplicação

#### **Recursos Avançados**
- **AI-Powered Analysis**: Sistema especializado com OpenAI GPT
- **Smart Web Scraping**: Extração inteligente de conteúdo web
- **Brazilian Market Focus**: Análises focadas no mercado brasileiro
- **Validação de Dados**: Validação robusta em todas as camadas
- **Error Handling**: Tratamento de erros padronizado
- **Logging**: Sistema de logs estruturado

## 🔧 Tecnologias Utilizadas

- **Linguagem**: Python 3.12
- **Framework Web**: Flask 3.1.2
- **IA/ML**: OpenAI 2.1.0
- **Web Scraping**: BeautifulSoup 4.14.2, Requests 2.32.5
- **Configuração**: Python-dotenv 1.1.1
- **Containerização**: Docker
- **Cloud**: Azure Container Apps
- **Testes**: pytest 8.4.2 + pytest-cov 7.0.0
- **CI/CD**: GitHub Actions

## 📦 Instalação e Execução

### Pré-requisitos
- Python 3.12 ou superior
- Conta OpenAI com API key válida
- Docker e Docker Compose
- Git

### Instalação Local

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/seu-usuario/jboard-py-ai-skills-vs-position.git
   cd jboard-py-ai-skills-vs-position
   ```

2. **Criar ambiente virtual:**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # ou
   source venv/bin/activate  # Linux/Mac
   ```

3. **Configurar variáveis de ambiente:**
   ```bash
   # Criar arquivo .env na raiz do projeto
   OPENAI_API_KEY=sua_openai_api_key
   OPENAI_API_URL=https://api.openai.com/v1/chat/completions
   FLASK_ENV=development
   DEBUG=true
   HOST=0.0.0.0
   PORT=8082
   REQUEST_TIMEOUT=10
   LOG_LEVEL=INFO
   ```

4. **Instalar dependências:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Executar em modo desenvolvimento:**
   ```bash
   python app.py
   ```

6. **Acessar a aplicação:**
   ```
   http://localhost:8082
   ```

### Execução com Docker

```bash
# Build da imagem
docker build -t jboard-ai-analyzer .

# Executar container
docker run -p 8082:8082 --env-file .env jboard-ai-analyzer
```

## 🧪 Execução de Testes

### Testes Unitários

```bash
# Executar todos os testes
python -m pytest src/ -v

# Executar testes com coverage
python -m pytest src/ -v --cov=src --cov-report=html

# Executar testes com coverage mínima
python -m pytest src/ -v --cov=src --cov-report=html --cov-fail-under=90
```

### Testes por Módulo

```bash
# Testes dos controllers
python -m pytest src/controllers/ -v

# Testes dos services
python -m pytest src/services/ -v

# Testes dos models
python -m pytest src/models/ -v

# Testes dos utils
python -m pytest src/utils/ -v
```

### Cobertura de Testes

```bash
# Gerar relatório de cobertura
python -m pytest src/ --cov=src --cov-report=html

# Visualizar relatório no navegador
# O relatório será gerado em htmlcov/index.html
```

## 🤖 Configuração de IA e Integração

### OpenAI GPT Integration

**Configuração da API:**
- **Model**: GPT-3.5-turbo ou GPT-4
- **Max Tokens**: 1000 tokens por resposta
- **Language**: Português brasileiro
- **Temperature**: Configurável para consistência

**System Prompt Especializado:**
```text
Você é um assistente de IA especializado em match de habilidades com descrição de vagas.
Analise a compatibilidade entre as habilidades do candidato e os requisitos da vaga.
Forneça uma porcentagem estimada de match e recomendações específicas.
Todas as respostas devem ser em português do Brasil.
```

**Características:**
- **Análise Contextual**: Comparação inteligente de habilidades vs requisitos
- **Market Focus**: Especialização no mercado brasileiro
- **Actionable Insights**: Recomendações práticas e implementáveis
- **Consistent Output**: Respostas estruturadas e padronizadas

### Web Scraping Configuration

**Recursos Suportados:**
- Extração de meta descriptions
- Timeout configurável para requisições

**Configuração:**
```env
# Configurações da aplicação
FLASK_ENV=development
DEBUG=True
HOST=0.0.0.0
PORT=8082

# Configurações de requisições HTTP
REQUEST_TIMEOUT=300

# Configurações de logging
LOG_LEVEL=INFO

# OpenAI API Configuration
OPENAI_API_KEY=sua_openai_api_key
OPENAI_API_URL=
```

## 🔄 Deploy e Workflows

### Azure Deploy Workflow

O projeto utiliza GitHub Actions para deploy automático no Azure Container Apps.

#### Triggers
- **Push**: Branches `main` e `master`
- **Manual**: `workflow_dispatch` para deploy sob demanda

#### Etapas do Pipeline

##### Test and Setup
- Checkout do código
- Setup Python 3.12
- Cache de dependências pip
- Instalação de dependências (`pip install -r requirements.txt`)
- Execução de testes (`pytest src/ --cov=src --cov-fail-under=90`)
- Validação de qualidade do código

##### Build and Deploy
- Setup Docker Buildx
- Login no Azure
- Login no Azure Container Registry
- Build e push da imagem Docker
- Deploy no Azure Container Apps
- Configuração de variáveis de ambiente de produção

#### Variáveis de Ambiente
- **AZURE_CONTAINER_REGISTRY**: `jboardregistry`
- **CONTAINER_APP_NAME**: `jboard-py-ai-skills-vs-position`
- **RESOURCE_GROUP**: `jboard-microservices`
- **IMAGE_NAME**: `jboard-py-ai-skills-vs-position`
- **TARGET_PORT**: `8082`

#### Secrets Necessários
- **AZURE_CREDENTIALS**: Credenciais de service principal
- **ACR_USERNAME**: Usuário do Container Registry
- **ACR_PASSWORD**: Senha do Container Registry
- **OPENAI_API_KEY**: Chave da API OpenAI
- **OPENAI_API_URL**: URL da API OpenAI

#### Características Avançadas
- **Dependency Validation**: Verificação de dependências antes do deploy
- **Multi-stage Testing**: Testes em paralelo para eficiência
- **Environment Isolation**: Configurações específicas por ambiente
- **Health Checks**: Verificação de deploy bem-sucedido
- **AI Integration Validation**: Teste de conectividade com OpenAI

### 🔒 Segurança em Produção

**⚠️ IMPORTANTE**: Arquitetura de segurança enterprise implementada.

**Características de Segurança:**
- ✅ **Rede Privada**: Execução em VNet privada do Azure
- ✅ **Zero Internet Exposure**: Nenhum endpoint público direto
- ✅ **Comunicação Interna**: Acesso apenas via rede interna
- ✅ **API Gateway**: Acesso externo controlado via gateway
- ✅ **Isolamento Completo**: Máxima segurança por isolamento
- ✅ **SSL/TLS**: Criptografia em todas as comunicações
- ✅ **API Key Protection**: Chaves de IA protegidas via Azure Key Vault

### Variáveis de Ambiente de Produção
```yaml
FLASK_ENV: production
DEBUG: false
HOST: 0.0.0.0
PORT: 8082
REQUEST_TIMEOUT: 300
LOG_LEVEL: INFO
OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
OPENAI_API_URL: ${{ secrets.OPENAI_API_URL }}
```

## 🤖 Como Funciona a Análise por IA

### Fluxo de Processamento

#### 1. **Recepção da Requisição**
```json
{
  "position": "https://exemplo.com/vaga-desenvolvedor-python",
  "skills": ["Python", "Flask", "Docker", "Azure", "MongoDB"]
}
```

#### 2. **Web Scraping Inteligente**
- Acesso à URL da vaga fornecida
- Extração da meta description da página
- Limpeza e formatação do texto extraído
- Validação do conteúdo obtido

#### 3. **Preparação para IA**
- Conversão da lista de habilidades em texto estruturado
- Combinação das habilidades com descrição da vaga
- Montagem do prompt otimizado para análise

#### 4. **Análise OpenAI GPT**
- **System Prompt**: Define assistente especialista em match de habilidades
- **User Content**: Combina habilidades do candidato com descrição da vaga
- **Configuração**: Máximo 1000 tokens de resposta
- **Idioma**: Respostas sempre em português brasileiro

#### 5. **Retorno Estruturado**
```json
{
  "message": "Com base na análise da vaga, suas habilidades apresentam um match de aproximadamente 85%. Você possui excelente compatibilidade em Python, Flask e Docker. Para aumentar suas chances: considere estudar Kubernetes e obter certificações Azure específicas..."
}
```

### Exemplo de Uso Completo

#### Requisição
```bash
curl -X POST http://localhost:8082/analyse \
  -H "Content-Type: application/json" \
  -d '{
    "position": "https://jobs.ashbyhq.com/EMPRESA/ID_DA_VAGA",
    "skills": ["Python", "Flask", "Docker", "AWS", "PostgreSQL"]
  }'
```

#### Resposta
```json
{
  "message": "Com base na análise da vaga, suas habilidades apresentam um match de aproximadamente 75%. Você possui forte compatibilidade em Python, Flask e Docker, que são requisitos principais. Para aumentar suas chances: considere estudar Kubernetes (mencionado como diferencial), obter certificações AWS específicas para a área, e desenvolver experiência com metodologias ágeis. Recomendo destacar projetos práticos que demonstrem suas habilidades em Python e Flask."
}
```

## 🤝 Colaboração e Desenvolvimento

### Padrões de Código
- **PEP 8**: Estilo de código Python padrão
- **Type Hints**: Tipagem para melhor documentação
- **Docstrings**: Documentação de funções e classes
- **Conventional Commits**: Mensagens padronizadas
- **Clean Architecture**: Organização em camadas bem definidas

### Estrutura de Pastas
```
src/
├── controllers/       # Handlers HTTP para endpoints
├── services/         # Lógica de negócio (AI, Web Scraping, Text Processing)
├── models/          # Estruturas de dados (DTOs)
├── config/          # Configurações da aplicação
└── utils/           # Utilitários (logging, validação)
```

### Contribuindo
1. Fork o projeto
2. Crie uma branch feature (`git checkout -b feature/amazing-feature`)
3. Commit suas mudanças (`git commit -m 'Add some amazing-feature'`)
4. Push para a branch (`git push origin feature/amazing-feature`)
5. Abra um Pull Request

### Code Review
- Todos os PRs devem passar nos testes
- Cobertura mínima de 90%
- Aprovação de pelo menos 1 reviewer
- Validação automática do CI/CD
- Verificação de integração com APIs externas

## 📄 Licenciamento

### Licença MIT

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

**Resumo da Licença:**
- ✅ Uso comercial
- ✅ Modificação
- ✅ Distribuição
- ✅ Uso privado
- ❌ Responsabilidade
- ❌ Garantia

### Direitos de Uso
- Permitido uso em projetos comerciais
- Permitida modificação do código
- Créditos aos autores originais apreciados
- Não há garantias de funcionamento
