import pytest
from unittest.mock import MagicMock, patch
import matplotlib.pyplot as plt
from src.network_plot import Network_Plot

@pytest.fixture
def mock_network_setup():
    with patch('src.network_plot.Network_Setup') as MockNetworkSetup:
        mock_network_setup = MockNetworkSetup.return_value
        mock_network_setup.get_network.return_value = MagicMock(
            buses=MagicMock(
                x=[0, 1],
                y=[0, 1],
                iterrows=MagicMock(return_value=iter([
                    ('bus1', MagicMock(x=0, y=0)),
                    ('bus2', MagicMock(x=1, y=1))
                ]))
            ),
            lines=MagicMock(
                iterrows=MagicMock(return_value=iter([
                    (0, MagicMock(bus0='bus1', bus1='bus2'))
                ]))
            ),
            links=MagicMock(
                iterrows=MagicMock(return_value=iter([
                    (0, MagicMock(bus0='bus1', bus1='bus2'))
                ]))
            ),
            transformers=MagicMock(
                iterrows=MagicMock(return_value=iter([
                    (0, MagicMock(bus0='bus1', bus1='bus2'))
                ]))
            ),
            generators=MagicMock(
                iterrows=MagicMock(return_value=iter([
                    (0, MagicMock(bus='bus1', name='gen1'))
                ]))
            )
        )
        yield mock_network_setup

@pytest.fixture
def network_plot(mock_network_setup):
    return Network_Plot('data')

def test_plot_network(network_plot):
    with patch.object(plt, 'show'):
        network_plot.plot_network()
        plt.show.assert_called_once()