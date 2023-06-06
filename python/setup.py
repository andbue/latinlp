from setuptools import setup, find_packages

setup(
    name='lemmatizers',
    version='0.0.1',
    license='GPL_v3.0',
    author='Andreas Büttner',
    author_email='andreas.buettner@uni-wuerzburg.de',
    description='A python interface to some lemmatizers for the Latin language',
    url='http://github.com/andbue/latinlp',
    long_description="This python module needs to be populated with binary packages and data by the docker file in the latinlp repository.",
    long_description_content_type='text/markdown',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    python_requires='>=3',
    install_requires=[
        'lxml',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    ],
)
