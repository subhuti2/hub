% % % a practice for a physics question in high school
% % % A ball vith speed v1 runs after B ball with speed v2 (v1 > v2).
% % % There is a rigid elastic wall behind A ball, which enable A to 
% % % keep its speed but change direction while hitting. The mass of 
% % % B is m times as A. Then how many times can A hit B?
function n = HitBalls(v01, v02, m)

	v1 = v01;
	v2 = v02;
	n = 0;
	while v1 > v2
		n = n + 1;
		[v1, v2] = oneHit(v1, v2, m);
		fprintf('After %d hit(s), v1 = %5.3f; v2 = %5.3f.\n', n, v1, v2);
	end
end

function [v1, v2] = oneHit(v01, v02, m)
	v1 = ((m - 1) * v01 - 2 * m * v02) / (m + 1);
	v2 = (2 * v01 + (m - 1) * v02) / (m + 1);
end
