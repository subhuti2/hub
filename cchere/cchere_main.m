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
ID_names = convertCharsToStrings(cchere_read('user_in0.txt'));
file_names = cchere_read ('user_out0.txt');
for i = numel(f1) : -1 : 1
	t0{i} = convertCharsToStrings(cchere_read(['T_', file_names{i}, '.txt']))';
	d0{i} = convertCharsToStrings(cchere_read(['D_', file_names{i}, '.txt']))';
end
for i = numel(f1) : -1 : 1
	t{i} = cchere_convert(t0{i}, 'time');
	d{i} = cchere_convert(d0{i}, 'date');
end
save('./cchere.mat', 'ID_names', 't', 'd', 't0', 'd0');
