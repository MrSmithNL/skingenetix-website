#!/bin/bash
# Run the five held waves SEQUENTIALLY. No pgrep-based waiting: chaining on
# `pgrep -f "generate-multi.py"` deadlocked yesterday because the watcher's own command line
# contains that string, so it waited on itself forever. Sequential execution needs no watcher.
cd "/Users/malcolmsmith/Claude Code/Projects/skingenetix-website"
set -a; source ~/.claude/config/image-credentials.env; set +a
python3 -c "import os; print('credentials visible to python:', {k: bool(os.environ.get(k)) for k in ('FAL_KEY','OPENAI_API_KEY','GEMINI_API_KEY')})"

run () {
  echo ""
  echo "=============================================================="
  echo "=== $1   started $(date +%H:%M:%S)"
  echo "=============================================================="
  python3 scripts/generate-multi.py "configs/banners/$1.json" --suppliers "$2" --candidates 2
  echo "=== $1 finished $(date +%H:%M:%S)"
}

# flux2 is included for the cream macros: generate-multi skips it automatically on the six
# referenced slots and runs it only on the three macro-only ones, which is the material it is
# good at. The dropper faces carry no reference at all, so flux2 runs on every slot there.
run matrixyl-cream-macros      seedream,gpt_image,nbp_pro,nbp_flash,flux2
run copper-day-cream-macros    seedream,gpt_image,nbp_pro,nbp_flash,flux2
run copper-night-cream-macros  seedream,gpt_image,nbp_pro,nbp_flash,flux2
run pdrn-cream-macros          seedream,gpt_image,nbp_pro,nbp_flash,flux2
run serum-dropper-faces        seedream,gpt_image,nbp_pro,nbp_flash,flux2

echo ""
echo "=== ALL FIVE WAVES DONE $(date +%H:%M:%S) ==="
for w in matrixyl copper-day copper-night pdrn serum-dropper; do
  d=$(ls -d assets/ai-generated/*${w}-cream-macros* assets/ai-generated/*${w}-faces* 2>/dev/null | head -1)
  [ -n "$d" ] && echo "  $(basename $d): $(find "$d" -name '*.png' | wc -l | tr -d ' ') tiles, manifest=$([ -f "$d/manifest.json" ] && echo yes || echo NO)"
done
