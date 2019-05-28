try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

setup(
    name = 'gitlab-cloner',
    version = '0.0.1',
    author = 'dedoussis',
    description = 'Clones everything',
    author_email = 'ddedoussis@gmail.com',
    packages = find_packages(),
    entry_points = {
        'console_scripts': ['gitlab-cloner = gitlab_cloner.__main__:main']
    }
)
