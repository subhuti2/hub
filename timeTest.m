% % % a practice for a timing test
% % % 1. read data and check
raw = load('./time.txt');
time(:, 3:4) = raw(2:end, 1:2);
time(:, 1:2) = raw(1:end-1, 3:4);
minute = mod(time, 100);
hour = floor(time/100);

X = hour(:, 1) < 20 | hour(:, 2) < 20 | hour(:, 3) > 12 | ...
	hour(:, 4) > 12 | minute(:, 1) > 59 | minute(:, 2) > 59 | ...
	minute(:, 3) > 59 | minute(:, 4) > 59;
Y = find(X);time(Y, :)

timec = time;
XXX = Y([7 16 18 23 33]);
timec(Y([3, 4]), 2) = timec(Y([3, 4]), 2) + 2400;
timec(Y(12), 1:2) = timec(Y(12), 1:2) + 2400;
timec(Y(15), 1:2) = timec(Y(15), 1:2) + 2400;
timec(XXX, :) = [];
minutec = mod(timec, 100);
hourc = floor(timec/100);
clear X Y XXX;

sleep0 = (hourc(:, 3) - hourc(:, 2) + 24) * 60 + ...
	minutec(:, 3) - minutec(:, 2);
sleep1 = (hourc(:, 4) - hourc(:, 1) + 24) * 60 + ...
	minutec(:, 4) - minutec(:, 1);
delay1 = (hourc(:, 2) - hourc(:, 1)) * 60 + minutec(:, 2) - minutec(:, 1);
delay2 = (hourc(:, 4) - hourc(:, 3)) * 60 + minutec(:, 4) - minutec(:, 3);

timex = timec;
X = sleep0 < 0 | delay1 < 0 | delay2 < 0;
Y = find(X);timex(Y, :)
timex(Y, :) = [];
minutex = mod(timex, 100);
hourx = floor(timex/100);
clear X Y;

startc = (hourx(:, 1)-24) * 60 + minutex(:, 1);
endc = hourx(:, 4) * 60 + minutex(:, 4);
sleep0 = (hourx(:, 3) - hourx(:, 2) + 24) * 60 + ...
	minutex(:, 3) - minutex(:, 2);
sleep1 = (hourx(:, 4) - hourx(:, 1) + 24) * 60 + ...
	minutex(:, 4) - minutex(:, 1);
delay1 = (hourx(:, 2) - hourx(:, 1)) * 60 + minutex(:, 2) - minutex(:, 1);
delay2 = (hourx(:, 4) - hourx(:, 3)) * 60 + minutex(:, 4) - minutex(:, 3);

clf; 
bar(sleep0/60); 
hold on; 
plot(smooth(sleep0/60, 30), 'linewidth', 3);
plot(smooth(sleep1/60, 30), 'linewidth', 3);

clf; 
plot(smooth(delay1/60, 30), 'linewidth', 3);
hold on;
plot(smooth(delay2/60, 30), 'linewidth', 3);

