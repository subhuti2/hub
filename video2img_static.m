% % % This function would read a video and extract the unique frames as images
% % % Each unique image may last multiple frames, but not interleaved

% % % This works for those videos with static images but not for dynamic

function imageCount = video2img_static (vName, iPath, iTag, ...
	cutoffImageNumber, diffThreshGray, diffThreshCount)

	%% 1. preparation
	CUTOFF_IMAGE_NUMBER = 100;
	DIFF_THRESH_GRAY = 30;
	DIFF_THRESH_COUNT = 5000;
	
	imageCount = -1;
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

	if nargin < 3
		iTag = 'frame';
	end
	
	if nargin < 4
		cutoffImageNumber = CUTOFF_IMAGE_NUMBER;
	end
	
	if nargin < 5
		diffThreshGray = DIFF_THRESH_GRAY;
	end
	
	if nargin < 6
		diffThreshCount = DIFF_THRESH_COUNT;
	end
	%% 2. do the work

	% Create a VideoReader object to read the video
	videoObj = VideoReader(vName);

	% Read and extract frames from the video
	frameCount = 0;
	imageCount = 0;
	while hasFrame(videoObj)
		isUnique = false;
		frameCount = frameCount + 1;
		currentFrame = readFrame(videoObj);
		
		if frameCount > 1	% No need to compare for first frame
			% Convert the frame to grayscale to improve frame matching
			grayFrame = rgb2gray(currentFrame);
			diff = sum(abs(double(previousFrame(:)) - double(grayFrame(:))) > ...
				diffThreshGray);
% 			if diff
% 				fprintf('% d', diff);
% 			end
			if diff > diffThreshCount
				isUnique = true;
				previousFrame = grayFrame;
				fprintf('% d', diff);
			end
		else
			isUnique = true;
			previousFrame = rgb2gray(currentFrame);
		end

		% If the frame is unique, save it as a JPEG image
		if isUnique
			outputFilePath = fullfile(iPath, sprintf([iTag, '_%d.jpg'], frameCount));
			imwrite(currentFrame, outputFilePath, 'jpg');
			ttt = clock;
			fprintf('\nImage %d extracted @%02d:%02d:%02d\n', frameCount, ...
				ttt(4:5), floor(ttt(6)));
			imageCount = imageCount + 1;
			if imageCount > cutoffImageNumber
				imageCount = -1;
				return;
			end
		end
	end
	fprintf('\nProcess done!\n')
end