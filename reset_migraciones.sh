#!/bin/bash

echo "🧨 BORRANDO MIGRACIONES..."
for app in contrato empleado liquidacion; do
  find "$app/migrations" -type f -name "*.py" ! -name "__init__.py" -delete
done

echo "🧹 BORRANDO __pycache__ Y .pyc..."
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type f -name "*.pyc" -delete

echo "🧱 RECONSTRUYENDO MIGRACIONES..."
python manage.py makemigrations contrato
python manage.py makemigrations empleado
python manage.py makemigrations liquidacion

echo "📦 APLICANDO MIGRACIONES..."
python manage.py migrate

echo "✅ LISTO!!!"
