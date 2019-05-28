from setuptools import find_packages, setup

setup(
    name="bitdefender_project_server",
    version="0.0.1",
    platforms="any",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],  # TODO
    author="Bit Defender",
    description="Server",
)
