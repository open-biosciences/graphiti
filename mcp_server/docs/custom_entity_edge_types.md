# Custom Entity and Edge Types (MCP Server)

This guide shows how to configure custom ontology types in Graphiti MCP Server and ingest episodes with them.

## What Is Supported

The MCP server now supports:

- `graphiti.ontology_preset` (built-in preset: `biosciences`)
- `graphiti.entity_types`
- `graphiti.edge_types`
- `graphiti.edge_type_map`
- `graphiti.excluded_entity_types` (optional)

These are passed through to Graphiti core `add_episode(...)` during `add_memory`.

## Built-in Biosciences Preset

To enable the built-in biosciences preset:

```yaml
graphiti:
  ontology_preset: biosciences
  group_id: bio-research-main
```

The preset includes trial/SL-specific ontology:

- Entities: `Gene`, `Protein`, `DrugCompound`, `Disease`, `Pathway`, `ClinicalTrial`, `Variant`, `Biomarker`
- Edges: `SyntheticLethalWith`, `Targets`, `InvestigatedIn`, `TreatedBy`, `InvolvedIn`, `AssociatedWith`, `ConfersResistanceTo`, `BiomarkerFor`
- Symmetric edge map entries for directional pairs

## 1) Configure `config.yaml`

Use `mcp_server/config/config.yaml`:

```yaml
graphiti:
  group_id: custom-ontology-demo

  entity_types:
    - name: Person
      description: A person entity with biographical information.
      fields:
        - name: age
          type: int
          description: Age in years
        - name: occupation
          type: string
          description: Current occupation
        - name: birth_date
          type: datetime
          description: Date of birth

    - name: Company
      description: A business organization.
      fields:
        - name: industry
          type: string
          description: Primary industry
        - name: founded_year
          type: int
          description: Year company was founded

  edge_types:
    - name: Employment
      description: Employment relationship between a person and company.
      fields:
        - name: position
          type: string
          description: Job title
        - name: start_date
          type: datetime
          description: Employment start date
        - name: salary
          type: float
          description: Annual salary in USD
        - name: is_current
          type: bool
          description: Whether employment is current

    - name: Partnership
      description: Partnership relationship between companies.
      fields:
        - name: partnership_type
          type: string
          description: Type of partnership
        - name: deal_value
          type: float
          description: Deal value in USD

  edge_type_map:
    - source: Person
      target: Company
      edge_types: [Employment]
    - source: Company
      target: Company
      edge_types: [Partnership]
    - source: Entity
      target: Entity
      edge_types: [Partnership]

  excluded_entity_types: []
```

If `edge_types` is configured but `edge_type_map` is omitted, the server uses:

```python
{('Entity', 'Entity'): [all_custom_edge_type_names]}
```

## 2) Start MCP Server

```bash
cd /home/donbr/open-biosciences/graphiti/mcp_server
uv sync
uv run graphiti_mcp_server.py --transport http
```

Default endpoint:

- `http://localhost:8000/mcp`

## 3) Add an Episode Through MCP

Example JSON-RPC call:

```bash
curl -sS http://localhost:8000/mcp \
  -H 'Content-Type: application/json' \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
      "name": "add_memory",
      "arguments": {
        "name": "Business Update",
        "episode_body": "Sarah joined TechCorp as CTO in January 2023 with a $200K salary. TechCorp partnered with DataCorp in a $5M deal.",
        "group_id": "custom-ontology-demo",
        "source": "text",
        "source_description": "business news"
      }
    }
  }'
```

## 4) Query Results

- `search_nodes` supports filtering by entity label via the `entity_types` argument.
- `search_memory_facts` can be used for relationship/fact retrieval by query text.

For direct edge-type filtering, use Graphiti core `search_` with `SearchFilters(edge_types=[...])`.

## Supported Field Types

- `string`, `str`, `text`
- `int`, `integer`
- `float`
- `bool`, `boolean`
- `datetime`
- `date`
- `dict`, `object`
- `list[T]` (example: `list[string]`, `list[int]`)

## Protected Entity Field Names

Do not use these names in custom entity `fields`:

- `uuid`
- `name`
- `group_id`
- `labels`
- `created_at`
- `summary`
- `attributes`
- `name_embedding`

If one is used, ingestion fails during ontology validation.
