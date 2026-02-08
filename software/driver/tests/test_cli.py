"""
Unit tests for pico_fan_hub.cli module
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from io import StringIO
import sys

from pico_fan_hub import cli


class TestCLI:
    """Tests for CLI commands"""
    
    @pytest.fixture
    def mock_fan_hub(self):
        """Create a mock PicoFanHub"""
        mock = Mock()
        mock.connect.return_value = True
        mock.disconnect = Mock()
        mock.get_config.return_value = {
            'version': (1, 0, 0),
            'num_fans': 6,
            'num_rgb_leds': 60,
            'pwm_frequency_khz': 25,
            'features': 0x07
        }
        mock.get_all_fan_rpm.return_value = [1200, 1300, 1400, 0, 0, 0]
        mock.get_all_fan_pwm.return_value = [128, 128, 128, 0, 0, 0]
        mock.set_fan_pwm.return_value = True
        mock.set_all_fan_pwm.return_value = True
        mock.set_rgb_mode_rainbow.return_value = True
        mock.set_rgb_mode_breathing.return_value = True
        mock.set_rgb_mode_static.return_value = True
        mock.set_rgb_off.return_value = True
        return mock
    
    def test_cmd_list_with_devices(self, mock_fan_hub):
        """Test list command with devices found"""
        mock_devices = [
            {'product_string': 'Pico Fan Hub', 'serial_number': '123456', 'path': b'/dev/hidraw0'}
        ]
        
        with patch('pico_fan_hub.cli.find_devices', return_value=mock_devices):
            args = Mock(command='list')
            result = cli.cmd_list(args)
            
            assert result == 0
    
    def test_cmd_list_no_devices(self):
        """Test list command with no devices"""
        with patch('pico_fan_hub.cli.find_devices', return_value=[]):
            args = Mock(command='list')
            result = cli.cmd_list(args)
            
            assert result == 1
    
    def test_cmd_info_success(self, mock_fan_hub):
        """Test info command success"""
        with patch('pico_fan_hub.cli.PicoFanHub', return_value=mock_fan_hub):
            args = Mock(command='info')
            result = cli.cmd_info(args)
            
            assert result == 0
            mock_fan_hub.connect.assert_called_once()
            mock_fan_hub.get_config.assert_called_once()
            mock_fan_hub.disconnect.assert_called_once()
    
    def test_cmd_info_connection_failure(self):
        """Test info command with connection failure"""
        mock = Mock()
        mock.connect.return_value = False
        
        with patch('pico_fan_hub.cli.PicoFanHub', return_value=mock):
            args = Mock(command='info')
            result = cli.cmd_info(args)
            
            assert result == 1
    
    def test_cmd_status_success(self, mock_fan_hub):
        """Test status command success"""
        with patch('pico_fan_hub.cli.PicoFanHub', return_value=mock_fan_hub):
            args = Mock(command='status')
            result = cli.cmd_status(args)
            
            assert result == 0
            mock_fan_hub.get_all_fan_rpm.assert_called_once()
            mock_fan_hub.get_all_fan_pwm.assert_called_once()
    
    def test_cmd_set_pwm_success(self, mock_fan_hub):
        """Test set-pwm command success"""
        with patch('pico_fan_hub.cli.PicoFanHub', return_value=mock_fan_hub):
            args = Mock(command='set-pwm', fan=1, duty=128)
            result = cli.cmd_set_pwm(args)
            
            assert result == 0
            mock_fan_hub.set_fan_pwm.assert_called_with(0, 128)
    
    def test_cmd_set_pwm_invalid_duty(self, mock_fan_hub):
        """Test set-pwm with invalid duty cycle"""
        with patch('pico_fan_hub.cli.PicoFanHub', return_value=mock_fan_hub):
            args = Mock(command='set-pwm', fan=1, duty=300)
            result = cli.cmd_set_pwm(args)
            
            assert result == 1
    
    def test_cmd_set_all_pwm_success(self, mock_fan_hub):
        """Test set-all-pwm command success"""
        with patch('pico_fan_hub.cli.PicoFanHub', return_value=mock_fan_hub):
            args = Mock(command='set-all-pwm', duty=200)
            result = cli.cmd_set_all_pwm(args)
            
            assert result == 0
            mock_fan_hub.set_all_fan_pwm.assert_called_once()
    
    def test_cmd_rgb_off(self, mock_fan_hub):
        """Test RGB off command"""
        with patch('pico_fan_hub.cli.PicoFanHub', return_value=mock_fan_hub):
            args = Mock(command='rgb', mode='off', color=None, speed=None)
            result = cli.cmd_rgb(args)
            
            assert result == 0
            mock_fan_hub.set_rgb_off.assert_called_once()
    
    def test_cmd_rgb_rainbow(self, mock_fan_hub):
        """Test RGB rainbow command"""
        with patch('pico_fan_hub.cli.PicoFanHub', return_value=mock_fan_hub):
            args = Mock(command='rgb', mode='rainbow', color=None, speed=75)
            result = cli.cmd_rgb(args)
            
            assert result == 0
            mock_fan_hub.set_rgb_mode_rainbow.assert_called_with(75)
    
    def test_cmd_rgb_breathing(self, mock_fan_hub):
        """Test RGB breathing command"""
        with patch('pico_fan_hub.cli.PicoFanHub', return_value=mock_fan_hub):
            args = Mock(command='rgb', mode='breathing', color='255,0,0', speed=30)
            result = cli.cmd_rgb(args)
            
            assert result == 0
            mock_fan_hub.set_rgb_mode_breathing.assert_called_with(255, 0, 0, 30)
    
    def test_cmd_rgb_static(self, mock_fan_hub):
        """Test RGB static command"""
        with patch('pico_fan_hub.cli.PicoFanHub', return_value=mock_fan_hub):
            args = Mock(command='rgb', mode='static', color='0,255,0', speed=None)
            result = cli.cmd_rgb(args)
            
            assert result == 0
            mock_fan_hub.set_rgb_mode_static.assert_called_with(0, 255, 0)
    
    def test_cmd_rgb_breathing_no_color(self, mock_fan_hub):
        """Test RGB breathing without color specified"""
        with patch('pico_fan_hub.cli.PicoFanHub', return_value=mock_fan_hub):
            args = Mock(command='rgb', mode='breathing', color=None, speed=30)
            result = cli.cmd_rgb(args)
            
            assert result == 1
    
    def test_cmd_rgb_unknown_mode(self, mock_fan_hub):
        """Test RGB with unknown mode"""
        with patch('pico_fan_hub.cli.PicoFanHub', return_value=mock_fan_hub):
            args = Mock(command='rgb', mode='unknown', color=None, speed=None)
            result = cli.cmd_rgb(args)
            
            assert result == 1
