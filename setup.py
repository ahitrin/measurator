from setuptools import setup, find_packages

setup(
    name='measurator',
    version='0.3.4',
    url='https://github.com/ahitrin-attic/measurator-proto',
    license='MIT',
    author='Andrey Hitrin',
    author_email='andrey.hitrin@gmail.com',
    description='Simple command-line app aimed to record and evaluate measures',
    packages=['measurator'],
    scripts=['bin/measure'],
    classifiers=[
        'Programming Language :: Python',
        'Development Status :: 1 - Alpha',
    ],
)
