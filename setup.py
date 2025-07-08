from setuptools import setup, find_packages
import os 
import sys 
from networksecurity.logger import Custom_Logger
from networksecurity.exception import CustomException
from typing import List

HYPEN_E_DOT = '-e .'
def get_requirements(file_path : str)->List[str]:
    requirements = []
    try:
        with open(file_path) as file_obj:
            requirements = file_obj.readlines()
            requirements = [req.replace("/n" , "") for req in requirements]

            if HYPEN_E_DOT in requirements:
                requirements.remove(HYPEN_E_DOT)
        
    except Exception as e:
        raise CustomException(e , sys)

setup(
    name = "networksecurity",
    version = "0.0.1" ,
    author = 'Anand J',
    author_email = 'anand06.jeyakumar@gmail.com',
    packages = find_packages(),
    install_requires = get_requirements('requirements.txt')
)