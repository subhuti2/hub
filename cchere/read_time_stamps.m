function hours = read_time_stamps(filename)
% Open the file for reading
	fid = fopen(filename, 'rt');

	% Check if the file was successfully opened
	if fid == -1
		 error('Failed to open file: %s', filename);
	end

	% Initialize an empty cell array to hold the lines
	times = {};

	% Read the file line by line
	tline = fgetl(fid);
	while ischar(tline)
		 % Append the current line to the cell array
		 times{end+1} = tline;

		 % Read the next line
		 tline = fgetl(fid);
	end

	% Close the file
	fclose(fid);

	% Initialize an array to hold the times in hours
	hours = zeros(length(times), 1);

	% Convert each time to decimal hours
	for i = 1:length(times)
		 % Split the time string into hours, minutes, and seconds
		 timeParts = strsplit(times{i}, ':');
		 hourPart = str2double(timeParts{1});
		 minutePart = str2double(timeParts{2});
		 secondPart = str2double(timeParts{3});

		 % Calculate the total hours as decimal
		 hours(i) = hourPart + minutePart / 60 + secondPart / 3600;
	end

	% Display the converted times
% 	disp(hours);
end