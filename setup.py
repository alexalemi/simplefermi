from distutils.core import setup

setup(
        name="SimpleFermi",
        version="0.1.0",
        packages=["simplefermi",],
        author="Alex Alemi",
        author_email="alexalemi@gmail.com",
        install_requires=[
            'pint',
            'pyerf',
            'matplotlib',
            'ipython',
            'numpy',
            'pillow',
        ],
        license="MIT",
        long_description=open('README.md').read(),
)
