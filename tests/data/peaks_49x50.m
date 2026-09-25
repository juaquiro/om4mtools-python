x_vec=linspace(-3, 3, 50);
y_vec=linspace(-3, 3, 49);
[x,y]=meshgrid(x_vec,y_vec);

z =  3*(1-x).^2.*exp(-(x.^2) - (y+1).^2) ... 
   - 10*(x/5 - x.^3 - y.^5).*exp(-x.^2-y.^2) ... 
   - 1/3*exp(-(x+1).^2 - y.^2) ;

 writematrix(z, 'peaks_49x50.csv');
