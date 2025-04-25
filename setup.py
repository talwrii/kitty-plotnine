import setuptools

setuptools.setup(
    name='kitty-plotnine',
    version="1.2.0",
    author='@readwithai',
    long_description_content_type='text/markdown',
    author_email='talwrii@gmail.com',
    description='Plot from the command-line with one-liners. Render plots in-line',
    license='GPLv3',
    keywords='kitty,terminal,plot,plotting',
    url='https://github.com/talwrii/kitty-plotnine',
    packages=["kitty_plotnine"],
    install_requires=[
        "plotnine",
        "matplotlib-backend-kitty"
    ],
    long_description=open('README.md').read(),
    entry_points={
        'console_scripts': ['k-nine=kitty_plotnine.main:main']
    },
    test_suite='nose.collector'
)
