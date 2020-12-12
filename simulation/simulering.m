
LineW = 2;
StopTime = 1;

% Parameters for screw-nut
threadHalfAngle_vec = 15;%[10, 12, 14.5, 16, 20, 25]; % 14.5 = std
Lead_vec = [6e-3];
dm = (12- 0.5*3)*10^(-3);% 25mm mean diameter
LeadAngle_vec = atand(Lead_vec./(pi*dm));
%%
out = sim('leadscrewStepper','StopTime',num2str(StopTime));
figure(1)
plot(out.force.Time, out.force.Data,'Linewidth',LineW)
xlabel('Time [s]')
ylim([620 625])
ylabel('Force [N]')
legend('Force')
grid on
title('Resulting lifting force from Z-axis stepper motor')
savePath=strcat('C:\Users\minim\Google Drive\Kth\Hk autoplant p3,p4\Force','');
savepic(1,1,savePath,'epsc');%'epsc'
%%
for threadHalfAngle = threadHalfAngle_vec
    
out = sim('leadscrewStepper','StopTime',num2str(StopTime));
% Comparing Velocity
figure(1)
plot(out.torque.Time, out.torque.Data,'Linewidth',LineW)
xlabel('Time [s]')
ylabel('Torque[Nm]')
legend('S.S','TF','Block','Simscape')
grid on
savePathT=strcat('C:\Users\minim\Google Drive\Kth\MEX\simulink\Mex-Simulering\Pictures\TorqueAngle',num2str(threadHalfAngle));
savepic(1,1,savePathT,'svg');

figure(2)
plot(out.current.Time, out.current.Data,'Linewidth',LineW)
xlabel('Time [s]')
ylabel('Current [A]')
legend('Current')
grid on
title(['\alpha = ',num2str(threadHalfAngle)])
savePath=strcat('C:\Users\minim\Google Drive\Kth\MEX\simulink\Mex-Simulering\Pictures\CurrentAngle',num2str(threadHalfAngle));
savepic(1,1,savePath,'svg');%'epsc'

end