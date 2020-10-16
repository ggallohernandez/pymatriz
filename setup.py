from setuptools import setup

with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(
    name='pymatriz',
    version='0.1.4',
    packages=['pymatriz'],
    url='https://github.com/ggallohernandez/pymatriz',
    license='MIT License',
    author='Guillermo Gallo',
    author_email='ggallohernandez@gmail.com',
    description='Python connector for Primary DMA (Matriz) Rest and Websocket APIs.',
    long_description=long_description,
    long_description_content_type="text/x-rst",
    install_requires=[
        'requests',
        'simplejson',
        'websocket-client',
        'pandas',
        'lxml',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "Topic :: Office/Business :: Financial :: Investment",
        "Topic :: Software Development"
    ],
)
