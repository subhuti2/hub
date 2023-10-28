% % % This function would read a video and extract the unique frames as images
% % % Each unique image may last multiple frames, but not interleaved
function nFrames1 = video2img_dynamic (vName, iPath, iTag, ...
	cutoffImageNumber, diffThreshGray, diffThreshCount, framesRange)

	%% 1. preparation
	CUTOFF_IMAGE_NUMBER = 100;	%at most how many images may be extracted from a video
	DIFF_THRESH_GRAY = 20;	%at most how many gray scale difference are tolerated
	DIFF_THRESH_COUNT = 1e-3;	%how many pixels may be different when considered as equal
	TOLERANCE_DISTANCE_IN_FRAMES = 2;	%+/- this number of frames are equal, then keep
	
	nFrames1 = -1;
	if nargin < 2
		fprintf ('Please specify the input video file and output image path!\n');
		return;
	else
		if ~exist(vName, 'file')
			fprintf('The input file does not exist!\n');
			return;
		elseif ~exist(iPath, 'dir')
			makedir(iPath);
			fprintf('Output folder does not exist, created!\n')
		end
	end

	if nargin < 3 || isempty(iTag)
		iTag = 'frame';
	end
	
	if nargin < 4 || isempty(cutoffImageNumber)
		cutoffImageNumber = CUTOFF_IMAGE_NUMBER;
	end
	
	if nargin < 5 || isempty(diffThreshGray)
		diffThreshGray = DIFF_THRESH_GRAY;
	end
	
	if nargin < 6 || isempty(diffThreshCount)
		diffThreshCount = DIFF_THRESH_COUNT;
	end
	
	if nargin < 7 || isempty(framesRange)
		framesRange = TOLERANCE_DISTANCE_IN_FRAMES;
	end
	%% 2. do the work

	% Create a VideoReader object to read the video
	videoObj = VideoReader(vName);
	

	% initiate data
	nFrames = round(videoObj.Duration * videoObj.FrameRate);
	theData = zeros(videoObj.Height, videoObj.Width, 3, nFrames, 'uint8');
	grayData = zeros(videoObj.Height, videoObj.Width, nFrames, 'uint8');

	
	% Read and extract frames from the video
	tic;
	frameCount = 0;
	while hasFrame(videoObj) && frameCount < 1e5
		frameCount = frameCount + 1;
		theData(:, :, :, frameCount) = readFrame(videoObj);
		grayData(:, :, frameCount) = rgb2gray(theData(:, :, :, frameCount));
		if ~mod(frameCount, 100)
			fprintf('.');
		end
	end
	fprintf('\nData read in after %7.2f seconds.\n', toc);
	
% 	d1 = theData;
% 	d2 = grayData;
% 	theData = d1;
% 	grayData = d2;

	% set parameters
% 	tic;
	diffThreshCount = videoObj.Height * videoObj.Width * diffThreshCount;
% 	fprintf('\nData checked after %7.2f seconds.\n', toc);

% 	diffThreshCount = 300;
% 	diffThreshGray = 10;
	% % % 	for i = 1 : 	nFrames
	% % % 			grayData(:, :, i) = rgb2gray(theData(:, :, :, i));
	% % % 	end
	
	% % % get the stable frames	
	tic;
	imageStableFlag = false(nFrames, 1);
	for fr = framesRange + 1 : nFrames - framesRange
		flag = false(framesRange, 1);
		for cf = 1 : framesRange
			theDiff = abs(double(grayData(:, :, fr + cf)) - ...
				double(grayData(:, :, fr - cf))) > diffThreshGray;
			flag(cf) = sum(theDiff(:)) < diffThreshCount;
		end
		if all(flag)
			imageStableFlag(fr) = true;
		end
	end
	theData = theData(:, :, :, imageStableFlag);
	grayData = grayData(:, :, imageStableFlag);
	nFrames2 = size(grayData, 3);
	fprintf('%d of %d were classified after %7.2f seconds.\n', nFrames2, nFrames, toc);
	
	% % % remove the duplicate frames	
	tic;
	imageDuplicateFlag = false(nFrames2, 1);
	for fr = 2 : nFrames2
		theDiff = abs(double(grayData(:, :, fr)) - ...
			double(grayData(:, :, fr - 1))) > diffThreshGray;
		if sum(theDiff(:)) < diffThreshCount
			imageDuplicateFlag(fr) = true;
		end
	end
	clear grayData;
	theData = theData(:, :, :, ~imageDuplicateFlag);
	nFrames1 = size(theData, 4);
	fprintf('%d of %d images were selected after %7.2f seconds.\n', nFrames1, nFrames2, toc);
	
	% % % export the images
	tic;
	if nFrames1 > cutoffImageNumber
		tmp = randperm(nFrames1);
		idx = sort(tmp(1 : cutoffImageNumber));
		theData = theData(:, :, :, idx);
		nFrames1 = cutoffImageNumber;
	end
	
	for fr = 1 : nFrames1
		outputFilePath = fullfile(iPath, sprintf([iTag, '_%03d.jpg'], fr));
		imwrite(theData(:, :, :, fr), outputFilePath, 'jpg');
	end
	fprintf('%d images were exported after %7.2f seconds.\n', nFrames1, toc);
	clear theData;

	ttt = clock;
	fprintf('\nDone @%02d:%02d:%02d\n', ttt(4:5), floor(ttt(6)));
end