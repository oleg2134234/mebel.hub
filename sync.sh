#!/usr/bin/env bash
# Синхронизация репозитория между двумя компьютерами.
#   ./sync.sh start            — подтянуть изменения перед работой
#   ./sync.sh end "что сделал" — бэкап + коммит + отправка
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

    # 1. Бэкап исходников перед отправкой — быстрый офлайн-откат.
    #    Медиа не архивируем (тяжёлое, меняется редко) — их откат через git.
    #    См. CLAUDE.md → «Откат обновлений».
    mkdir -p backups
    zip_name="backups/source_$(date '+%Y-%m-%d_%H%M').zip"
    include=(index.html CLAUDE.md .gitattributes .gitignore sync.ps1 sync.sh tools assets/fonts assets/brand)
    present=()
    for p in "${include[@]}"; do [ -e "$p" ] && present+=("$p"); done
    if command -v zip >/dev/null 2>&1; then
      rm -f "$zip_name"
      zip -q -r "$zip_name" "${present[@]}"
    else
      tar -czf "${zip_name%.zip}.tgz" "${present[@]}"
      zip_name="${zip_name%.zip}.tgz"
    fi
    echo "-> бэкап: $zip_name"
    ls -1t backups/source_* 2>/dev/null | tail -n +16 | xargs -r rm -f

    # 2. Коммит.
    git add -A
    if git diff --cached --quiet; then
      echo "Новых изменений нет — проверю неотправленные коммиты."
    else
      echo "-> commit: $msg"
      git commit -m "$msg"
    fi

    # 3. Подтянуть чужое и отправить.
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
    echo "  ./sync.sh end \"что сделал\" — бэкап + коммит + отправка"
    exit 0
    ;;
esac
