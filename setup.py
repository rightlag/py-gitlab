import gitlab

from setuptools import setup, find_packages


setup(
    name='py-gitlab',
    version=gitlab.__version__,
    description='A Python SDK used to interface with the GitLab Web API',
    url='http://gitlab.cisco.com/rightlag/py-gitlab',
    author=gitlab.__author__,
    author_email='jaswalsh@cisco.com',
    license='MIT',
    packages=find_packages(exclude=['test*']),
    install_requires=[
        'requests',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
    ],
    keywords='gitlab web-api sdk',
)
