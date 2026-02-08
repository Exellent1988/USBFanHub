# Contributing to Pico Fan Hub

Thank you for your interest in the Pico Fan Hub project!

## Development Setup

### Firmware Development

1. **Install Pico SDK:**
   ```bash
   cd ~
   git clone https://github.com/raspberrypi/pico-sdk.git
   cd pico-sdk
   git submodule update --init
   export PICO_SDK_PATH=~/pico-sdk
   ```

2. **Install build tools:**
   ```bash
   sudo apt install cmake gcc-arm-none-eabi libnewlib-arm-none-eabi
   ```

3. **Build firmware:**
   ```bash
   cd firmware
   ./build.sh
   ```

### Linux Software Development

1. **Install dependencies:**
   ```bash
   sudo apt install python3-pip python3-hid libhidapi-hidraw0
   ```

2. **Development installation:**
   ```bash
   cd software/driver
   pip3 install -e .
   ```

3. **Run tests:**
   ```bash
   python3 -m pytest
   ```

## Project Structure

```
.
├── firmware/               # Pico firmware (C/C++)
│   ├── src/               # Source code
│   ├── include/           # Header files
│   └── build.sh           # Build script
├── software/              # Linux software
│   └── driver/            # Python hwmon driver
├── hardware/              # Hardware documentation
│   ├── pinout.md          # Pin assignments
│   └── schematic_suggestions.md  # KiCad suggestions
├── docs/                  # Documentation
└── README.md              # Main documentation
```

## Code Guidelines

### Firmware (C/C++)

- **Style:** K&R C Style
- **Indentation:** 4 spaces
- **Comments:** English
- **Documentation:** Doxygen-compatible

**Example:**
```c
/**
 * @brief Sets PWM for a fan
 * @param fan_index Fan index (0-5)
 * @param duty_cycle PWM duty cycle (0-255)
 */
void pwm_control_set_duty(uint8_t fan_index, uint8_t duty_cycle) {
    if (fan_index >= NUM_FANS) {
        return;
    }
    // Implementation...
}
```

### Python

- **Style:** PEP 8
- **Indentation:** 4 spaces
- **Type Hints:** Use where possible
- **Docstrings:** Google Style

**Example:**
```python
def set_fan_pwm(self, fan_index: int, duty_cycle: int) -> bool:
    """
    Sets PWM for a fan.
    
    Args:
        fan_index: Fan index (0-5)
        duty_cycle: PWM value (0-255)
        
    Returns:
        True on success, False on error
    """
    if fan_index < 0 or fan_index >= self.num_fans:
        return False
    # Implementation...
```

## Git Workflow

1. **Fork the repository**

2. **Create a feature branch:**
   ```bash
   git checkout -b feature/my-feature
   ```

3. **Commit your changes:**
   ```bash
   git add .
   git commit -m "feat(pwm): Add new PWM frequency setting"
   ```

4. **Push to fork:**
   ```bash
   git push origin feature/my-feature
   ```

5. **Create a Pull Request**

### Commit Message Format

We use [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bugfix
- `docs`: Documentation
- `style`: Formatting
- `refactor`: Code refactoring
- `test`: Tests
- `chore`: Build system, dependencies

**Examples:**
```
feat(rgb): Add rainbow effect
fix(tachometer): Correct RPM calculation
docs(hardware): Expand pinout documentation
```

## Testing

### Firmware Tests

Manual tests with hardware required. Test checklist:

- [ ] Measure PWM output with oscilloscope (25 kHz)
- [ ] Test tachometer input with various fans
- [ ] Test RGB output with WS2812B strip
- [ ] Check USB enumeration (`lsusb`)
- [ ] Test all HID reports

### Software Tests

```bash
cd software/driver
python3 -m pytest tests/
```

### Integration Tests

1. Flash firmware on Pico
2. Connect to Linux system
3. Start driver
4. Test all CLI commands

## Hardware Tests

If you're proposing hardware changes:

1. **Simulation:** LTspice or similar
2. **Breadboard prototype:** Test first
3. **Measurements:** Oscilloscope screenshots
4. **Documentation:** Schematic + explanation

## Documentation

- **New features:** Document in README.md
- **API changes:** Update docs/usb_protocol.md
- **Hardware:** Document in hardware/ directory
- **Examples:** Always provide example code

## Pull Request Checklist

Before submitting a pull request:

- [ ] Code compiles without warnings
- [ ] Tests pass
- [ ] Documentation updated
- [ ] Commit messages follow convention
- [ ] Code style adhered to
- [ ] No unnecessary files committed
- [ ] Feature was tested (description in PR)

## Questions?

If you have questions, create an issue or contact the maintainers.

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.
