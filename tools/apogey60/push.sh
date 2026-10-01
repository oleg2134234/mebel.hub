#!/bin/bash
cd C:/Temp/claude/pub
git fetch -q origin
git rebase -q origin/main 2>&1 | tail -1
git push -q origin HEAD:main 2>&1 | tail -1
git log --oneline origin/main -1
