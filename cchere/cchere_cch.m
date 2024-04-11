
% Define the file name
f1 = read_filenames('cch1.txt');
f2 = read_filenames('cch2.txt');
N = 24;

for ii = numel(f1) : -1 : 1
	t1 = read_time_stamps(['T_', f1{ii}, '.txt']);
	h1 = histc(t1, 0:N-1);
	h1 = h1 ./ sum(h1);
	t2 = read_time_stamps(['T_', f2{ii}, '.txt']);
	h2 = histc(t2, 0:N-1);
	h2 = h2 ./ sum(h2);
	[x1, x2] = corrcoef(h1, h2);
	cc(ii) = x1(1, 2);
	cp(ii) = x2(1, 2);
	cch(:, ii) = xcorr(h1, h2);
end

x = -N+1 : N-1;
bar(x, cch(:, 1));

