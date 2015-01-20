from distutils.core import setup

setup(
    name='twistedlilypad',
    version='0.1',
    packages=[
        'twistedlilypad',
        'twistedlilypad.Packets',
        'twistedlilypad.Requests',
        'twistedlilypad.Results',
        'twistedlilypad.Utilities'
    ],
    url='',
    license='MIT',
    author='Alasdair Scott',
    author_email='ali@flaminscotsman.co.uk',
    description='Implementation of the lilypad protocol in python'
)
