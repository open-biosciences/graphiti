"""Tests for built-in ontology presets."""

import pytest

from config.schema import GraphitiAppConfig
from models.ontology_presets import get_ontology_preset


def test_biosciences_preset_contains_trial_and_sl_types():
    """Biosciences preset includes SL + trial entities/edges and symmetric mapping."""
    preset = get_ontology_preset('biosciences')

    assert 'ClinicalTrial' in preset.entity_types
    assert 'SyntheticLethalWith' in preset.edge_types
    assert 'InvestigatedIn' in preset.edge_types

    # Symmetric mapping checks
    assert ('DrugCompound', 'ClinicalTrial') in preset.edge_type_map
    assert ('ClinicalTrial', 'DrugCompound') in preset.edge_type_map
    assert ('Gene', 'Gene') in preset.edge_type_map
    assert ('Entity', 'Entity') in preset.edge_type_map


def test_unknown_preset_raises_helpful_error():
    """Unknown preset names return a clear error."""
    with pytest.raises(ValueError, match='Unknown ontology preset'):
        get_ontology_preset('not-a-real-preset')


def test_graphiti_app_config_accepts_ontology_preset():
    """Configuration schema includes ontology_preset."""
    cfg = GraphitiAppConfig(ontology_preset='biosciences')
    assert cfg.ontology_preset == 'biosciences'
