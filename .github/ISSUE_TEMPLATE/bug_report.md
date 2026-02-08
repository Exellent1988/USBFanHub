---
name: Bug Report
about: Report a bug to help us improve
title: '[BUG] '
labels: bug
assignees: ''
---

## 🐛 Bug Description

A clear and concise description of the bug.

## 🔄 Reproduce

Steps to reproduce the behavior:

1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

## ✅ Expected Behavior

A clear and concise description of what you expected to happen.

## 📸 Screenshots

If applicable, add screenshots to explain the problem.

## 🖥️ System Information

**Hardware:**
- Raspberry Pi Pico: [yes/no]
- Fan type: [e.g., Noctua NF-A12x25]
- RGB LEDs: [WS2812B, count]

**Software:**
- OS: [e.g., Ubuntu 22.04]
- Python version: [e.g., 3.10.5]
- Firmware version: [e.g., v1.0.0]
- Driver version: [e.g., 1.0.0]

**Component:**
- [ ] Firmware (Pico)
- [ ] Python driver
- [ ] CLI tool
- [ ] Hardware
- [ ] Documentation

## 📋 Logs

```
Insert relevant logs here
```

**Firmware logs:**
```
# If DEBUG enabled
```

**Python logs:**
```bash
# Output from:
pico-fan-ctl status
# or
python -m pico_fan_hub.cli status
```

**USB logs:**
```bash
# Output from:
lsusb | grep 2e8a
dmesg | tail -20
```

## 🔍 Additional Context

Additional information about the problem.

## ✅ Checklist

- [ ] I have read the documentation
- [ ] I have searched for similar issues
- [ ] I have tested with the latest version
- [ ] I can reproduce the problem
