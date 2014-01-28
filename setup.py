#!/usr/bin/python2

from distutils.core import setup
setup(
    name="VoIP.py",
    version="0.1",
    description="A highly re-configurable VoIP-Client framework using PJSIP.",
    author=["Frank Haase", "Dennis Guse"],
    packages = ['', 'Defines', 'SIPController', 'Modules', 'Modules/CallModules', 'Modules/ConfigModules', 'Modules/MainCliModules', 'Modules/MainUIModules', 'Modules/UIModules', 'Modules/PresenceModules'],
    package_data={'' : ['UIElements/*', 'Resources/*']},
    license='GNU GPL',
)
