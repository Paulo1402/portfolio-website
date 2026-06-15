# ❤️ Portfolio App

Este é um aplicativo de portfólio que exibe informações sobre mim e meus projetos.

O aplicativo foi desenvolvido em
Python com o framework Django utilizando seu sistema de templates com Boostrap na estilização do frontend.

## 🚀 Tecnologias

- Python
- Django
- HTML
- CSS
- JavaScript
- Bootstrap
- PostgreSQL
- Nginx

## CI/CD

O repositório usa GitHub Actions para:

- validar o código com Ruff e `manage.py check`
- rodar os testes do Django
- buildar a imagem Docker e publicar no GHCR
- acessar a VPS por SSH e atualizar o stack com `docker compose`

## Docker Compose

O projeto usa arquivos Compose separados por ambiente:

- `docker-compose.dev.yml`: ambiente local com build da imagem, PostgreSQL e servidor de desenvolvimento do Django.
- `docker-compose.prod.yml`: template versionado do ambiente de produção, copiado para a VPS como `docker-compose.yml`.

Para subir o ambiente local:

```bash
docker compose -f docker-compose.dev.yml up -d --build
```

O serviço `django` do compose local roda as migrações e inicia `python manage.py runserver 0.0.0.0:8000`.
Depois de subir, acesse `http://localhost:8000/`.

O deploy de produção não copia o código da aplicação para a VPS. A pipeline publica a imagem no GHCR, copia
`docker-compose.prod.yml` para a VPS como `docker-compose.yml`, copia `scripts/deploy-app.sh` como `deploy-app.sh`,
e executa o script remoto para atualizar o stack.

### Repository variables and secrets

- Repository variables (set in GitHub Settings → Variables):
  - `VPS_HOST`: IP ou domínio da VPS
  - `VPS_USER`: nome do usuário de deploy (ex: `deployer`)
  - `VPS_APP_DIR`: diretório da aplicação (ex: `/app`)

- Secrets (set in GitHub Settings → Secrets):
  - `VPS_SSH_KEY`: chave privada SSH do usuário (keep secret)
  - `VPS_KNOWN_HOSTS`: contents of your VPS known_hosts (see README for how to generate)

### Setup da VPS

1. **Criar usuário de deploy e gerar SSH key**:
   ```bash
   sudo useradd -m -s /bin/bash -c "Portfolio app deployment" deployer
   sudo usermod -aG docker deployer
   sudo mkdir -p /app
   sudo chown deployer:deployer /app
   sudo -u deployer ssh-keygen -t ed25519 -f /home/deployer/.ssh/id_ed25519 -N ""
   ```

2. **Criar rede Docker compartilhada**:
   ```bash
   docker network create proxy_network
   ```

3. **Criar volumes compartilhados com nginx-proxy**:
   ```bash
   docker volume create portfolio_app_static_data
   docker volume create portfolio_app_media_data
   ```

4. **Criar `.env` na VPS**:
   ```bash
   # Criar .env em /app com as variáveis necessárias (baseado em .env.example)
   ```

5. **Fazer deploy inicial manual, se necessário**:
   ```bash
   cd /app
   # A pipeline cria/atualiza docker-compose.yml, deploy-app.sh e .env.cicd.
   # Após esses arquivos existirem na VPS:
   ./deploy-app.sh
   ```

### Observações

- O deploy assume que a VPS já tem o `docker compose` instalado e funcionando.
- Para simplificar, publique a imagem como **public** no GHCR; se mantiver privada, a VPS precisará autenticar no
  registry.
- O serviço do app no compose é esperado como `django`; não mude esse nome no `docker-compose.prod.yml`.
- Na VPS, o arquivo de produção versionado é publicado como `docker-compose.yml`.
- O compose da VPS compartilha os volumes `portfolio_app_static_data` e `portfolio_app_media_data` com o `nginx-proxy`.
- O deploy roda `migrate` e `collectstatic` dentro do container do app após o `up -d`.
- O `nginx-proxy` continua separado do app para facilitar manutenção e futuras migrações.
