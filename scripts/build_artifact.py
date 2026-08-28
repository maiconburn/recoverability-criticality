"""Assemble the validation report artifact (inlines figures as data URIs)."""

import base64
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIGURES = ROOT / "results" / "figures"
OUT = Path(
    "/private/tmp/claude-501/-Users-maiconesteves-fisica/"
    "0f1bdd7e-c08f-4678-b0c9-cdfea8c8af0d/scratchpad/lei-complexidade-critica.html"
)


def uri(name: str) -> str:
    payload = base64.b64encode((FIGURES / name).read_bytes()).decode()
    return f"data:image/png;base64,{payload}"


template = (ROOT / "scripts" / "artifact_template.html").read_text()
for key, filename in (
    ("FIG1", "fig1_channels.png"),
    ("FIG2", "fig2_rate_halving.png"),
    ("FIG3", "fig3_distance.png"),
    ("FIG4", "fig4_collapse.png"),
    ("FIG5", "fig5_complexity.png"),
):
    template = template.replace("{{" + key + "}}", uri(filename))

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(template)
print(f"wrote {OUT} ({OUT.stat().st_size/1024:.0f} KB)")
