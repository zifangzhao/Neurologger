% function WILD_PreProcessFolder(path)
folders = genpath(pwd);
folders = strsplit(folders,';');
pth = pwd;
for idx=1:length(folders)
   
    info_file = dir(fullfile(folders{idx}, 'CE_params.bin'));
    amp_file = dir(fullfile(folders{idx}, 'amplifier.dat'));
    imu_file = dir(fullfile(folders{idx}, 'IMU.mat'));
    if(~isempty(info_file)&~isempty(amp_file)&isempty(imu_file))
        fprintf('Progress:%.01f %s\n',100*idx/length(folders),folders{idx});
        
        cd(folders{idx});
        WILD_PreProcess(fullfile(folders{idx}, 'amplifier.dat'),[],0,0);
    end
end
cd(pth)
    
    