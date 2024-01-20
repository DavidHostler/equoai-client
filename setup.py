import setuptools

setuptools.setup(
    name='equoai',
    version='1.0.0',
    author='David Hostler',
    description='Python client for accessing the EquoAI platform and all its core services',
    packages=['equoai'],
    download_url = 'https://github.com/DavidHostler/equoai-client',    # I explain this later on
    install_requires=[            # I get to this in a second
          'torch',
          'sentence_transformers',
          'requests',
          'tiktoken'
      ],
)
