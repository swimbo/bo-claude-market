#!/usr/bin/env bash
# find-plans.sh — Auto-discover plan files from bo-planner and deep-plan output locations
# Usage: bash find-plans.sh [project_root]
# Output: One plan file path per line, most relevant first

set -euo pipefail

PROJECT_ROOT="${1:-.}"

found=()

# --- bo-planner: docs/planning/phased-plan.md ---
BO_PLAN="$PROJECT_ROOT/docs/planning/phased-plan.md"
if [[ -f "$BO_PLAN" ]]; then
  found+=("$BO_PLAN")
  # Also collect phase files
  for phase in "$PROJECT_ROOT"/docs/planning/phase-*-plan.md; do
    [[ -f "$phase" ]] && found+=("$phase")
  done
  # Architecture doc if present
  [[ -f "$PROJECT_ROOT/docs/planning/architecture.md" ]] && found+=("$PROJECT_ROOT/docs/planning/architecture.md")
fi

# --- deep-plan: locate deep_plan_config.json, read planning_dir ---
while IFS= read -r config_file; do
  planning_dir=$(python3 -c "
import json, os, sys
try:
    with open('$config_file') as f:
        cfg = json.load(f)
    pd = cfg.get('planning_dir', '')
    if not os.path.isabs(pd):
        pd = os.path.join(os.path.dirname('$config_file'), pd)
    print(os.path.normpath(pd))
except Exception:
    sys.exit(1)
" 2>/dev/null) || continue

  # Main plan file
  if [[ -d "$planning_dir" ]]; then
    [[ -f "$planning_dir/claude-plan.md" ]] && found+=("$planning_dir/claude-plan.md")
    [[ -f "$planning_dir/claude-spec.md" ]] && found+=("$planning_dir/claude-spec.md")
    # Section files
    if [[ -d "$planning_dir/sections" ]]; then
      for section in "$planning_dir"/sections/section-*.md; do
        [[ -f "$section" ]] && found+=("$section")
      done
    fi
  fi
done < <(find "$PROJECT_ROOT" -maxdepth 3 -name "deep_plan_config.json" -not -path "*/node_modules/*" -not -path "*/.git/*" 2>/dev/null)

# --- Fallback: common plan file patterns ---
if [[ ${#found[@]} -eq 0 ]]; then
  for pattern in "PLAN.md" "plan.md" "IMPLEMENTATION_PLAN.md" "implementation-plan.md" "ARCHITECTURE.md"; do
    for f in $(find "$PROJECT_ROOT" -maxdepth 3 -name "$pattern" -not -path "*/node_modules/*" -not -path "*/.git/*" 2>/dev/null); do
      found+=("$f")
    done
  done
fi

# Deduplicate and output
if [[ ${#found[@]} -eq 0 ]]; then
  echo "NO_PLANS_FOUND" >&2
  exit 1
fi

printf '%s\n' "${found[@]}" | awk '!seen[$0]++'
