from setuptools import find_packages, setup

setup(
    name = 'Myflaskblog',
    version = '1.0.0',
    author = 'Ahmadullah Mirza',
    author_email = 'ahmad@trickyadmin.com',
    description = 'This is my first flask application',
    # long_description = open(readme.txt).read(),
    # license = 'LICENSE.txt',
    packages = find_packages(),
    include_package_data  = True ,
    zip_safe = False,
    install_requires= [
        'flask'
    ]
)
