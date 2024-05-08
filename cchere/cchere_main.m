%% 1. compute cch based on certain text files
% % Define the file name
% f1 = read_filenames('cch1.txt');
% f2 = read_filenames('cch2.txt');
% N = 24;
% 
% for ii = numel(f1) : -1 : 1
% 	t1 = read_time_stamps(['T_', f1{ii}, '.txt']);
% 	h1 = histc(t1, 0:N-1);
% 	h1 = h1 ./ sum(h1);
% 	t2 = read_time_stamps(['T_', f2{ii}, '.txt']);
% 	h2 = histc(t2, 0:N-1);
% 	h2 = h2 ./ sum(h2);
% 	[x1, x2] = corrcoef(h1, h2);
% 	cc(ii) = x1(1, 2);
% 	cp(ii) = x2(1, 2);
% 	cch(:, ii) = xcorr(h1, h2);
% end
% 
% x = -N+1 : N-1;
% bar(x, cch(:, 1));

%% 2. read all cchere data and save into matfiles
% ID_names = convertCharsToStrings(cchere_read('user_in0.txt'))';
% file_names = convertCharsToStrings(cchere_read ('user_out0.txt'))';
% ID = [num2str((1 : numel(ID_names))'), ID_names, file_names];
% for i = numel(file_names) : -1 : 1
% 	t0{i} = convertCharsToStrings(cchere_read(['T_', file_names{i}, '.txt']))';
% 	d0{i} = convertCharsToStrings(cchere_read(['D_', file_names{i}, '.txt']))';
% end
% for i = numel(file_names) : -1 : 1
% 	t{i} = cchere_convert(t0{i}, 'time');
% 	d{i} = cchere_convert(d0{i}, 'date');
% end
% save('./cchere.mat', 'ID', 't', 'd');

%% 3. do the analysis on subset of data
% % % % 3.1 get the distribution, normalized
% HOURS_PER_DAY = 24;
% res = 0.5;
% idx = linspace(0, HOURS_PER_DAY, HOURS_PER_DAY / res + 1);
% for i = numel(t) : -1 : 1
% 	dd(:, i) = histc(t{i}, idx);
% end
% dd(HOURS_PER_DAY / res + 1, :) = [];
% dd = dd ./ sum(dd);
% 
% % % % 3.2 get the correlation and manual check
% for i = numel(t) : -1 : 1
% 	for j = numel(t) : -1 : 1
% 		[x1, x2] = corrcoef(dd(:, i), dd(:, j));
% 		cc(i, j) = x1(1, 2);
% 		cp(j, i) = x2(1, 2);
% 	end
% end
% th = 0.7
% for N = 1 : numel(t)
% 	[ID(cc(N, :) > th, :), cc(cc(N, :) > th, N)]
% 	pause;
% end
% 
% % % 3.3 plot for specified users
% id1 = 18; id2 = 19;
% id1 = 22; id2 = 23;

% id1 = 14; 
% for id2 = [4 7 11 34]
% 	cchere_plot_cch(dd, ID, id1, id2);
% end

% % % 3.4 plot for specified users, in limited time span
% HOURS_PER_DAY = 24;
% res = 0.5;
% idx = linspace(0, HOURS_PER_DAY, HOURS_PER_DAY / res + 1);
% for i = numel(t) : -1 : 1
% 	st = d{i} < 20230000;
% 	dd2(:, i) = histc(t{i}(st), idx);
% end
% dd2(HOURS_PER_DAY / res + 1, :) = [];
% dd2 = dd2 ./ sum(dd2);
% 
% id1 = 14; 
% for id2 = [4 7 11 34]
% 	cchere_plot_cch(dd2, ID, id1, id2);
% end

%%. 4 compare two IDs
id1 = 13; id2 = 18; id3 = 19;
ct = 0;
for iy = 2007 : 2024
	for im = 1 : 12
		ct = ct + 1;
		x1 = iy *10000 + (im - 1) * 100;
		x2 = iy *10000 + im * 100;
		x0(4, ct) = x2 / 100;
		x0(1, ct) = sum(d{id1} <= x2 & d{id1} > x1);
		x0(2, ct) = sum(d{id2} <= x2 & d{id2} > x1);
		x0(3, ct) = sum(d{id3} <= x2 & d{id3} > x1);
	end
end
x1 = x0(1, 109:end);
x2 = sum(x0(2:3, 109:end));


function cchere_plot_cch(dd, ID, id1, id2)
	addpath('C:\Users\peng_\git\weg\0fun\export_fig');
	M0 = max([dd(:, id1); dd(:, id2)]);
	M = ceil(M0 * 50)/50;

	p = polyfit(dd(:, id1), dd(:, id2), 1);
	x = [0 M];
	y = polyval(p, x);
	[x1, x2] = corrcoef(dd(:, id1), dd(:, id2));

	clf;
	figure('color', [1 1 1]);
	h1 = plot(dd(:, id1), dd(:, id2), 'c.', 'markersize', 30);
	hold on;
	h2 = plot(x, y, 'r-', 'linewidth', 2);
	text(0.7*M, 0.5*M, ['\itr = ', num2str(x1(1, 2), '%0.2f')], 'fontsize', 36);
	axis equal;
	set(gca, 'xlim', [-0.01 M+0.01], 'ylim', [-0.01 M+0.01], 'xtick', [0 M/2 M], 'ytick', [0 M/2 M], ...
		'fontsize', 20);
% 	h3 = xlabel(ID{id1, 2}, 'Position', [0.75 * M, -0.012, -1]);
% 	h4 = ylabel(ID{id2, 2}, 'Position', [-0.012, 0.75 * M, -1]);
	fname = [ID{id1, 2}, '_', ID{id2, 2}, '.png'];
	export_fig(fname);
end	
