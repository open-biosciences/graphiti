# Graphiti MCP Server: Biosciences Ontology Preset

This document is fork-specific to `open-biosciences/graphiti`.

It describes how to run the MCP server with the built-in `biosciences` ontology preset, including trial and synthetic-lethality (SL) relationship types.

## Why This Exists

The main [`README.md`](README.md) keeps generic custom ontology examples (for example `Person`/`Company`).

This file captures biosciences-specific configuration and usage for research workflows.

## Enable the Biosciences Preset

Use either config or environment variable:

```yaml
graphiti:
  group_id: "bio-research-main"
  ontology_preset: "biosciences"
```

or

```bash
export GRAPHITI_ONTOLOGY_PRESET=biosciences
```

Then start the server from `mcp_server/`:

```bash
uv sync
uv run graphiti_mcp_server.py --transport http
```

## Included Biosciences Types

Entity types:

- `Gene`
- `Protein`
- `DrugCompound`
- `Disease`
- `Pathway`
- `ClinicalTrial`
- `Variant`
- `Biomarker`

Edge types:

- `SyntheticLethalWith`
- `Targets`
- `InvestigatedIn`
- `TreatedBy`
- `InvolvedIn`
- `AssociatedWith`
- `ConfersResistanceTo`
- `BiomarkerFor`

## Symmetric Edge Maps

The preset defines base mappings and generates symmetric pairs automatically where directionality should be mirrored.

Example: both `DrugCompound -> ClinicalTrial` and `ClinicalTrial -> DrugCompound` are mapped.

This is implemented in:

- [`src/models/ontology_presets.py`](src/models/ontology_presets.py)

## Overriding or Extending the Preset

You can combine the preset with explicit config overrides:

- `graphiti.entity_types`
- `graphiti.edge_types`
- `graphiti.edge_type_map`
- `graphiti.excluded_entity_types`

Config-defined values are merged on top of preset defaults.

## Validation Constraints

Protected entity field names are not allowed:

- `uuid`
- `name`
- `group_id`
- `labels`
- `created_at`
- `summary`
- `attributes`
- `name_embedding`

Using these fields in ontology definitions causes ingestion validation failures.

## Suggested Namespace Pattern

Use one `group_id` per experiment/workspace run for clean isolation:

- `exp_<slug>_<YYYYMMDD>`

Example:

- `exp_cq14edgefix_20260305`

