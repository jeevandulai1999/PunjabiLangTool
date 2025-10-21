"""Tests for scenario service"""
import pytest

from backend.models.scenario import CustomScenario
from backend.services.scenario_service import (
    CURATED_SCENARIOS,
    get_scenario_service,
)


class TestScenarioService:
    """Test ScenarioService"""
    
    def test_get_curated_scenario(self):
        """Test retrieving a curated scenario"""
        service = get_scenario_service()
        
        # Get market shopping scenario
        scenario = service.get_scenario("market_shopping")
        
        assert scenario is not None
        assert scenario.id == "market_shopping"
        assert scenario.title == "Shopping at the Market"
        assert scenario.dialect == "doabi"
        assert len(scenario.goals) > 0
    
    def test_list_scenarios(self):
        """Test listing all scenarios"""
        service = get_scenario_service()
        
        scenarios = service.list_scenarios()
        
        assert len(scenarios) > 0
        assert all(hasattr(s, 'id') for s in scenarios)
        assert all(hasattr(s, 'title') for s in scenarios)
    
    def test_nonexistent_scenario(self):
        """Test getting a scenario that doesn't exist"""
        service = get_scenario_service()
        
        scenario = service.get_scenario("nonexistent_scenario_id")
        
        assert scenario is None
    
    def test_curated_scenarios_structure(self):
        """Test that curated scenarios have required fields"""
        for scenario_id, scenario in CURATED_SCENARIOS.items():
            assert scenario.id == scenario_id
            assert scenario.title
            assert scenario.description
            assert scenario.persona_name
            assert scenario.persona_role
            assert scenario.setting
            assert len(scenario.goals) > 0
            assert scenario.dialect
    
    @pytest.mark.skipif(
        "not config.getoption('--run-api-tests', default=False)",
        reason="Skipping API tests to limit costs"
    )
    def test_generate_custom_scenario(self):
        """Test generating a custom scenario (requires API call)"""
        service = get_scenario_service()
        
        custom = CustomScenario(
            prompt="Having tea at a friend's house",
            dialect="doabi"
        )
        
        scenario = service.generate_custom_scenario(custom)
        
        assert scenario is not None
        assert scenario.id == "custom"
        assert scenario.persona_name
        assert scenario.setting
        assert len(scenario.goals) > 0


def pytest_addoption(parser):
    """Add custom pytest command line option"""
    parser.addoption(
        "--run-api-tests",
        action="store_true",
        default=False,
        help="Run tests that make API calls (costs money)"
    )

