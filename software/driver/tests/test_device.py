"""
Unit tests for pico_fan_hub.device module
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
import struct

from pico_fan_hub.device import (
    PicoFanHub,
    find_devices,
    REPORT_ID_FAN_PWM,
    REPORT_ID_FAN_RPM,
    REPORT_ID_RGB_CONTROL,
    REPORT_ID_CONFIG,
)


class TestPicoFanHub:
    """Tests for PicoFanHub class"""
    
    @pytest.fixture
    def mock_hid_device(self):
        """Create a mock HID device"""
        mock_dev = Mock()
        mock_dev.open = Mock()
        mock_dev.close = Mock()
        mock_dev.set_nonblocking = Mock()
        mock_dev.get_feature_report = Mock()
        mock_dev.send_feature_report = Mock()
        mock_dev.write = Mock()
        return mock_dev
    
    @pytest.fixture
    def fan_hub(self, mock_hid_device):
        """Create a PicoFanHub instance with mocked HID"""
        with patch('pico_fan_hub.device.hid.device', return_value=mock_hid_device):
            hub = PicoFanHub()
            hub.device = mock_hid_device
            return hub
    
    def test_init(self):
        """Test PicoFanHub initialization"""
        hub = PicoFanHub()
        assert hub.vendor_id == 0x2E8A
        assert hub.product_id == 0x1001
        assert hub.num_fans == 6
        assert hub.device is None
    
    def test_connect_success(self, mock_hid_device):
        """Test successful connection"""
        with patch('pico_fan_hub.device.hid.device', return_value=mock_hid_device):
            # Mock config response
            config_data = struct.pack('<BBBBBBBB8s', 
                REPORT_ID_CONFIG, 1, 0, 0, 6, 60, 25, 0x07, b'\x00' * 8)
            mock_hid_device.get_feature_report.return_value = list(config_data)
            
            hub = PicoFanHub()
            result = hub.connect()
            
            assert result is True
            assert hub.num_fans == 6
            mock_hid_device.open.assert_called_once()
            mock_hid_device.set_nonblocking.assert_called_with(True)
    
    def test_connect_failure(self, mock_hid_device):
        """Test connection failure"""
        with patch('pico_fan_hub.device.hid.device', return_value=mock_hid_device):
            mock_hid_device.open.side_effect = Exception("Connection failed")
            
            hub = PicoFanHub()
            result = hub.connect()
            
            assert result is False
    
    def test_disconnect(self, fan_hub, mock_hid_device):
        """Test disconnection"""
        fan_hub.disconnect()
        mock_hid_device.close.assert_called_once()
        assert fan_hub.device is None
    
    def test_is_connected(self, fan_hub):
        """Test connection status check"""
        assert fan_hub.is_connected() is True
        fan_hub.device = None
        assert fan_hub.is_connected() is False
    
    def test_set_fan_pwm_valid(self, fan_hub, mock_hid_device):
        """Test setting valid PWM value"""
        # Mock get_all_fan_pwm
        current_pwm = struct.pack('B6BB', REPORT_ID_FAN_PWM, 
                                  100, 100, 100, 100, 100, 100, 0)
        mock_hid_device.get_feature_report.return_value = list(current_pwm)
        
        result = fan_hub.set_fan_pwm(0, 128)
        
        assert result is True
        mock_hid_device.send_feature_report.assert_called_once()
    
    def test_set_fan_pwm_invalid_index(self, fan_hub):
        """Test setting PWM with invalid fan index"""
        result = fan_hub.set_fan_pwm(10, 128)
        assert result is False
    
    def test_set_fan_pwm_invalid_duty(self, fan_hub):
        """Test setting PWM with invalid duty cycle"""
        result = fan_hub.set_fan_pwm(0, 300)
        assert result is False
    
    def test_set_all_fan_pwm(self, fan_hub, mock_hid_device):
        """Test setting PWM for all fans"""
        duties = [128, 128, 128, 128, 128, 128]
        result = fan_hub.set_all_fan_pwm(duties)
        
        assert result is True
        mock_hid_device.send_feature_report.assert_called_once()
        
        # Verify the sent data
        call_args = mock_hid_device.send_feature_report.call_args[0][0]
        assert call_args[0] == REPORT_ID_FAN_PWM
        assert list(call_args[1:7]) == duties
    
    def test_get_all_fan_pwm(self, fan_hub, mock_hid_device):
        """Test getting PWM values"""
        expected = [100, 150, 200, 255, 0, 128]
        pwm_data = struct.pack('B6BB', REPORT_ID_FAN_PWM, *expected, 0)
        mock_hid_device.get_feature_report.return_value = list(pwm_data)
        
        result = fan_hub.get_all_fan_pwm()
        
        assert result == expected
    
    def test_get_all_fan_rpm(self, fan_hub, mock_hid_device):
        """Test getting RPM values"""
        expected = [1200, 1300, 1400, 1500, 0, 0]
        rpm_data = struct.pack('<B6H', REPORT_ID_FAN_RPM, *expected)
        mock_hid_device.get_feature_report.return_value = list(rpm_data)
        
        result = fan_hub.get_all_fan_rpm()
        
        assert result == expected
    
    def test_get_config(self, fan_hub, mock_hid_device):
        """Test getting configuration"""
        config_data = struct.pack('<BBBBBBBB8s', 
            REPORT_ID_CONFIG, 1, 2, 3, 6, 60, 25, 0x07, b'\x00' * 8)
        mock_hid_device.get_feature_report.return_value = list(config_data)
        
        result = fan_hub.get_config()
        
        assert result['version'] == (1, 2, 3)
        assert result['num_fans'] == 6
        assert result['num_rgb_leds'] == 60
        assert result['pwm_frequency_khz'] == 25
        assert result['features'] == 0x07
    
    def test_set_rgb_direct(self, fan_hub, mock_hid_device):
        """Test setting RGB LEDs directly"""
        colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
        result = fan_hub.set_rgb_direct(0, colors)
        
        assert result is True
        mock_hid_device.send_feature_report.assert_called_once()
        
        # Verify the sent data
        call_args = mock_hid_device.send_feature_report.call_args[0][0]
        assert call_args[0] == REPORT_ID_RGB_CONTROL
        assert call_args[1] == 0  # start_index
        assert call_args[2] == 3  # count
        assert call_args[3] == 0x00  # mode: Direct
    
    def test_set_rgb_mode_rainbow(self, fan_hub, mock_hid_device):
        """Test setting rainbow mode"""
        result = fan_hub.set_rgb_mode_rainbow(speed=75)
        
        assert result is True
        mock_hid_device.send_feature_report.assert_called_once()
        
        call_args = mock_hid_device.send_feature_report.call_args[0][0]
        assert call_args[3] == 0x01  # mode: Rainbow
        assert call_args[4] == 75  # speed
    
    def test_set_rgb_mode_breathing(self, fan_hub, mock_hid_device):
        """Test setting breathing mode"""
        result = fan_hub.set_rgb_mode_breathing(255, 128, 64, speed=40)
        
        assert result is True
        mock_hid_device.send_feature_report.assert_called_once()
        
        call_args = mock_hid_device.send_feature_report.call_args[0][0]
        assert call_args[3] == 0x02  # mode: Breathing
        assert call_args[4:7] == bytes([255, 128, 64])  # RGB
        assert call_args[7] == 40  # speed
    
    def test_set_rgb_mode_static(self, fan_hub, mock_hid_device):
        """Test setting static color mode"""
        result = fan_hub.set_rgb_mode_static(255, 255, 255)
        
        assert result is True
        mock_hid_device.send_feature_report.assert_called_once()
        
        call_args = mock_hid_device.send_feature_report.call_args[0][0]
        assert call_args[3] == 0x03  # mode: Static
        assert call_args[4:7] == bytes([255, 255, 255])  # RGB
    
    def test_set_rgb_off(self, fan_hub, mock_hid_device):
        """Test turning RGB off"""
        result = fan_hub.set_rgb_off()
        
        assert result is True
        mock_hid_device.send_feature_report.assert_called_once()
        
        call_args = mock_hid_device.send_feature_report.call_args[0][0]
        assert call_args[3] == 0x04  # mode: Off


def test_find_devices():
    """Test finding devices"""
    with patch('pico_fan_hub.device.hid.enumerate') as mock_enum:
        mock_enum.return_value = [
            {'vendor_id': 0x2E8A, 'product_id': 0x1001, 'path': b'/dev/hidraw0'},
            {'vendor_id': 0x2E8A, 'product_id': 0x1001, 'path': b'/dev/hidraw1'},
        ]
        
        devices = find_devices()
        
        assert len(devices) == 2
        mock_enum.assert_called_with(0x2E8A, 0x1001)
