import setuptools
from setuptools import find_packages

CLASSIFIERS = [
    'Development Status :: 3 - Alpha',
    'License :: OSI Approved :: MIT License',
    'Environment :: Console',
    'Topic :: Internet :: Name Service (DNS)'
]

setuptools.setup(name='autodns',
                 version='0.0.1',
                 description='Update DNS records with AWS Rt53',
                 long_description=open('README.md').read().strip(),
                 author='Charles Butler',
                 author_email='charles.butler@ubuntu.com',
                 url='http://github.com/chuckbutler/auto-dns',
                 py_modules=[],
                 packages=find_packages(),
                 entry_points={
                     'console_scripts': [
                         'autodns = autodns.cli:main'
                         ],
                     },
                 install_requires=['pyyaml', 'path.py'],
                 package_data={
                     'template': ['template/record'],
                 },
                 include_package_data=True,
                 license='MIT License',
                 zip_safe=False,
                 keywords='dns, aws, route53, rt53',
                 classifiers=CLASSIFIERS)
