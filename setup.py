from setuptools import find_packages, setup

install_requires = [
    "wagtail>=2.11,<3",
    "django-treebeard>=4.0,<=4.5"
]

testing_extras = ["coverage>=3.7.0"]

setup(
    name="wagtail-exim",
    url="https://github.com/cfpb/wagtail-exim",
    author="CFPB",
    author_email="tech@cfpb.gov",
    description="Utility to export and import Wagtail pages by URL path",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    license="CC0",
    version="1.0.0",
    include_package_data=True,
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=install_requires,
    extras_require={"testing": testing_extras},
    classifiers=[
        "Framework :: Django",
        "Framework :: Django :: 2.2",
        "Framework :: Django :: 3.1",
        "Framework :: Wagtail",
        "Framework :: Wagtail :: 2",
        "License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication",
        "License :: Public Domain",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
)
