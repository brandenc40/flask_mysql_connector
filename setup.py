"""
Flask-MySql-Connector
-------------

Easy to use MySQL client for Flask apps.
"""
from setuptools import setup


setup(
    name='Flask-MySql-Connector',
    version='1.0',
    url='https://github.com/brandenc40/flask_mysql_connector',
    license='BSD',
    author='Branden Colen',
    author_email='brandencolen@gmail.com',
    description='Easy to use MySQL client for Flask apps.',
    long_description=__doc__,
    packages=['flask_mysql_connector'],
    namespace_packages=['flask_mysql_connector'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    packages=setuptools.find_packages(),
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
