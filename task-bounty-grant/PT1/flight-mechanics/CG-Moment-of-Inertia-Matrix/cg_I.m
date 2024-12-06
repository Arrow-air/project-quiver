clc;clear;
format short g;
%% Units: grams, cm, g*cm^2

%% Without Payload
m_old = 18000;
cg_old = [0	0	3.36];
I_old = [1.2402e+07	793.57	-39876
793.57	1.225e+07	-349.24
-39876	-349.24	2.1709e+07];

%% Add weight
m_add = 4000;
cg_add = [0,0,-20]; % origin is center of thrust

%% Calculate new parameters
m_new = m_old+m_add;
cg_new = (m_old*cg_old+m_add*cg_add)/m_new;
cg_shift = cg_new-cg_old;
I_old_shifted = I_old+m_old*(norm(cg_shift)^2*eye(3)-transpose(cg_shift)*cg_shift);
cg_add_dist = cg_add-cg_new;
I_new = I_old_shifted+m_add*(norm(cg_add_dist)^2*eye(3)-transpose(cg_add_dist)*cg_add_dist);

