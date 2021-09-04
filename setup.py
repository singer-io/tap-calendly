from setuptools import setup

setup(
    name='tap-calendly',
    version='0.0.1',
    packages=['tap_calendly', 'tap_calendly.tests'],
    url='https://github.com/karbonhq/singer-tap-calendly',
    license='',
    author='Nolan McCafferty',
    author_email='nolanmccafferty@gmail.com',
    description='Singer.io tap for Calendly',
    install_requires=['setuptools~=41.0.1', 'requests~=2.25.1', 'singer-sdk'],
)
