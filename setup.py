from setuptools import setup
from janitor import __version__

setup(
    name='django-janitor',
    version=__version__,
    description="django-janitor allows you to use bleach to clean HTML stored in a Model's field.",
    long_description=open('README.rst').read(),
    author='Brad Montgomery',
    author_email='brad@bradmontgomery.net',
    url='https://bitbucket.org/bkmontgomery/django-janitor/',
    license='BSD',
    packages=['janitor'],
    include_package_data=True,
    package_data = { '': ['README.rst'] },
    zip_safe=False,
    install_requires=['django', 'bleach'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Markup :: HTML',
        'Topic :: Utilities',
    ]
)
