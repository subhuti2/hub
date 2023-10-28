% % % This function would read a video and extract the unique theData as images
% % % Each unique image may last multiple theData, but not interleaved
function numResults = video2img_kmeans (vName, iPath, iTag, ...
	numImages, maxIterations, clusterThresh, resizeFlag)

	%% 1. preparation
	numResults = 0;
	
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
	
	if nargin < 4 || isempty(numImages)
		numImages = 50;
	end
	
	if nargin < 5 || isempty(maxIterations)
		maxIterations = 500;
	end
	
	if nargin < 6 || isempty(clusterThresh)
		clusterThresh = 0.1;
	end
	
	if nargin < 7 || isempty(resizeFlag)
		resizeFlag = false;
	end
	
	%% 2. prepare data

	% Create a VideoReader object to read the video
	videoObj = VideoReader(vName);
	

	% initiate data
	nFrames = round(videoObj.Duration * videoObj.FrameRate);
	theData = zeros(videoObj.Height, videoObj.Width, 3, nFrames, 'uint8');
	if resizeFlag
		grayData = zeros(resizeFlag, resizeFlag, nFrames, 'uint8');
	else
		grayData = zeros(videoObj.Height, videoObj.Width, nFrames, 'uint8');
	end

	
	% Read and extract theData from the video
	tic;
	frameCount = 0;
	while hasFrame(videoObj) && frameCount < 1e5
		frameCount = frameCount + 1;
		theData(:, :, :, frameCount) = readFrame(videoObj);
		if resizeFlag
			grayData(:, :, frameCount) = imresize(rgb2gray(theData(:, :, :, frameCount)), ...
				[resizeFlag, resizeFlag]); 
		else
			grayData(:, :, frameCount) = rgb2gray(theData(:, :, :, frameCount));
		end
	if ~mod(frameCount, 100)
			fprintf('.');
		end
	end
	fprintf('\nData read in after %7.2f seconds.\n', toc);

	%% 3. do the work
	tic;
	
	% Reshape the video theData into 2D matrix where each row is a flattened frame
	data = double(reshape(grayData, [], nFrames)');
	clear grayData;

	% Number of clusters to start with
	[cluster_idx, cluster_centroids] = kmeans(data, numImages, 'MaxIter', maxIterations);

	% Calculate pairwise distances between centroids
	D = pdist(cluster_centroids, 'euclidean');
	D = squareform(D);

	while true
		 [i, j] = find(D < clusterThresh & D > 0, 1); % find clusters to merge

		 if isempty(i)
			  break; % Exit loop if no clusters can be merged
		 end

		 % Merge clusters i and j
		 data(cluster_idx == j, :) = cluster_centroids(i, :);
		 cluster_idx(cluster_idx == j) = i;

		 % Re-compute centroids
		 for k = 1 : numImages
			  cluster_data = data(cluster_idx == k, :);
			  cluster_centroids(k, :) = mean(cluster_data, 1);
		 end

		 % Re-compute pairwise distances
		 D = pdist(cluster_centroids, 'euclidean');
		 D = squareform(D);
	end

	% Extract representative index from theData
	unique_clusters = unique(cluster_idx);
	numResults = numel(unique_clusters);
	idxInOrigin = zeros(numResults, 1);
	for k = 1 : numResults
		 theIdx = find(cluster_idx == unique_clusters(k));
		 cluster_data = data(theIdx, :);
		 theDistance = mean(bsxfun(@minus, cluster_data, mean(cluster_data, 1)).^2, 2);
		 [~, tmp] = min(theDistance);
		 idxInOrigin(k) = theIdx(tmp);
		 clear tmp theIdx cluster_data theDistance;
	end	
	clear data cluster_idx cluster_centroids;

	%% 4. extract images
	tic;
	theData = theData(:, :, :, idxInOrigin);
	for fr = 1 : numResults
		outputFilePath = fullfile(iPath, sprintf([iTag, '_%03d.jpg'], fr));
		imwrite(theData(:, :, :, fr), outputFilePath, 'jpg');
	end
	fprintf('%d images were exported after %7.2f seconds.\n', numResults, toc);
	clear theData;
	
	ttt = clock;
	fprintf('\nDone @%02d:%02d:%02d\n', ttt(4:5), floor(ttt(6)));
end