#!/bin/bash
set -e

host="$1"
shift
cmd="$@"

echo "Waiting for Postgres ($host) to be ready..."
until pg_isready -h "$host" -U "postgres"; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 3
done

>&2 echo "Postgres is up - executing command"
exec $cmd