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

4. **Copiar o `docker-compose.yaml` e `.env`**:
   ```bash
   # Copiar o docker-compose.yaml do repositório para /app
   # Criar .env em /app com as variáveis necessárias (baseado em .env.example)
   ```

5. **Fazer pull inicial e subir os serviços**:
   ```bash
   cd /app
   docker compose pull
   docker compose up -d
   docker compose run --rm django python manage.py migrate --noinput
   docker compose run --rm django python manage.py compilemessages
   docker compose run --rm django python manage.py collectstatic --noinput
   ```

### Observações

- O deploy assume que a VPS já tem o `docker compose` instalado e funcionando.
- Para simplificar, publique a imagem como **public** no GHCR; se mantiver privada, a VPS precisará autenticar no
  registry.
- O serviço do app no compose é esperado como `django`; não mude esse nome no `docker-compose.yaml`.
- O compose da VPS compartilha os volumes `portfolio_app_static_data` e `portfolio_app_media_data` com o `nginx-proxy`.
- O deploy roda `migrate` e `collectstatic` dentro do container do app após o `up -d`.
- O `nginx-proxy` continua separado do app para facilitar manutenção e futuras migrações.
