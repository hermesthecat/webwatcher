import os
from distutils.core import setup


def read_file(filename):
    with open(os.path.join(os.path.dirname(__file__), filename)) as file:
        return file.read()


setup(
    name='webwatcher',
    packages=['webwatcher'],
    version='CI_COMMIT_TAG',
    license='MIT',
    description='Convert media files to a modern smaller equivalent.',
    long_description=read_file('README.md'),
    long_description_content_type='text/markdown',
    author='cclloyd',
    author_email='cclloyd@cclloyd.com',
    url='https://gitlab.com/cclloyd1',
    keywords=['media', 'webp', 'webm', 'convert', 'compress'],
    install_requires=[
        'environs',
        'watchdog',
        'ffmpeg-python',
    ],
    python_requires='>=3.8',
    classifiers=[
        # "3 - Alpha"    "4 - Beta"    "5 - Production/Stable"
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Information Technology',
        'Topic :: Multimedia :: Graphics :: Graphics Conversion',
        'Topic :: Multimedia :: Sound/Audio :: Conversion',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3 :: Only',
    ],
)
