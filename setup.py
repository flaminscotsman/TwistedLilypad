from setuptools import find_packages, setup


setup(
    name='twistedlilypad',
    version='2.0.0',

    description='An implementation of the lilypad protocol in python',

    url='https://github.com/flaminscotsman/TwistedLilypad',

    author='Alasdair Scott',
    author_email='ali+python@flaminscotsman.co.uk',

    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development',

        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ],

    keywords='lilypad minecraft',

    packages=find_packages(exclude=('tests', 'tests.utilities')),

    install_requires=['twisted'],
)
