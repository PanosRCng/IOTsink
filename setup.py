from setuptools import setup, find_packages



f = open('README.md', 'r')
LONG_DESCRIPTION = f.read()
f.close()

setup(
    name='iotsink',
    description='server app that acts as a message sink',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author='PanosRCng',
    author_email='panosrcng@gmail.com',
    url='https://cloud.panosrcng.com/gogs/iotsink',
    license='unlicensed',
    packages=find_packages(exclude=['ez_setup']),
    entry_points="""
        [console_scripts]
        iotsink = iotsink.iotsink
    """,
)
