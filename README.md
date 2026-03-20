[![Stand With Ukraine](https://raw.githubusercontent.com/vshymanskyy/StandWithUkraine/main/banner-direct-single.svg)](https://stand-with-ukraine.pp.ua)
[![Made in Ukraine](https://img.shields.io/badge/made_in-Ukraine-ffd700.svg?labelColor=0057b7)](https://stand-with-ukraine.pp.ua)
[![Stand With Ukraine](https://raw.githubusercontent.com/vshymanskyy/StandWithUkraine/main/badges/StandWithUkraine.svg)](https://stand-with-ukraine.pp.ua)
[![Russian Warship Go Fuck Yourself](https://raw.githubusercontent.com/vshymanskyy/StandWithUkraine/main/badges/RussianWarship.svg)](https://stand-with-ukraine.pp.ua)

# Customs Tax Calculator

This Django project provides a web-based customs tax calculator for calculating import taxes on parcels in Ukraine.

## Features

- Calculates customs taxes based on the price input.
- Supports both Euro and Dollar currencies with conversion rates.

## Django SECRET_KEY

The `SECRET_KEY` is used for cryptographic signing in Django and is critical for production security.

### How to generate it

Using Django's built-in utility:

```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

Or using Python's secrets module:

```python
import secrets
print(secrets.token_urlsafe(50))
```

### How to use it in Docker run

```bash
docker run -e SECRET_KEY=your_generated_secret_key -p 8000:8000 your_image
```

The SECRET_KEY is configured in `config/settings.py` using the `SECRET_KEY` environment variable. In DEBUG mode (development), it falls back to an insecure generated key. In production (DEBUG=False), the environment variable is required.

Do not forget to run with --init for SIGTERM to correctly forward to child processes.

[Amazon Userscript](userscripts/README.md)

## GitHub
https://github.com/ALERTua/import_tax_calculator
