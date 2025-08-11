#!/bin/bash
# wait-for-mysql.sh

set -e

host="$1"
port="$2"
user="$3"
password="$4"

until mysql -h"$host" -P"$port" -u"$user" -p"$password" -e "SELECT 1" &> /dev/null; do
  >&2 echo "MySQL is unavailable - sleeping"
  sleep 1
done

>&2 echo "MySQL is up - executing command"
exec "${@:5}"
