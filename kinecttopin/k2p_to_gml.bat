@echo off

cd %~dp0

set INPUT=%1
set OUTPUT=%~dp1
rem all, head, neck, torso, l_shoulder, l_elbow, l_hand, r_shoulder, r_elbow, r_hand, l_hip, l_knee, l_foot, r_hip, r_knee, r_foot
set JOINTS=r_hand

python k2p_to_gml.py -- %INPUT% %OUTPUT% %JOINTS%

@pause