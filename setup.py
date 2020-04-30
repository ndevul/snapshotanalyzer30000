from setuptools import setup

setup(
    name = 'SnapshotAnalyzer',
    version = '0.1',
    author = 'JohnDoe',
    description = 'Snapshot Analyzer is a tool to manage EC2 snapshots',
    licence = 'GPLv3+',
    packages = ['shotty'],
    url = 'https://github.com/ndevul/snapshotanalyzer30000',
    install_required = [
        'boto3',
        'click'
    ],
    entry_point = '''
        [console_scripts]
        shotty = shotty.shotty.cli
    ''',

)
