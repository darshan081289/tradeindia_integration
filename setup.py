from setuptools import setup, find_packages

with open("requirements.txt") as f:
    install_requires = f.read().strip().split("\n")

# Get version from __version__ variable in tradeindia_integration/__init__.py
from tradeindia_integration import __version__ as version

setup(
    name="tradeindia_integration",
    version=version,
    description="Integration between TradeIndia and ERPNext",
    author="Darshan Patel",
    author_email="darshan.patel@quarkssystems.com",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=install_requires
)
