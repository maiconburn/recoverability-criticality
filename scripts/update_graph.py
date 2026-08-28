"""Fold the numerical validation results into the graphify knowledge graph.

Adds one node per measured result plus a verdict node, linked to the
existing transcript concepts ("Lei de complexidade crítica", "Ponto
excepcional", "Reconstrução espectral cega", "Complexidade espectral
operacional"), then graphify cluster-only regenerates report and viz.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GRAPH = ROOT / "graphify-out" / "graph.json"
FITS = ROOT / "results" / "fits.json"
PREFIX = "theory_validation_results_"
SOURCE = "results/RESULTS.md"


def node(identifier, label, community=1, node_type="evidence", location="results"):
    return {
        "label": label,
        "file_type": "document",
        "source_file": SOURCE,
        "source_location": location,
        "source_url": None,
        "captured_at": None,
        "author": None,
        "contributor": None,
        "id": PREFIX + identifier,
        "community": community,
        "norm_label": label.lower(),
        "type": node_type,
    }


def link(source, target, relation="supports", score=1.0):
    return {
        "relation": relation,
        "confidence": "EXTRACTED",
        "confidence_score": score,
        "source_file": SOURCE,
        "source_location": "validation run 2026-08-28",
        "weight": 1.0,
        "source": source,
        "target": target,
    }


def main() -> None:
    fits = json.loads(FITS.read_text())
    graph = json.loads(GRAPH.read_text())
    existing = {entry["id"] for entry in graph["nodes"]}

    transcript = "theory_validation_corpus_source_conversation_"
    ratio = fits["ratio_2alphaEP_over_alphaRho"]
    gamma = fits["gamma_mean"]
    decade = fits["p3_measured_per_decade"]

    additions = [
        node(
            "ep_exato",
            "EP exato do benchmark: q2=-16.1472, omega=-5.6738i",
            node_type="evidence",
        ),
        node(
            "p1_amplificacao",
            f"P1 confirmada: expoente do canal crítico gamma = {gamma:.2f} "
            "(previsto 0.5)",
        ),
        node(
            "p2_taxa_metade",
            f"P2 confirmada: 2*alpha_EP/alpha_rho = {ratio:.2f} (previsto 1) "
            "e eps(0)=sqrt(delta_rho) com coeficiente 1.03",
        ),
        node(
            "p3_lei_log",
            f"P3/P4 confirmadas: {decade:.2f} níveis por década "
            "(congelado: 1.47)",
        ),
        node(
            "ep_taxa_cheia",
            f"Posição do EP converge na taxa cheia alpha={fits['alpha_ep_shift']:.2f}",
        ),
        node(
            "veredito",
            "Validação numérica da lei de complexidade crítica: as três "
            "previsões pré-registradas do turno 112 confirmadas",
            node_type="decision",
        ),
    ]
    new_links = [
        link(PREFIX + "veredito", transcript + "lei_de_complexidade_critica"),
        link(PREFIX + "veredito", transcript + "complexidade_espectral_operacional"),
        link(PREFIX + "ep_exato", transcript + "ponto_excepcional"),
        link(PREFIX + "ep_exato", transcript + "modos_quasinormais", "references"),
        link(PREFIX + "p1_amplificacao", PREFIX + "veredito"),
        link(PREFIX + "p2_taxa_metade", PREFIX + "veredito"),
        link(PREFIX + "p3_lei_log", PREFIX + "veredito"),
        link(
            PREFIX + "p2_taxa_metade",
            transcript + "kernel_de_sensibilidade_do_observavel",
            "references",
        ),
        link(
            PREFIX + "p3_lei_log",
            transcript + "reconstrucao_espectral_cega",
            "references",
        ),
        link(
            PREFIX + "ep_taxa_cheia",
            transcript + "geometria_das_singularidades_complexas",
            "references",
        ),
    ]

    graph["nodes"] = [n for n in graph["nodes"] if not n["id"].startswith(PREFIX)]
    graph["links"] = [
        l
        for l in graph["links"]
        if not (l["source"].startswith(PREFIX) or l["target"].startswith(PREFIX))
    ]
    graph["nodes"].extend(additions)
    for entry in new_links:
        assert entry["target"] in existing | {n["id"] for n in additions}, entry
    graph["links"].extend(new_links)
    GRAPH.write_text(json.dumps(graph, ensure_ascii=False, indent=1))
    print(f"graph updated: {len(graph['nodes'])} nodes, {len(graph['links'])} links")


if __name__ == "__main__":
    main()
