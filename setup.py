from distutils.core import setup
 
setup(
    name='django-memo',
    version='0.0.1',
    description='Simple django application to create notes and share with other users',
    author='Tommaso Barbugli',
    author_email='tbarbugli@gmail.com',
    url='http://github.com/tbarbugli',
    package_dir={'notes': 'notes'},
    packages=packages,
    package_data={'notes': data_files}, 
    install_requires = ['django-gravatar', 'setuptools'],
    classifiers=[
        'Development Status :: 1 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ]
)