from setuptools import find_packages,setup
from typing import List

HYPHEN_E_DOT = '-e .'

def get_requirements(file_path:str)-> List[str]:
    '''
        gatheres all the requirements
    '''
    try:
        requirements = []

        with open(file_path) as file:

            requirements = file.readlines()
            requirements = [r.strip() for r in requirements]

            if HYPHEN_E_DOT in requirements :
                requirements.remove(HYPHEN_E_DOT)

            return requirements
    except Exception as e:
        print("File not found error requirements.txt")

print(get_requirements("requirements.txt"))

setup(
    name='Network_Security',
    version='0.0.1',
    author='Harman',
    author_email='hsk9.nahan@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')
)


