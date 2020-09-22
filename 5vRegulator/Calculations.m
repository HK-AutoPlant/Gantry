clear all; close all; clc;

Vout       = 5;    %[V]

Vref       = 1.23; %[V]

SwitchFreq = 52;   %[kHz]

% Voltage Divider:


disp(['To aquire reference voltage, R2 = ', num2str(R2), ' Ohm.']);

ET = (Vin - Vout) * Vout/Vin * 1000/SwitchFreq;
L = 100; %[uH]



% Capacitor Selection:

disp(['Output Capacitor Cout >= ', num2str(Cout), ' uF.']);


disp(['The output capacitor must be rated for atleast ', num2str(Vin * 1.5), ' V.']);
disp(['The diode must be rated to handle ', num2str(1.2 * IMax), ' A.']);