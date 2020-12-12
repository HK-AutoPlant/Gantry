function savepic(SAVE,larger,str,format) 
% Function that saves pictures. SAVE = 1 to save!
% larger = 1 to enlarge
% str is the string to where on the hard drive
% it is suppose to save the picture in question.
% Can be used to just adjust graphic and font size too
if larger == 1
fig = get(groot,'CurrentFigure');
figNumber = fig.Number;
figure(figNumber)

set(gca,'fontsize',20)
     width=1310;
     height=750;
     set(gcf,'units','points','position',[10,10,width,height])
end
if SAVE==1
saveas(gcf,str,format);
end
end