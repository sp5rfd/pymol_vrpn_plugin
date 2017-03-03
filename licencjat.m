% wczytanie pliku mapowania i struktur pdb
structure=pdbread('1fg0.pdb');
template=pdbread('helix.pdb');
mappingCells=textscan(fopen('1fg0_helix.txt'),'%s %s');
mappingKey=cell2mat(mappingCells{2});
mappingValue=str2num(cell2mat(mappingCells{1}));



