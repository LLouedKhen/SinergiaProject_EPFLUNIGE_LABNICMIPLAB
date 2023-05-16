 for i = 1:length(Emotions')
    
    if i < 10
        emNum = ['0',num2str(i)];
        emCN{i,1} = emNum;
    else 
        emNum = num2str(i);
        emCN{i,1} = emNum;
    end
    
 end
 
 EmAndNum = [Emotions', emCN];

 for i= 1:height(drop)
     emoDrop = extractBetween(drop.MovEmo{i},', ', ')');
     sDrop = emoDrop{1}(2:end-1);
     relInd = find(strcmp(Emotions,sDrop));
     dropCon = ['con_0', EmandNum(relInd,2)]
     drop.MovEmo{i} = insertBefore(drop.MovEmo{i},')',  dropCon);
 end
