function [sysParam,dspParam] = WILD_ReadHeader(filename)
if nargin <1
    [filename,p] = uigetfile('CE_params.bin');
    filename = fullfile(p,filename);
end
% Open the binary file for reading
fid = fopen(filename, 'rb');

if fid == -1
    error('Failed to open the file.');
end

fseek(fid,0,'eof');
bytes= ftell(fid);
Ndsp = bytes/512-1;

fseek(fid,440,'bof');
sysParam.data_version = fread(fid,1,'uint8');
fseek(fid,0,'bof');
% Read the sysParam
if(sysParam.data_version==0)
    sysParam.fs = fread(fid, 1, 'uint32');                % 4 bytes
    sysParam.AUX_mode = fread(fid, 1, 'uint32');          % 4 bytes
    sysParam.Nch = fread(fid, 1, 'uint32');               % 4 bytes
    sysParam.convCmd = fread(fid, 64, 'uint16');          % 64*2 bytes
    sysParam.dispCH = fread(fid, 1, 'uint32');            % 4 bytes
    sysParam.func1 = fread(fid, 1, 'uint32');             % 4 bytes
    sysParam.func2 = fread(fid, 1, 'uint32');             % 4 bytes
    sysParam.cmd_ch = fread(fid, 1, 'uint32');            % 4 bytes
    sysParam.rec_ch = fread(fid, 1, 'uint32');            % 4 bytes
    sysParam.stim_mode = fread(fid, 1, 'uint32');         % 4 bytes
    sysParam.cl_mode = fread(fid, 1, 'uint32');           % 4 bytes
    sysParam.stim_interval = fread(fid, 4, 'uint32')/10;     % 4*4 bytes
    sysParam.pulse_width = fread(fid, 4, 'uint32');       % 4*4 bytes
    sysParam.pulse_cnt = fread(fid, 4, 'uint32');         % 4*4 bytes
    sysParam.stim_delay = fread(fid, 4, 'uint32');        % 4*4 bytes
    sysParam.stim_RndDelay = fread(fid, 4, 'uint32');     % 4*4 bytes
    sysParam.trigger_trainStart = fread(fid, 1, 'uint32');% 4 bytes
    sysParam.trigger_trainDuration = fread(fid, 1, 'uint32'); % 4 bytes
    sysParam.trigger_gain = fread(fid, 4, 'float32');     % 4*4 bytes
    sysParam.SD_capacity = fread(fid, 1, 'uint32');       % 4 bytes
    sysParam.LED_pulse_CNT = fread(fid, 1, 'uint32');     % 4 bytes
    sysParam.preview_channel_bank = fread(fid, 1, 'uint32'); % 4 bytes
    sysParam.system_status = fread(fid, 1, 'uint32');     % 4 bytes
    sysParam.stim_intensity = fread(fid, 4, 'uint32');    % 4*4 bytes
    sysParam.stim_ch = fread(fid, 4, 'uint32');           % 4*4 bytes
    sysParam.MISC_ratio = fread(fid, 1, 'uint8');         % 1 byte
    sysParam.PREV_ratio = fread(fid, 1, 'uint8');         % 1 byte
    sysParam.MISC_interval = fread(fid, 1, 'uint16');     % 2 bytes
    sysParam.error_code = fread(fid, 1, 'uint32');        % 4 bytes
    sysParam.firmware_version = fread(fid, 1, 'uint16');  % 2 bytes
    sysParam.hw_version = fread(fid, 1, 'uint16');        % 2 bytes
    sysParam.date = fread(fid, 1, 'uint32');              % 4 bytes
    sysParam.time = fread(fid, 5, 'uint32');              % 5*4 bytes (assuming RTC_TimeTypeDef is 20 bytes)
    sysParam.MAC =  sprintf('%02X:', fread(fid, 8, 'uint8'));                % 8 bytes
    sysParam.Vbatt_threshold = fread(fid, 1, 'uint16');   % 2 bytes
    sysParam.unassigned_16 = fread(fid, 1, 'uint16');     % 2 bytes
    sysParam.unassigned = fread(fid, 36, 'uint32');       % 36*4 bytes
    sysParam.sampling_rate =[0,0,0,0];
else
    sysParam.fs = fread(fid, 1, 'uint32');                % 4 bytes
    sysParam.AUX_mode = fread(fid, 1, 'uint32');          % 4 bytes
    sysParam.Nch_each = fread(fid, 8, 'uint16');
    sysParam.Nch= sysParam.Nch_each(1);
    sysParam.spd_rate = fread(fid, 8, 'uint16');
    sysParam.sampling_rate = fread(fid, 8, 'uint32');
    sysParam.channellist = fread(fid, 64, 'uint8');
    fread(fid,1,'uint32'); %unassigned
    sysParam.dispCH = fread(fid, 1, 'uint32');            % 4 bytes
    sysParam.func1 = fread(fid, 1, 'uint32');             % 4 bytes
    sysParam.func2 = fread(fid, 1, 'uint32');             % 4 bytes
    sysParam.cmd_ch = fread(fid, 1, 'uint32');            % 4 bytes
    sysParam.rec_ch = fread(fid, 1, 'uint32');            % 4 bytes
    sysParam.stim_mode = fread(fid, 1, 'uint32');         % 4 bytes
    sysParam.cl_mode = fread(fid, 1, 'uint32');           % 4 bytes
    sysParam.stim_interval = fread(fid, 4, 'uint32')/10;     % 4*4 bytes
    sysParam.pulse_width = fread(fid, 4, 'uint32');       % 4*4 bytes
    sysParam.pulse_cnt = fread(fid, 4, 'uint32');         % 4*4 bytes
    sysParam.stim_delay = fread(fid, 4, 'uint32');        % 4*4 bytes
    sysParam.stim_RndDelay = fread(fid, 4, 'uint32');     % 4*4 bytes
    sysParam.trigger_trainStart = fread(fid, 1, 'uint32');% 4 bytes
    sysParam.trigger_trainDuration = fread(fid, 1, 'uint32'); % 4 bytes
    sysParam.trigger_gain = fread(fid, 4, 'float32');     % 4*4 bytes
    sysParam.SD_capacity = fread(fid, 1, 'uint32');       % 4 bytes
    sysParam.LED_pulse_CNT = fread(fid, 1, 'uint32');     % 4 bytes
    sysParam.preview_channel_bank = fread(fid, 1, 'uint32'); % 4 bytes
    sysParam.system_status = fread(fid, 1, 'uint32');     % 4 bytes
    sysParam.stim_intensity = fread(fid, 4, 'uint32');    % 4*4 bytes
    sysParam.stim_ch = fread(fid, 4, 'uint32');           % 4*4 bytes
    sysParam.MISC_ratio = fread(fid, 1, 'uint8');         % 1 byte
    sysParam.PREV_ratio = fread(fid, 1, 'uint8');         % 1 byte
    sysParam.MISC_interval = fread(fid, 1, 'uint16');     % 2 bytes
    sysParam.error_code = fread(fid, 1, 'uint32');        % 4 bytes
    sysParam.firmware_version = fread(fid, 1, 'uint16');  % 2 bytes
    sysParam.hw_version = fread(fid, 1, 'uint16');        % 2 bytes
    sysParam.date = fread(fid, 1, 'uint32');              % 4 bytes
    sysParam.time = fread(fid, 5, 'uint32');              % 5*4 bytes (assuming RTC_TimeTypeDef is 20 bytes)
    sysParam.MAC =  sprintf('%02X:', fread(fid, 8, 'uint8'));                % 8 bytes
    sysParam.Vbatt_threshold = fread(fid, 1, 'uint16');   % 2 bytes
    sysParam.unassigned_16 = fread(fid, 1, 'uint16');     % 2 bytes
    sysParam.unassigned = fread(fid, 36, 'uint32');       % 36*4 bytes
end
sysParam.rec_time = RTC_to_datetime(sysParam);
dspParam = cell(Ndsp,1);
for didx=1:Ndsp
    fseek(fid,512*didx,'bof');
    dsp=[];
    dsp.chOrd  = fread(fid,128,'uint8');
    dsp.formula = fread(fid, 1, 'uint8');
    dsp.func1 = fread(fid, 1, 'uint8');
    dsp.func2 = fread(fid, 1, 'uint8');
    dsp.MAOrd1 = fread(fid, 1, 'uint8');
    dsp.filter1 = fread(fid, 46, 'float');
    dsp.filter2 = fread(fid, 46, 'float');
    dspParam{didx}=dsp;
end

% Close the file
fclose(fid);
end


function dt = RTC_to_datetime(sysParam)
% Convert STM32 RTC fields to MATLAB datetime

% Decode date
b = typecast(uint32(sysParam.date), 'uint8');
weekday = b(1);
month   = b(2);
day     = b(3);
year    = 2000 + double(b(4));

% Decode time
tbytes = typecast(uint32(sysParam.time), 'uint8');
hours   = tbytes(1);
minutes = tbytes(2);
seconds = double(tbytes(3));

tbytes_32 = typecast(uint32(sysParam.time), 'uint32');
ssr = tbytes(2);
SecondFraction = 9999;  
fractional_seconds  = double(SecondFraction - ssr) / double(SecondFraction + 1);
% Build datetime
dt = datetime(year, month, day, hours, minutes, seconds+fractional_seconds );

% Optional fractional correction
% SubSeconds = sysParam.time(2);
% SecondFraction = sysParam.time(3);
% dt = dt + seconds(-double(SubSeconds) / double(SecondFraction));
end


