clear all; close all; clc;
%% Requirments:
Vout       = 5;    %[V]
Vin        = 24;   %[V]
Vref       = 1.23; %[V]
IMax       = 3;    %[A]
SwitchFreq = 52;   %[kHz]

% Voltage Divider:
R1 = 1000; %[Ohm]
R2 = R1*(Vout/Vref - 1);
disp(['To aquire reference voltage, R2 = ', num2str(R2), ' Ohm.']);
% Inductor Selection:
ET = (Vin - Vout) * Vout/Vin * 1000/SwitchFreq;
L = 100; %[uH]

disp(['ET = ', num2str(ET), ' V * us which gives an inductor value of ', num2str(L), ' uH.']);

% Capacitor Selection:
Cout = 13300 * Vin/(Vout * L);
disp(['Output Capacitor Cout >= ', num2str(Cout), ' uF.']);
disp('');% Facts from datasheet:disp('--- Datasheet Facts ---');
disp('The input Capacitor should be alumininum or tantulum and located close to the regulator, a 100 uF capacitor should suffice.');
disp(['The output capacitor must be rated for atleast ', num2str(Vin * 1.5), ' V.']);
disp(['The diode must be rated to handle ', num2str(1.2 * IMax), ' A.']);
