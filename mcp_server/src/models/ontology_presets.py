"""Built-in ontology presets for Graphiti MCP Server."""

from dataclasses import dataclass

from pydantic import BaseModel, Field


class Gene(BaseModel):
    """A gene entity from a biological organism."""

    symbol: str | None = Field(None, description='HGNC gene symbol (e.g., BRCA1)')
    hgnc_id: str | None = Field(None, description='HGNC identifier (e.g., HGNC:1100)')
    ensembl_id: str | None = Field(None, description='Ensembl gene ID (e.g., ENSG00000012048)')
    entrez_id: str | None = Field(None, description='NCBI Entrez Gene ID')


class Protein(BaseModel):
    """A protein entity with structural and functional annotations."""

    uniprot_id: str | None = Field(None, description='UniProt accession (e.g., P38398)')
    protein_name: str | None = Field(None, description='Protein name')
    gene_symbol: str | None = Field(None, description='Associated gene symbol')


class DrugCompound(BaseModel):
    """A drug or compound entity with pharmacology metadata."""

    drug_name: str | None = Field(None, description='Drug or compound name')
    chembl_id: str | None = Field(None, description='ChEMBL compound ID (e.g., CHEMBL25)')
    drugbank_id: str | None = Field(None, description='DrugBank identifier')
    max_phase: int | None = Field(None, description='Highest clinical phase observed (0-4)')


class Disease(BaseModel):
    """A disease or phenotype entity."""

    disease_name: str | None = Field(None, description='Disease name')
    mondo_id: str | None = Field(None, description='MONDO disease identifier')
    efo_id: str | None = Field(None, description='EFO disease identifier')


class Pathway(BaseModel):
    """A biological pathway entity."""

    pathway_name: str | None = Field(None, description='Pathway name')
    wikipathways_id: str | None = Field(None, description='WikiPathways identifier (e.g., WP:WP534)')


class ClinicalTrial(BaseModel):
    """A clinical trial entity."""

    nct_id: str | None = Field(None, description='ClinicalTrials.gov identifier (e.g., NCT:00461032)')
    phase: str | None = Field(None, description='Clinical trial phase')
    status: str | None = Field(None, description='Recruitment or completion status')
    condition: str | None = Field(None, description='Primary disease/condition under study')


class Variant(BaseModel):
    """A genomic variant or mutation entity."""

    hgvs: str | None = Field(None, description='HGVS notation')
    gene_symbol: str | None = Field(None, description='Gene associated with the variant')
    protein_change: str | None = Field(None, description='Protein-level change (e.g., p.R175H)')


class Biomarker(BaseModel):
    """A predictive, prognostic, or pharmacodynamic biomarker entity."""

    biomarker_name: str | None = Field(None, description='Biomarker name')
    biomarker_type: str | None = Field(
        None,
        description='Biomarker class (predictive, prognostic, pharmacodynamic)',
    )
    assay: str | None = Field(None, description='Assay or test used to measure this biomarker')


class SyntheticLethalWith(BaseModel):
    """Synthetic lethal relationship between two entities, typically genes."""

    evidence_source: str | None = Field(None, description='Source of SL evidence')
    confidence_score: float | None = Field(None, description='Confidence score (0-1)')
    context: str | None = Field(None, description='Disease, lineage, or molecular context')


class Targets(BaseModel):
    """Drug-to-target relationship between a compound and a gene/protein."""

    mechanism: str | None = Field(None, description='Mechanism of action')
    potency_nm: float | None = Field(None, description='Potency value in nM when available')
    evidence_source: str | None = Field(None, description='Source supporting target linkage')


class InvestigatedIn(BaseModel):
    """Entity investigated in a clinical trial context."""

    nct_id: str | None = Field(None, description='ClinicalTrials.gov identifier')
    phase: str | None = Field(None, description='Clinical trial phase')
    status: str | None = Field(None, description='Trial status')


class TreatedBy(BaseModel):
    """Disease treated by a compound or intervention."""

    line_of_therapy: str | None = Field(None, description='Treatment line where known')
    evidence_source: str | None = Field(None, description='Source supporting treatment indication')


class InvolvedIn(BaseModel):
    """Gene/protein involvement in a pathway."""

    role: str | None = Field(None, description='Role in pathway (activator, component, regulator)')
    evidence_source: str | None = Field(None, description='Source supporting pathway membership')


class AssociatedWith(BaseModel):
    """General association between entities."""

    score: float | None = Field(None, description='Association strength score (0-1)')
    evidence_source: str | None = Field(None, description='Source supporting association')


class ConfersResistanceTo(BaseModel):
    """Variant or biomarker associated with treatment resistance."""

    resistance_mechanism: str | None = Field(None, description='Mechanistic explanation of resistance')
    evidence_source: str | None = Field(None, description='Source supporting resistance finding')


class BiomarkerFor(BaseModel):
    """Biomarker relationship for therapy selection or disease stratification."""

    biomarker_role: str | None = Field(None, description='Predictive/prognostic/monitoring role')
    evidence_source: str | None = Field(None, description='Source supporting biomarker use')


BIO_RESEARCH_ENTITY_TYPES: dict[str, type[BaseModel]] = {
    'Gene': Gene,
    'Protein': Protein,
    'DrugCompound': DrugCompound,
    'Disease': Disease,
    'Pathway': Pathway,
    'ClinicalTrial': ClinicalTrial,
    'Variant': Variant,
    'Biomarker': Biomarker,
}

BIO_RESEARCH_EDGE_TYPES: dict[str, type[BaseModel]] = {
    'SyntheticLethalWith': SyntheticLethalWith,
    'Targets': Targets,
    'InvestigatedIn': InvestigatedIn,
    'TreatedBy': TreatedBy,
    'InvolvedIn': InvolvedIn,
    'AssociatedWith': AssociatedWith,
    'ConfersResistanceTo': ConfersResistanceTo,
    'BiomarkerFor': BiomarkerFor,
}


def _add_symmetric_pairs(
    edge_map: dict[tuple[str, str], list[str]],
) -> dict[tuple[str, str], list[str]]:
    """Create symmetric entries for all edge mappings."""
    symmetric_map: dict[tuple[str, str], list[str]] = {}

    for (source, target), edge_types in edge_map.items():
        for pair in ((source, target), (target, source)):
            existing = symmetric_map.get(pair, [])
            merged = sorted(set(existing + edge_types))
            symmetric_map[pair] = merged

    return symmetric_map


BASE_BIO_RESEARCH_EDGE_TYPE_MAP: dict[tuple[str, str], list[str]] = {
    ('Gene', 'Gene'): ['SyntheticLethalWith', 'AssociatedWith'],
    ('Gene', 'Protein'): ['AssociatedWith'],
    ('DrugCompound', 'Gene'): ['Targets'],
    ('DrugCompound', 'Protein'): ['Targets'],
    ('Gene', 'Pathway'): ['InvolvedIn'],
    ('Protein', 'Pathway'): ['InvolvedIn'],
    ('Disease', 'DrugCompound'): ['TreatedBy', 'InvestigatedIn'],
    ('ClinicalTrial', 'DrugCompound'): ['InvestigatedIn'],
    ('ClinicalTrial', 'Disease'): ['InvestigatedIn'],
    ('ClinicalTrial', 'Gene'): ['AssociatedWith'],
    ('Variant', 'Gene'): ['AssociatedWith'],
    ('Variant', 'DrugCompound'): ['ConfersResistanceTo', 'BiomarkerFor'],
    ('Biomarker', 'Disease'): ['BiomarkerFor'],
    ('Biomarker', 'DrugCompound'): ['BiomarkerFor'],
    ('Entity', 'Entity'): ['AssociatedWith'],
}

BIO_RESEARCH_EDGE_TYPE_MAP = _add_symmetric_pairs(BASE_BIO_RESEARCH_EDGE_TYPE_MAP)


@dataclass(frozen=True)
class OntologyPreset:
    """Container for a built-in ontology preset."""

    entity_types: dict[str, type[BaseModel]]
    edge_types: dict[str, type[BaseModel]]
    edge_type_map: dict[tuple[str, str], list[str]]
    excluded_entity_types: list[str]


ONTOLOGY_PRESETS: dict[str, OntologyPreset] = {
    'biosciences': OntologyPreset(
        entity_types=BIO_RESEARCH_ENTITY_TYPES,
        edge_types=BIO_RESEARCH_EDGE_TYPES,
        edge_type_map=BIO_RESEARCH_EDGE_TYPE_MAP,
        excluded_entity_types=[],
    ),
}


def list_ontology_presets() -> list[str]:
    """Return names of built-in ontology presets."""
    return sorted(ONTOLOGY_PRESETS.keys())


def get_ontology_preset(name: str) -> OntologyPreset:
    """Get a built-in ontology preset by name."""
    preset = ONTOLOGY_PRESETS.get(name.lower())
    if preset is None:
        available = ', '.join(list_ontology_presets())
        raise ValueError(f'Unknown ontology preset "{name}". Available presets: {available}')
    return preset
