#!/usr/bin/env bash
# Синхронизация репозитория между двумя компьютерами.
#   ./sync.sh start            — подтянуть изменения перед работой
#   ./sync.sh end "что сделал" — закоммитить и отправить
set -euo pipefail
cd "$(dirname "$0")"

action="${1:-}"

case "$action" in
  start)
    echo "-> git pull --rebase --autostash"
    git pull --rebase --autostash || {
      echo "pull не прошёл. Разреши конфликт, затем: git rebase --continue" >&2
      exit 1
    }
    echo "Готово. Репозиторий актуален — можно работать."
    ;;

  end)
    shift || true
    msg="$*"
    [ -n "$msg" ] || msg="update $(date '+%Y-%m-%d %H:%M')"

    git add -A
    if git diff --cached --quiet; then
      echo "Новых изменений нет — проверю неотправленные коммиты."
    else
      echo "-> commit: $msg"
      git commit -m "$msg"
    fi

    echo "-> git pull --rebase --autostash"
    git pull --rebase --autostash || {
      echo "pull перед push не прошёл. Разреши конфликт, затем снова: ./sync.sh end" >&2
      exit 1
    }

    echo "-> git push"
    git push

    echo "Отправлено. На другой машине в начале работы: ./sync.sh start"
    ;;

  *)
    echo "Использование:"
    echo "  ./sync.sh start            — подтянуть изменения перед работой"
    echo "  ./sync.sh end \"что сделал\" — закоммитить и отправить"
    exit 0
    ;;
esac
