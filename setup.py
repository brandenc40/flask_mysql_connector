"""
Flask-MySql-Connector
-------------

Easy to use MySQL client for Flask app.
"""
from setuptools import setup


setup(
    name='Flask-MySql-Connector',
    version='1.0',
    url='http://example.com/flask-sqlite3/',
    license='BSD',
    author='Branden Colen',
    author_email='brandencolen@gmail.com',
    description='Easy to use MySQL client for Flask app.',
    long_description=__doc__,
    packages=['flask_mysql_connector'],
    namespace_packages=['flask_mysql_connector'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
