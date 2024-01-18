from setuptools import setup

setup(
    name='tap-calendly',
    version='0.0.3',
    packages=['tap_calendly', 'tap_calendly.tests'],
    url='https://github.com/singer-io/tap-calendly',
    license='',
    author='Nolan McCafferty',
    author_email='nolanmccafferty@gmail.com',
    description='Singer.io tap for Calendly',
    install_requires=[
        'requests~=2.25.1',
        'singer-sdk'],
)
