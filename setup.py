from setuptools import setup
from janitor import __version__

short_desc = (
    "django-janitor allows you to use bleach to clean HTML stored in a "
    "Model's field."
)

setup(
    name='django-janitor',
    version=__version__,
    description=short_desc,
    long_description=open('README.rst').read(),
    author='Brad Montgomery',
    author_email='brad@bradmontgomery.net',
    url='https://github.com/bradmontgomery/django-janitor',
    license='MIT',
    packages=['janitor'],
    include_package_data=True,
    package_data={'': ['README.rst']},
    zip_safe=False,
    install_requires=['django', 'bleach'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Markup :: HTML',
        'Topic :: Utilities',
    ]
)
