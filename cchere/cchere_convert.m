function out = cchere_convert(in, type)
	% Initialize an array to hold the in data
	out = zeros(length(in), 1);

	if strcmp(type, 'time')
		% Convert each time to decimal hours
		for i = 1:length(in)
			 % Split the time string into hours, minutes, and seconds
			 timeParts = strsplit(in{i}, ':');
			 hourPart = str2double(timeParts{1});
			 minutePart = str2double(timeParts{2});
			 secondPart = str2double(timeParts{3});

			 % Calculate the total hours as decimal
			 out(i) = hourPart + minutePart / 60 + secondPart / 3600;
		end
	elseif strcmp(type, 'date')
		% Convert each time to decimal hours
		for i = 1:length(in)
			 % Split the time string into hours, minutes, and seconds
			 timeParts = strsplit(in{i}, '-');
			 hourPart = str2double(timeParts{1});
			 minutePart = str2double(timeParts{2});
			 secondPart = str2double(timeParts{3});

			 % Calculate the total hours as decimal
			 out(i) = hourPart*10000 + minutePart*100 + secondPart;
		end
	else
		fprintf('Unknown data type!\n');
		out = in;
	end
	
	% Display the converted in
	% disp(out);
end