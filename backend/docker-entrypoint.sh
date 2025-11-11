#!/bin/bash
set -e
if [ "$1" = 'worker' ]; then
  # Start a simple loop to simulate a worker (replace with celery in production)
  echo "Starting worker (stub)..."
  python -u -c "import time; print('Worker running'); time.sleep(3600)"
else
  exec "$@"
fi
