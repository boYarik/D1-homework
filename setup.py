import setuptools  
  
with open("README.md", "r") as fh:  
 long_description = fh.read()  
setuptools.setup(  
 name="trello_client", version="0.0.1", author="Ярослав", author_email="malysevaroslav0@gmail.com", description="Клиент для трелло", long_description=long_description, long_description_content_type="text/markdown", url="https://github.com/basics-api-username/trello_client", packages=setuptools.find_packages(), classifiers=[ "Programming Language :: Python :: 3", "License :: OSI Approved :: MIT License", "Operating System :: OS Independent", ], python_requires='>=3.6',)
