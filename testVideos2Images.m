% % % Parameter settings
LONG_NAME = 10;

% % % Specify the path to the input video files and output images
inputPath = 'D:\Downloads\t2\t2v\';
outputPath = 'D:\Downloads\t2\t2v2i\';

% % % The tags to read in
theTag = '[DLPanda.com][kkishappyyy]';
n1 = numel(theTag);

% % % The current file ID
tmp = dir([inputPath, '*.txt']);
n2 = str2double(tmp.name(1:end-4));
n3 = n2;

% % % get the files
fNames = dir([inputPath, theTag, '*.mp4']);

% % % Work in a loop to rename 
for iv = 1 : numel(fNames)
	if numel(fNames(iv).name) - n1 < LONG_NAME
		continue;
	else
		n3 = n3 + 1;	%add counter
		% % %	rename	
		fNames(iv).name2 = [theTag, num2str(n3, '%03d'), '.mp4'];
		movefile(fullfile(fNames(iv).folder, fNames(iv).name), ...
				fullfile(fNames(iv).folder, [fNames(iv).name2]));
	end
end
% % % Work in a loop to do the job
% % % dynamic
% imNumLimit = 100;
% imFrameRange = 5;
% imGrayTolerance = 20;
% imPixelTolerance = 1e-3;

% % % k-means
numImages = 50;
maxIterations = 500;
clusterThresh = 0.1;
resizeFlag = 256;

for iv = 1 : numel(fNames)
	% % % get images	
% 		numImage = video2img_static (fullfile(fNames(iv).folder, fNames(iv).name2), ...
% 			outputPath, ['AIab', fNames(iv).name2(n1+1 : end-4)], 100);
% 	numImage = video2img_dynamic (fullfile(fNames(iv).folder, fNames(iv).name), ...
% 		outputPath, ['AIab', fNames(iv).name(n1+1 : end-4)], ...
% 		imNumLimit, imGrayTolerance, imPixelTolerance, imFrameRange);
	numImage = video2img_kmeans (fullfile(fNames(iv).folder, fNames(iv).name), ...
		outputPath, ['AIab', fNames(iv).name(n1+1 : end-4)], ...
		numImages, maxIterations, clusterThresh, resizeFlag);
% 	if numImage > 0 && numImage < imLimit / 2
% 		% % % move the successful ones
% 		movefile(fullfile(fNames(iv).folder, fNames(iv).name), ...
% 			fullfile(fNames(iv).folder, 'extracted', fNames(iv).name));
% 	elseif numImage > imLimit / 2
% 		% % % clean up the failed ones
% 		delete(fullfile(outputPath, ...
% 			['AIab', fNames(iv).name(n1+1 : end-4), '*.jpg']));
% 	end
end
% 
% if n3 > n2
% 	movefile(fullfile(tmp.folder, [num2str(n2), '.txt']), ...
% 			fullfile(tmp.folder, [num2str(n3), '.txt']));
% end
%% below is backup of the first version
% % % % Specify the path to the input video files and output images
% inputPath = 'D:\Downloads\t2\t2v\';
% outputPath = 'D:\Downloads\t2\t2v2i\';
% 
% % % % The tags to read in
% theTag = '[DLPanda.com][aiartbeauty]';
% n1 = numel(theTag);
% 
% % % % % get the files
% % fNames = dir([inputPath, theTag, '*.mp4']);
% % 
% % % % % rename if the name is too long
% % for iv = numel(fNames) : -1 : 1
% % 	if numel(fNames(iv).name) - n1 > 10
% % 		fNames(iv).name2 = [theTag, num2str(iv, '%03d'), '.mp4'];
% % 		movefile(fullfile(fNames(iv).folder, fNames(iv).name), ...
% % 			fullfile(fNames(iv).folder, [fNames(iv).name2, '.mp4']));
% % 	else
% % 		fNames(iv).name2 = fNames(iv).name;
% % 	end
% % end
% 
% % % % get the files
% fNames = dir([inputPath, theTag, '*.mp4']);
% 
% % % % do the extraction
% numImage = zeros(numel(fNames), 1);
% for iv = 1 : numel(fNames)
% 	numImage(iv) = video2img (fullfile(fNames(iv).folder, fNames(iv).name), ...
% 		outputPath, ['AIab', fNames(iv).name(n1+1 : end-4)], 100);
% end
% 
% % % % aftermath
% mkdir([inputPath, 'extracted']);
% for iv = 1 : numel(fNames)
% 	if numImage(iv) > 0
% 	% % % move the successful ones
% 		movefile(fullfile(fNames(iv).folder, fNames(iv).name), ...
% 			fullfile(fNames(iv).folder, 'extracted', fNames(iv).name));
% 	else
% 	% % % clean up the failed ones
% 		delete(fullfile(outputPath, ...
% 			['AIab', fNames(iv).name(n1+1 : end-4), '*.jpg']));
% 	end
% end
% 
% % fNames = dir([outputPath, theTag, '*.jpg']);
% % for iv = 1 : numel(fNames)
% % 	fNames(iv).name2 = ['AIab003_', num2str(iv, '%04d'), '.jpg'];
% % 	movefile(fullfile(fNames(iv).folder, fNames(iv).name), ...
% % 		fullfile(fNames(iv).folder, fNames(iv).name2));
% % end
