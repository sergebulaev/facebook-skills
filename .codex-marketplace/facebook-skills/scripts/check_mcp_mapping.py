#!/usr/bin/env python3
"""The documented MCP read path must match the library it replaces.

A skill reading through the Apify connector gets the actor's raw output and has
only `references/mcp-read-layer.md` to turn it into the records every other
skill expects. If that document drifts from the client, the connector path
starts producing a second, subtly different contract: same field names, one of
them silently absent or fed from the wrong place. Nothing at runtime would
notice, because both shapes are plain dicts.

So it is checked rather than trusted. Three things must agree with the code:
the actor ids, every input key the client sends, and every flat field the
normalizer produces.

Run from the repo root:

    python3 scripts/check_mcp_mapping.py
"""
import ast
import importlib
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

DOC = ROOT / "references" / "mcp-read-layer.md"
CLIENT = ROOT / "lib" / "apify_client.py"
#: (module, attribute) of every function that flattens an actor row.
NORMALIZERS = (("lib.apify_client", "_page_stats"), ("lib.apify_client", "_comment"))
#: Input keys that are near-misses, documented so nobody sends them again.
WARN_ABOUT = ("max_comments",)


def mentions(doc: str, name: str, extra: str = "") -> bool:
    """A name counts as documented only as a whole word.

    `name not in doc` is satisfied by any longer name containing it, so
    queryTypeX would silently pass for queryType. Actor ids need `extra` to
    cover the characters they are allowed to contain, or a rename to
    actor-name-v2 passes as actor-name.
    """
    char = "A-Za-z0-9_" + extra
    return re.search(rf"(?<![{char}]){re.escape(name)}(?![{char}])", doc) is not None


def actor_ids(tree: ast.AST) -> set[str]:
    """Every string constant in the client that looks like an actor id."""
    found = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            if re.fullmatch(r"[A-Za-z0-9_.-]+~[A-Za-z0-9_.-]+", node.value):
                found.add(node.value.replace("~", "/"))
    return found


def payload_keys(tree: ast.AST) -> set[str]:
    """Keys of every literal dict passed to the actor-running helper."""
    keys = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        name = getattr(node.func, "attr", getattr(node.func, "id", ""))
        if name not in ("_run", "_run_sync"):
            continue
        for arg in node.args:
            if isinstance(arg, ast.Dict):
                keys |= {k.value for k in arg.keys
                         if isinstance(k, ast.Constant) and isinstance(k.value, str)}
    return keys


def per_normalizer_fields() -> list[tuple[str, set[str]]]:
    out = []
    for module_name, attr in NORMALIZERS:
        module = importlib.import_module(module_name)
        produced = getattr(module, attr)({})
        out.append((attr, {k for k in produced if not k.startswith("_")}))
    return out


def flat_fields() -> set[str]:
    fields = set()
    for _, produced in per_normalizer_fields():
        fields |= produced
    return fields


def table_for(doc: str, attr: str) -> set[str] | None:
    """Fields of the mapping table that the prose attributes to `attr`.

    Matching by name is what makes the check precise: when one shape's fields
    are a superset of another's, a "some table covers it" test passes even
    after a row is deleted from the right one. Each table must be introduced
    with the normalizer it belongs to, e.g. "what `_profile_post` produces".
    """
    marker = re.search(r"`" + re.escape(attr) + r"`", doc)
    if not marker:
        return None
    after = doc[marker.end():]
    if "| Flat field |" not in after:
        return None
    body = after.split("| Flat field |", 1)[1].split(chr(10) * 2, 1)[0]
    return set(re.findall(r"^\| `([a-z_][a-z0-9_]*)` \|", body, re.M))


def mapping_tables(doc: str) -> list[set[str]]:
    """Field sets of every `| Flat field |` table in the document.

    Checked per table, not across the whole file: with two shapes that share
    field names, dropping a row from one table still leaves the name present
    somewhere else, and a whole-document check would pass.
    """
    tables = []
    for chunk in doc.split("| Flat field |")[1:]:
        body = chunk.split(chr(10) * 2, 1)[0]   # to the blank line after the table
        tables.append(set(re.findall(r"^\| `([a-z_][a-z0-9_]*)` \|", body, re.M)))
    return tables


def main() -> int:
    problems = []

    if not DOC.is_file():
        print(f"{DOC.relative_to(ROOT)} is missing; the connector path is undocumented.")
        return 1
    doc = DOC.read_text(encoding="utf-8")
    tree = ast.parse(CLIENT.read_text(encoding="utf-8"))

    for actor in sorted(actor_ids(tree)):
        if not mentions(doc, actor, extra=r"./\-"):
            problems.append(f"actor {actor} is called by the client and absent from the doc")

    keys = payload_keys(tree)
    if not keys:
        problems.append("no literal actor payload found in the client: has it changed shape?")
    for key in sorted(keys):
        if not mentions(doc, key):
            problems.append(f"input key `{key}` is sent by the client and undocumented")

    for key in sorted(WARN_ABOUT):
        if not mentions(doc, key):
            problems.append(f"the doc does not warn about `{key}`, which is ignored and bills a run")

    fields = flat_fields()
    if len(fields) < 5:
        problems.append("the normalizer produced almost nothing: wrong attribute?")
    for field in sorted(fields):
        if not re.search(r"`" + re.escape(field) + r"`", doc):
            problems.append(f"flat field `{field}` is produced by the client and undocumented")

    tables = mapping_tables(doc)
    known = set().union(*tables) if tables else set()
    for field in sorted(known - fields):
        problems.append(f"a mapping table documents `{field}`, which the client never produces")

    for attr, produced in per_normalizer_fields():
        own = table_for(doc, attr)
        if own is None:
            problems.append(
                f"the doc never names {attr} before a mapping table, so there is no way to "
                f"tell which table is its contract")
            continue
        missing = sorted(produced - own)
        if missing:
            problems.append(f"the table documented for {attr} is missing: {', '.join(missing)}")
        extra = sorted(own - produced)
        if extra:
            problems.append(f"the table documented for {attr} adds fields it never produces: {', '.join(extra)}")

    if "mcp.apify.com?actors=" not in doc:
        problems.append("the doc does not give the filtered connector URL")
    if "call-actor" not in doc:
        problems.append("the doc does not explain why the bare server is not the one to use")

    if problems:
        print("MCP read-layer mapping:\n" + "\n".join("  " + p for p in problems))
        return 1

    print(f"OK: {len(actor_ids(tree))} actor(s), {len(keys)} input key(s) and "
          f"{len(fields)} flat field(s) all documented in references/mcp-read-layer.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
