from setuptools import setup, find_packages

setup(
    name='pico-fan-hub',
    version='1.0.0',
    description='Linux hwmon driver for Raspberry Pi Pico Fan Hub',
    author='Custom',
    packages=find_packages(),
    install_requires=[
        'pyusb>=1.2.1',
        'hidapi>=0.12.0',
    ],
    entry_points={
        'console_scripts': [
            'pico-fan-hub=pico_fan_hub.daemon:main',
            'pico-fan-ctl=pico_fan_hub.cli:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
