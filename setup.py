from setuptools import setup
from os import path


with open(path.join(path.abspath(path.dirname(__file__)), 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='flask_mysql_connector',
    version='1.0.2',
    url='https://github.com/brandenc40/flask_mysql_connector',
    license='MIT',
    author='Branden Colen',
    author_email='brandencolen@gmail.com',
    description='Easy to use MySQL client for Flask apps.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=['flask_mysql_connector'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'mysql-connector-python',
        'flask',
        'pandas'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
