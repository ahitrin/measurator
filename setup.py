from setuptools import setup

setup(
    name='measurator',
    version=0.1,
    url='https://ahitrin.github.io',
    license='MIT',
    author='Andrey Hitrin',
    author_email='andrey.hitrin@gmail.com',
    description='Simple command-line app aimed to record and evaluate measures',
    packages=['measurator'],
    scripts=['bin/measure'],
    platform='any',
    classifiers = [
        'Programming Language :: Python',
        'Development Status :: 1 - Alpha',
        ],
)
