import pytest
import pandas as pd
from unittest.mock import MagicMock
from hybrid_renewable_pypsa.src.network_setup import Network_Setup
from hybrid_renewable_pypsa.src.data_loader import Data_Loader

@pytest.fixture
def mock_data_loader():
    data_loader = Data_Loader('data')
    data_loader.read_csv = MagicMock()
    return data_loader

@pytest.fixture
def network_setup(mock_data_loader):
    network_setup = Network_Setup('data')
    network_setup.data_loader = mock_data_loader
    return network_setup

def test_add_buses(network_setup, mock_data_loader):
    """Test adding buses to the network."""
    mock_data_loader.read_csv.return_value = pd.DataFrame({
        'name': ['bus1', 'bus2'],
        'v_nom': [110, 220],
        'x': [0, 1],
        'y': [0, 1],
        'carrier': ['AC', 'DC']
    })
    network_setup._add_buses()
    assert 'bus1' in network_setup.network.buses.index
    assert 'bus2' in network_setup.network.buses.index

def test_add_generators(network_setup, mock_data_loader):
    """Test adding generators to the network."""
    mock_data_loader.read_csv.return_value = pd.DataFrame({
        'name': ['gen1', 'gen2'],
        'bus': ['bus1', 'bus2'],
        'control': ['PQ', 'PV'],
        'p_nom': [100, 200],
        'efficiency': [0.9, 0.95],
        'capital_cost': [1000, 2000],
        'marginal_cost': [10, 20],
        'p_max_pu': [1.0, 1.0],
        'p_min_pu': [0.0, 0.0]
    })
    network_setup._add_generators()
    assert 'gen1' in network_setup.network.generators.index
    assert 'gen2' in network_setup.network.generators.index

def test_add_storage_units(network_setup, mock_data_loader):
    """Test adding storage units to the network."""
    mock_data_loader.read_csv.return_value = pd.DataFrame({
        'name': ['storage1', 'storage2'],
        'bus': ['bus1', 'bus2'],
        'p_nom': [50, 100],
        'capital_cost': [500, 1000],
        'state_of_charge_initial': [0.5, 0.8],
        'efficiency_store': [0.9, 0.95],
        'efficiency_dispatch': [0.9, 0.95],
        'max_hours': [4, 8],
        'marginal_cost': [5, 10],
        'p_min_pu': [0.0, 0.0],
        'p_max_pu': [1.0, 1.0],
        'cyclic_state_of_charge': [True, False],
        'state_of_charge_min': [0.1, 0.2],
        'state_of_charge_max': [0.9, 0.95]
    })
    network_setup._add_storage_units()
    assert 'storage1' in network_setup.network.storage_units.index
    assert 'storage2' in network_setup.network.storage_units.index

def test_add_lines(network_setup, mock_data_loader):
    """Test adding lines to the network."""
    mock_data_loader.read_csv.return_value = pd.DataFrame({
        'name': ['line1', 'line2'],
        'bus0': ['bus1', 'bus2'],
        'bus1': ['bus3', 'bus4'],
        'length': [10, 20],
        'r_per_length': [0.01, 0.02],
        'x_per_length': [0.03, 0.04],
        'c_per_length': [0.05, 0.06],
        's_nom': [100, 200],
        'type': ['overhead', 'underground'],
        'capital_cost': [10000, 20000]
    })
    network_setup._add_lines()
    assert 'line1' in network_setup.network.lines.index
    assert 'line2' in network_setup.network.lines.index

def test_add_transformers(network_setup, mock_data_loader):
    """Test adding transformers to the network."""
    mock_data_loader.read_csv.return_value = pd.DataFrame({
        'name': ['transformer1', 'transformer2'],
        'bus0': ['bus1', 'bus2'],
        'bus1': ['bus3', 'bus4'],
        's_nom': [100, 200],
        'x': [0.01, 0.02],
        'r': [0.03, 0.04],
        'tap_position': [0, 1],
        'tap_min': [-5, -5],
        'tap_max': [5, 5],
        'tap_step': [0.01, 0.01],
        'efficiency': [0.98, 0.99],
        'capital_cost': [5000, 10000]
    })
    network_setup._add_transformers()
    assert 'transformer1' in network_setup.network.transformers.index
    assert 'transformer2' in network_setup.network.transformers.index

def test_add_links(network_setup, mock_data_loader):
    """Test adding links to the network."""
    mock_data_loader.read_csv.return_value = pd.DataFrame({
        'name': ['link1', 'link2'],
        'bus0': ['bus1', 'bus2'],
        'bus1': ['bus3', 'bus4'],
        'p_nom': [100, 200],
        'efficiency': [0.9, 0.95],
        'capital_cost': [1000, 2000],
        'transformer_type': ['type1', 'type2'],
        'min_pu': [0.0, 0.0],
        'max_pu': [1.0, 1.0],
        'reactive_power_capacity': [50, 100],
        'r': [0.01, 0.02],
        'x': [0.03, 0.04],
        'startup_cost': [100, 200],
        'shutdown_cost': [50, 100],
        'ramp_up': [10, 20],
        'ramp_down': [10, 20],
        'maintenance_cost': [5, 10],
        'control_type': ['type1', 'type2']
    })
    network_setup._add_links()
    assert 'link1' in network_setup.network.links.index
    assert 'link2' in network_setup.network.links.index

def test_add_loads(network_setup, mock_data_loader):
    """Test adding loads to the network."""
    mock_data_loader.read_csv.return_value = pd.DataFrame({
        'name': ['load1', 'load2'],
        'bus': ['bus1', 'bus2'],
        'p_set': ['1.0,2.0', '3.0,4.0'],
        'q_set': ['0.5,1.0', '1.5,2.0'],
        'p_min': [0.0, 0.0],
        'p_max': [10.0, 20.0],
        'scaling_factor': [1.0, 1.0],
        'status': [True, True],
        'control_type': ['type1', 'type2'],
        'response_time': [0.1, 0.2],
        'priority': [1, 2]
    })
    network_setup._add_loads()
    assert 'load1' in network_setup.network.loads.index
    assert 'load2' in network_setup.network.loads.index