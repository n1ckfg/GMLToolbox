@echo off

cd %~dp0

set INPUT=%1
set OUTPUT=%~dp1

python gml_to_painter.py -- %INPUT% %OUTPUT%

@pause