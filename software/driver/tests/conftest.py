"""
Pytest configuration and fixtures
"""

import pytest
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture
def mock_hid_available():
    """Mock HID library availability"""
    return True


@pytest.fixture
def sample_fan_data():
    """Sample fan data for tests"""
    return {
        'rpms': [1200, 1300, 1400, 1500, 1600, 1700],
        'pwms': [128, 128, 128, 128, 128, 128],
        'num_fans': 6
    }


@pytest.fixture
def sample_rgb_colors():
    """Sample RGB color data"""
    return [
        (255, 0, 0),    # Red
        (0, 255, 0),    # Green
        (0, 0, 255),    # Blue
        (255, 255, 0),  # Yellow
        (255, 0, 255),  # Magenta
        (0, 255, 255),  # Cyan
    ]
