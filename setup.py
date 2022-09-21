from setuptools import setup

setup(
    name='tap-calendly',
    version='0.0.2',
    packages=['tap_calendly', 'tap_calendly.tests'],
    url='https://github.com/singer-io/tap-calendly',
    license='',
    author='Nolan McCafferty',
    author_email='nolanmccafferty@gmail.com',
    description='Singer.io tap for Calendly',
    install_requires=['setuptools~=41.0.1', 'requests~=2.25.1', 'singer-sdk'],
    classifiers=['Programming Language :: Python :: 3 :: Only'],
    py_modules=['tap_calendly'],
    entry_points='''
            [console_scripts]
            tap-calendly=tap_calendly.tap:TapCalendly.cli
        '''
)
