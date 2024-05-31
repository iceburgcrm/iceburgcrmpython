from setuptools import setup, find_packages

setup(
    name='iceburgcrm',
    version='1.5.0',
    install_requires=[],
    author='Robert Devenyi',
    author_email='rob@iceburg.ca',
    description='Iceburg CRM is a metadata driven CRM in django python that allows you to quickly prototype any CRM. The default CRM is based on a typical business CRM but the flexibility of dynamic modules, fields, subpanels allows prototyping of any number of different tyes of CRMs.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://www.iceburg.ca',
    project_urls={
        'Homepage': 'https://github.com/iceburgcrm/iceburgcrmpython',
        'Demo': 'https://demo.iceburg.ca'
    },
    classifiers=[
        'AI CRM :: Django CRM :: Python CRM',
        'Orator :: CRM :: CRM Generator',
        'Metadata CRM :: CRM Creator',
    ],
    python_requires='>=3.8',
    packages=find_packages(),
)
