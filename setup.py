from setuptools import setup, find_packages
import os


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name='baruwa',
      version="1.1.0",
      description="Ajax enabled MailScanner web frontend",
      long_description=read('README'),
      keywords='MailScanner Email Filters Quarantine Spam',
      author='Andrew Colin Kissa',
      author_email='andrew@topdog.za.net',
      url='http://www.topdog.za.net/baruwa',
      license='GPL',
      packages=find_packages('src'),
      package_dir = {'': 'src'},
      include_package_data=True,
      zip_safe=False,
      dependency_links = [],
      install_requires=['setuptools',
        'Django>= 1.2.0',
        'django-celery',
        'MySQL-python>=1.2.1p2',
        'reportlab',
        'anyjson',
        #'GeoIP',
        'iPy',
        'lxml',
      ],
      classifiers = ['Development Status :: 5 - Production/Stable',
                   'Environment :: Web Environment',
                   'Framework :: Django',
                   'Intended Audience :: System Administrators',
                   'Intended Audience :: Information Technology',
                   'Intended Audience :: Telecommunications Industry',
                   'Intended Audience :: Customer Service',
                   'License :: OSI Approved :: GNU General Public License (GPL)',
                   'Natural Language :: English',
                   'Operating System :: POSIX :: Linux',
                   'Operating System :: POSIX :: BSD',
                   'Operating System :: POSIX :: SunOS/Solaris',
                   'Programming Language :: Python :: 2',
                   'Programming Language :: Python :: 2.4',
                   'Programming Language :: Python :: 2.5',
                   'Programming Language :: Python :: 2.6',
                   'Programming Language :: Python :: 2.7',
                   'Topic :: Internet :: WWW/HTTP',
                   'Topic :: Communications :: Email :: Filters',
                   'Topic :: System :: Monitoring',
                   'Topic :: Multimedia :: Graphics :: Presentation',
                   'Topic :: System :: Systems Administration',
                   ],
      )
