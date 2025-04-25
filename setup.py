import setuptools

setuptools.setup(
    name='kitty-plotnine',
    version=0.1,
    author='readwithai',
    long_description_content_type='text/markdown',
    author_email='Email',
    description='',
    license='GPLv3',
    keywords='',
    url='',
    packages=["kitty_plotnine"],
    install_requires=[
        "plotnine",
        "matplotlib-backend-kitty"
    ],
    long_description=open('README.md').read(),
    entry_points={
        'console_scripts': ['k-nine=kitty_plotnine.main:main']
    },
    classifiers=[
    ],
    test_suite='nose.collector'
)
