#!/bin/bash
# Check if all phases in docs/planning/phased-plan.md are complete
# Always exits 0 — uses stdout for status reporting

PLAN_DIR="docs/planning"
PLAN_FILE="${PLAN_DIR}/phased-plan.md"

if [ ! -f "$PLAN_FILE" ]; then
    echo "[bo-planner] No phased-plan.md found — no active planning session."
    exit 0
fi

TOTAL=$(grep -c "### Phase\|^| [0-9]" "$PLAN_FILE" || true)
COMPLETE=$(grep -cF "complete" "$PLAN_FILE" || true)
IN_PROGRESS=$(grep -cF "in_progress" "$PLAN_FILE" || true)
PENDING=$(grep -cF "pending" "$PLAN_FILE" || true)

: "${TOTAL:=0}"
: "${COMPLETE:=0}"
: "${IN_PROGRESS:=0}"
: "${PENDING:=0}"

# Check for phase plans without verification
UNVERIFIED=0
for f in "$PLAN_DIR"/phase-*-plan.md; do
    [ -f "$f" ] || continue
    if grep -qF "**Status:** complete" "$f" 2>/dev/null; then
        if ! grep -A2 "## Verification" "$f" | grep -q "\[x\]" 2>/dev/null; then
            UNVERIFIED=$((UNVERIFIED + 1))
        fi
    fi
done

if [ "$COMPLETE" -eq "$TOTAL" ] && [ "$TOTAL" -gt 0 ]; then
    echo "[bo-planner] ALL PHASES COMPLETE ($COMPLETE/$TOTAL)"
    if [ "$UNVERIFIED" -gt 0 ]; then
        echo "[bo-planner] WARNING: $UNVERIFIED phase(s) complete but verification not documented."
    fi
else
    echo "[bo-planner] Task in progress ($COMPLETE/$TOTAL phases complete)"
    [ "$IN_PROGRESS" -gt 0 ] && echo "[bo-planner] $IN_PROGRESS phase(s) in progress."
    [ "$PENDING" -gt 0 ] && echo "[bo-planner] $PENDING phase(s) pending."
fi

# Check scope fence exists
if ! grep -q "### IN Scope" "$PLAN_FILE" 2>/dev/null; then
    echo "[bo-planner] WARNING: No scope fence found in phased-plan.md"
fi

exit 0
