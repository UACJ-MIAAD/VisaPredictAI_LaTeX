"""Contrato de colocación de flotantes del maestro: ninguna figura, tabla o algoritmo aparece
antes del texto que la menciona por primera vez.

flafter impide que un flotante se coloque antes de su punto en el texto; basta entonces con que
cada entorno se escriba después de su primera referencia y que ninguno fuerce [H].
"""

from __future__ import annotations

import re
from pathlib import Path

TEX = Path(__file__).resolve().parents[1] / "reports/latex/ProyectoI_VisaPredictAI.tex"
FLOAT = r"(?:figure|table|algorithm)"


def _lines() -> list[str]:
    return [re.sub(r"(?<!\\)%.*", "", line) for line in TEX.read_text().split("\n")]


def _floats_and_first_refs(lines: list[str]) -> tuple[dict[str, int], dict[str, int]]:
    floats: dict[str, int] = {}
    refs: dict[str, int] = {}
    begin = None
    for n, line in enumerate(lines, 1):
        if re.search(rf"\\begin\{{{FLOAT}\}}", line):
            begin = n
        for label in re.findall(r"\\label\{((?:fig|tab|alg):[^}]+)\}", line):
            if begin is not None:
                floats.setdefault(label, begin)
        if re.search(rf"\\end\{{{FLOAT}\}}", line):
            begin = None
        for ref in re.findall(r"\\ref\*?\{((?:fig|tab|alg):[^}]+)\}", line):
            refs.setdefault(ref, n)
    return floats, refs


def test_flafter_is_loaded() -> None:
    assert any(re.match(r"\\usepackage\{flafter\}", line.strip()) for line in _lines())


# The EDA cites several large figures with little text between them; there (and in A.6) each float is pinned
# ([H]) right after the paragraph that cites it, so the queue cannot push them pages away.
PINNED = {
    "tab:eda_descriptiva", "fig:eda_panel", "fig:eda_completitud", "fig:backlog_f4", "fig:eda_spaghetti",
    "fig:eda_dist", "fig:eda_violin_c", "fig:eda_violin_cat", "fig:eda_retros", "fig:eda_season",
    "fig:eda_corr2", "fig:eda_brecha", "fig:eda_stl", "fig:eda_acf",
    # A.6 closes the document with two figures and no text between them: pinned, they share
    # pages with that text instead of being flushed one per page before the author page.
    "fig:eda_dv", "fig:grid_dff",
}


def test_only_the_eda_pins_floats_here() -> None:
    text = "\n".join(_lines())
    blocks = re.findall(rf"\\begin\{{({FLOAT})\}}\[([^\]]*)\](.*?)\\end\{{\1\}}", text, re.S)
    assert blocks
    pinned = {lab for _, spec, body in blocks if "H" in spec
              for lab in re.findall(r"\\label\{((?:fig|tab|alg):[^}]+)\}", body)}
    assert pinned == PINNED


def test_every_float_is_written_after_its_first_reference() -> None:
    floats, refs = _floats_and_first_refs(_lines())
    referenced = {k: v for k, v in floats.items() if k in refs}
    # A float may carry an alias label that is never cited; it still needs one cited label.
    assert set(floats.values()) == set(referenced.values())
    early = {k: (v, refs[k]) for k, v in referenced.items() if v < refs[k]}
    assert early == {}


def test_no_page_is_left_holding_a_lone_float() -> None:
    """A float page needs at least 85 % of the page filled, and the section barrier only turns the
    page: forcing \\clearpage emptied pending floats one per page."""
    text = "\n".join(_lines())
    fraction = re.search(r"\\renewcommand\{\\floatpagefraction\}\{([0-9.]+)\}", text)
    assert fraction and float(fraction.group(1)) >= 0.85
    barrier = re.search(r"\\newcommand\{\\barreraflotantes\}\{(.*?)\n\\makeatother", text, re.S)
    assert barrier and "\\clearpage" not in barrier.group(1)
