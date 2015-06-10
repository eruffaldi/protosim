function setudpsendaddress(ip,port,tag)
%
% Simulink UDP SendTo configurator
%
% setudpsendaddress(ip,port,tag)
%
% All will be set to the given ip and port, untouched if empty array is
% passed. 
% Tag is used to modify only the ones with given Tag
%
% Emanuele Ruffaldi 2010, SSSA-PERCRO
% Rev 1
if nargin < 3
    tag = [];
end
if nargin < 2
    port = [];
end
% maybe in the future: see getfilepaths
if isempty(tag)
    q = find_system(bdroot,'SearchDepth',Inf,'LookUnderMasks','all','BlockType','S-Function','FunctionName','xpcudpbytesend');
else
    q = find_system(bdroot,'SearchDepth',Inf,'LookUnderMasks','all','BlockType','S-Function','FunctionName','xpcudpbytesend','Tag',tag);
end
port =num2str(port);
for j =1:length(q)
    if ~isempty(ip)
        set_param(q{j},'ipAddress',ip);
    end
    if ~isempty(port)
        set_param(q{j},'ipPort',port);
    end
end
