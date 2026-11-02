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
        for ref in re.findall(r"\\ref\{((?:fig|tab|alg):[^}]+)\}", line):
            refs.setdefault(ref, n)
    return floats, refs


def test_flafter_is_loaded() -> None:
    assert any(re.match(r"\\usepackage\{flafter\}", line.strip()) for line in _lines())


def test_no_float_forces_here() -> None:
    specs = re.findall(rf"\\begin\{{{FLOAT}\}}\[([^\]]*)\]", "\n".join(_lines()))
    assert specs and all("H" not in s for s in specs)


def test_every_float_is_written_after_its_first_reference() -> None:
    floats, refs = _floats_and_first_refs(_lines())
    referenced = {k: v for k, v in floats.items() if k in refs}
    # A float may carry an alias label that is never cited; it still needs one cited label.
    assert set(floats.values()) == set(referenced.values())
    early = {k: (v, refs[k]) for k, v in referenced.items() if v < refs[k]}
    assert early == {}
