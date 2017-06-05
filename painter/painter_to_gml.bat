@echo off

cd %~dp0

set INPUT=%1
set OUTPUT=%~dp1

python painter_to_gml.py -- %INPUT% %OUTPUT%

@pause