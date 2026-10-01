#!/bin/bash
# usage: pub.sh localId
cd /c/Temp/claude/work
node addcard.mjs $1 C:/Temp/claude/work/gen/$1.jpg || exit 1
t=$(node -e 'const c=require("./cards.json").find(x=>x.localId==process.argv[1]);console.log(c.title+"|"+c.slug)' $1)
title=${t%|*}; slug=${t#*|}
cd C:/Temp/claude/pub
git add index.html assets/$slug
git commit -q -m "Добавить карточку $title

Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>"
git log --oneline -1
