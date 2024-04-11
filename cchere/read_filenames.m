function lines = read_filenames(filename)
    % Open the file for reading
    fid = fopen(filename, 'rt');

    % Check if the file was successfully opened
    if fid == -1
        error('Failed to open file: %s', filename);
    end

    % Initialize an empty cell array to hold the lines
    lines = {};

    % Read the file line by line
    tline = fgetl(fid);
    while ischar(tline)
        % Append the current line to the cell array
        lines{end+1} = tline;
        
        % Read the next line
        tline = fgetl(fid);
    end

    % Close the file
    fclose(fid);

%     % Display the cell array
%     disp(lines);
end
