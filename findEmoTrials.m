clear; clc;

datapath =  '/media/miplab-nas2/Data2/Movies_Emo/Leyla';

load AllEmoTables_EmoTable

keep = zeros(height(allEmoTables), 1);
for i = 1:height(allEmoTables)
    if isempty(strfind(allEmoTables{i,:}, 'Emotion'))
        keep(i) = 0;
    else 
        keep(i) = 1;
    end
end

tEmoT = allEmoTables(keep,:);