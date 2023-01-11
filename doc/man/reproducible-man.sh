#!/usr/bin/env bash
# Ensure man pages are reproducible, as scdoc inserts the current date.
# This will be replaced with the current git commit.

# Verify that we can actually utilise git.
if command -v git &> /dev/null; then
  # Ensure that we are inside a git working tree.
  if git rev-parse --is-inside-work-tree > /dev/null 2>&1; then
    commit_date=$(git show --no-patch --format=%cd --date=format:%Y-%m-%d)
  else
    exit 0
  fi

  # Replace dates in all man pages.
  for page in ./*.1; do
    sed \
      -i "$page" \
      -e "s/\"[0-9]\{4\}-[0-9]\{2\}-[0-9]\{2\}\"/\"$commit_date\"/"
  done
fi
