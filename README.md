# Infrastructure Monitoring Stack

Production-ready мониторинг стек на базе Prometheus, Loki, Grafana с Telegram алертами.

## Стек технологий

| Компонент | Версия | Назначение |
|-----------|--------|------------|
| **Prometheus** | 3.7.1 | Сбор и хранение метрик |
| **Grafana** | latest | Визуализация и дашборды |
| **Loki** | latest | Централизованное логирование |
| **Promtail** | 3.5.7 | Агент сбора логов |
| **Alertmanager** | 0.27.0 | Управление алертами |
| **Telegram Bot** | 0.4.3 | Уведомления в Telegram |
| **Node Exporter** | 1.8.2 | Метрики хоста |
| **cAdvisor** | 0.49.1 | Метрики контейнеров |
| **HAProxy Exporter** | 0.15.0 | Метрики HAProxy |
| **Blackbox Exporter** | 0.25.0 | HTTP/TCP проверки |

## Возможности

### Сбор метрик
- Системные метрики (CPU, RAM, Disk, Network)
- Метрики Docker контейнеров
- Метрики HAProxy (backends, requests, response time)
- Health checks HTTP endpoints
- 9 активных targets

### Логирование
- Централизованный сбор логов всех контейнеров
- Парсинг логов HAProxy (9 полей)
- Парсинг логов Xray (6 полей)
- Парсинг логов Nginx (5 полей)
- Логи системных событий (SSH, sudo, security)
- Retention: 30 дней

### Алертинг
- 22 правила Prometheus (6 групп)
- 9 правил Loki (security)
- Уведомления в Telegram
- 2 уровня severity (critical, warning)
- Группировка и подавление алертов

**Покрытие алертами:**
- System Resources (CPU, Memory, Disk)
- Services (HAProxy, Prometheus, Grafana)
- Network Traffic
- HAProxy Traffic
- WireGuard
- Security (SSH brute force, web attacks, kernel panic)

### Визуализация
- 7 готовых дашбордов Grafana
- Infrastructure Overview (custom)
- Provisioning для автоматической настройки

## Быстрый старт

### Предварительные требования

- Docker 20.10+
- Docker Compose 2.0+
- Ubuntu 20.04/22.04 или Debian 11/12
- Минимум 4GB RAM (рекомендуется 8GB)
- 20GB свободного места

### Установка

```bash
# Клонируйте репозиторий
git clone https://github.com/YOUR_USERNAME/infrastructure-monitoring.git
cd infrastructure-monitoring

# Создайте external сеть для HAProxy
docker network create haproxy_proxy_network

# Настройте переменные окружения для Telegram
nano alertmanager/config/alertmanager.yml
# Замените <TELEGRAM_ADMIN_ID> и <TELEGRAM_BOT_TOKEN>

# Запустите стек
docker compose up -d
```

### Проверка

```bash
# Проверка статуса контейнеров
docker compose ps

# Проверка targets Prometheus (должно быть 9 UP)
curl -s http://localhost:9090/api/v1/targets | jq -r '.data.activeTargets[] | "\(.labels.job) - \(.health)"'

# Проверка Loki
curl -s http://localhost:3100/ready

# Проверка Alertmanager
curl -s http://localhost:9093/api/v2/status
```

## Доступ к сервисам

### Локальный доступ

| Сервис | URL | Описание |
|--------|-----|----------|
| Prometheus | http://localhost:9090 | Метрики и правила |
| Grafana | http://localhost:3200 | Дашборды (admin/admin) |
| Loki | http://localhost:3100 | API логов |
| Alertmanager | http://localhost:9093 | Управление алертами |

### Внешний доступ (через HAProxy)

Настройте HAProxy для проксирования на порт 4443 с базовой аутентификацией.

## Структура проекта

```
.
├── docker-compose.yml              # Основной манифест
├── prometheus/
│   ├── config/
│   │   └── prometheus.yml          # Конфигурация Prometheus
│   └── rules/
│       ├── resources.yml           # Алерты ресурсов (7)
│       └── traffic.yml             # Алерты трафика (15)
├── loki/
│   ├── config/
│   │   └── loki-config.yml         # Конфигурация Loki
│   └── rules/
│       └── fake/
│           └── security.yml        # Алерты безопасности (9)
├── promtail/
│   └── config/
│       └── promtail-config.yml     # Конфигурация Promtail с парсингом
├── alertmanager/
│   └── config/
│       └── alertmanager.yml        # Конфигурация Alertmanager
├── blackbox-exporter/
│   └── config/
│       └── blackbox.yml            # Конфигурация Blackbox
├── grafana/
│   └── provisioning/
│       ├── datasources/
│       │   └── datasources.yml     # Автоматическое подключение источников
│       └── dashboards/
│           └── dashboards.yml      # Автоматическая загрузка дашбордов
└── docs/
    ├── monitoring-stack-setup.md   # Полная инструкция
    ├── METRICS_EXPORTERS.md        # Настройка экспортеров
    ├── LOGS_LOKI_PROMTAIL.md       # Настройка логирования
    ├── ALERTS.md                   # Настройка алертов
    ├── GRAFANA_DASHBOARDS.md       # Работа с Grafana
    └── FINAL_SUMMARY.md            # Итоговая сводка
```

## Конфигурация

### Telegram бот

1. Создайте бота через @BotFather
2. Получите TOKEN
3. Получите свой TELEGRAM_ID через @userinfobot
4. Укажите в `docker-compose.yml`:
   ```yaml
   environment:
     - TELEGRAM_ADMIN=<YOUR_TELEGRAM_ID>
     - TELEGRAM_TOKEN=<YOUR_BOT_TOKEN>
   ```
5. Отправьте `/start` боту после запуска

### HAProxy Stats

Для работы HAProxy Exporter добавьте в `haproxy.cfg`:

```haproxy
frontend stats
    bind *:8404
    stats enable
    stats uri /stats
    stats refresh 10s
```

### Retention политики

По умолчанию:
- Prometheus: 30 дней
- Loki: 30 дней

Изменяется в соответствующих конфигах.

## Использование ресурсов

| Сервис | CPU | RAM | Disk |
|--------|-----|-----|------|
| Prometheus | ~2% | 400 MB | ~900 MB |
| Grafana | ~1% | 150 MB | ~136 MB |
| Loki | ~1% | 200 MB | ~104 MB |
| Promtail | ~1% | 50 MB | - |
| Exporters | <1% | 50 MB | - |
| **Итого** | ~5-10% | ~1 GB | ~1.2 GB |

## Troubleshooting

### Prometheus не собирает метрики

```bash
# Проверка targets
curl http://localhost:9090/api/v1/targets

# Перезагрузка конфигурации
docker exec prometheus kill -HUP 1

# Проверка правил
docker exec prometheus promtool check rules /etc/prometheus/rules/resources.yml
```

### Loki не принимает логи

```bash
# Проверка готовности
curl http://localhost:3100/ready

# Логи Promtail
docker logs promtail --tail=50

# Перезапуск
docker compose restart loki promtail
```

### Алерты не приходят в Telegram

```bash
# Проверка регистрации
docker logs alertmanager-telegram | grep "registered"

# Проверка переменных
docker exec alertmanager-telegram env | grep TELEGRAM

# Отправьте /start боту
```

## Мониторинг

Стек включает self-monitoring:
- Prometheus мониторит сам себя
- Алерты на недоступность критичных сервисов
- Метрики производительности всех компонентов

## Безопасность

**Production рекомендации:**

1. Смените пароли Grafana
2. Настройте HTTPS через HAProxy
3. Ограничьте доступ firewall:
   ```bash
   ufw allow 4443/tcp
   ufw deny 9090/tcp
   ufw deny 3200/tcp
   ```
4. Используйте secrets для токенов

## Документация

Полная документация находится в директории [docs/](docs/):
- [Развертывание стека](docs/monitoring-stack-setup.md)
- [Настройка экспортеров](docs/METRICS_EXPORTERS.md)
- [Логирование](docs/LOGS_LOKI_PROMTAIL.md)
- [Алерты](docs/ALERTS.md)
- [Grafana](docs/GRAFANA_DASHBOARDS.md)

## Лицензия

MIT License

## Автор

becausethatbee

## Поддержка

При возникновении проблем:
1. Проверьте [Troubleshooting](#troubleshooting)
2. Изучите документацию в `docs/`
3. Создайте Issue в репозитории
