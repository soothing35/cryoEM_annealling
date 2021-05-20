function res = writeBINARYtoSPIDER(nClass,nPix,dir,senses,psinums,pcase)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Copyright (c) 2020 UWM ManifoldEM team 
% Developed by Ghoncheh Mashayekhi, 2017- 2020
% Adopted from the original codes developed by Ali Dashti 2014


% Here this program was modified to label particles from different datasets 
% Modifications were marked by '%%'
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

boundCond=0;
ConCoef=20;

if exist([dir,'/Dat'],'file')==0
    mkdir([dir,'/Dat'])
    fileattrib([dir,'/Dat'],'+w','o')
elseif pcase==1
    system(['rm -f',dir,'/Dat/*.dat']);
end

fil=[dir,'/Data/S2tessellationResult.mat'];
load(fil)
fil=[dir,'/Data/starFile.mat'];
load(fil,'q')
load(fil,'Label_matrix4')

qq=q;
numimbin=zeros(1,nClass);
indsinbin=cell(1,nClass);

            

switch pcase
    case 1
        % Using IMGT
        for prD = 1:size(psinums,1)

            if psinums(prD,1)~=0
                %if each line in psinumber is not 0 
                clear IMGT tau q posPath ind psi1 IMG1 posPsi1
                
                ind=CG{1,prD}; % get the location of first line first column in all patches CG
                q=qq(:,ind); % get the euler angle from the particle orientation matrix 
                
                %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                Label_matrix5=Label_matrix4(:,ind);  %conduct the same transformation and calculation to matrixes of labels
                %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                
                fileNam1  =[dir,'/NLSA/NLSA_prD',int2str(prD),'_psi_',num2str(psinums(prD,1)),'.mat'];
                load(fileNam1,'tau','IMGT','posPsi1');
                % posPsi1 is the trojectory movement arrangement
                
                fileNam2  =[dir,'/EM/EM_prD',int2str(prD),'.mat'];
                load(fileNam2,'posPath');
                posPsi=posPath(posPsi1);
                disp(prD);
                conOrder=floor(length(ind(posPath))/ConCoef);
                
                q=q(:,posPsi); % rearrange the extracted angles according to the calculated trojectories
                
                %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                Label_matrix5=Label_matrix5(:,posPsi);   %conduct the same transformation and calculation to matrixes of labels
                %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                
                nS = size(q,2);
                if (boundCond ==1)
                    q = q(:,conOrder:nS);
                    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                    Label_matrix5=Label_matrix5(:,conOrder:nS);   %conduct the same transformation and calculation to matrixes of labels
                    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                else
                    q = q(:,conOrder:nS-conOrder-1); %???
                    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                    Label_matrix5=Label_matrix5(:,conOrder:nS-conOrder-1);   %conduct the same transformation and calculation to matrixes of labels
                    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                end
                
                for bin = 1:nClass
                   
                    ind1 = (bin-1)/nClass;
                    ind2 = bin/nClass;
                    if (bin ==nClass)
                        tauind= find((tau>=ind1) & (tau<=ind2));
                    else
                        tauind= find((tau>=ind1) & (tau<ind2));
                    end
                %    while (isempty(tauind))
                %        sc = 1/(nClass*2);
                %        ind1 = ind1 - sc*ind1;
                %        ind2 = ind2+sc*ind2;
                %        tauind = find((tau>=ind1)&(tau<ind2));
                %    end
                    indsinbin{bin}=[indsinbin{bin};ind(posPsi(tauind))];
                    
                    
                    fileNam1 = [dir,'/Dat/NLSAImage','_',num2str(bin),'_of_',int2str(nClass),'.dat'];
                    fileNam2 = [dir,'/Dat/TauVals','_',num2str(bin),'_of_',int2str(nClass),'.dat'];
                    fileNam5 = [dir,'/Dat/qs','_',num2str(bin),'_of_',int2str(nClass),'.dat'];
                    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                    fileNam6 = [dir,'/Dat/prelabel','_',num2str(bin),'_of_',int2str(nClass),'.dat']; % name the files which contain labels
                    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                    
                    f1 = fopen(fileNam1,'a');
                    fwrite(f1,IMGT(:,tauind),'float32');
                    fclose(f1);
                    
                    f2= fopen(fileNam2,'a');
                    fwrite(f2,tau(tauind),'float32'); %gm: it means for each bin of a single PD we would have different q and PD?!
                    fclose(f2);                    
                    f5 = fopen(fileNam5,'a');
                    fwrite(f5,q(:,tauind),'double'); % what q(:,tauind) means?
                    % devide patch prD1 into 50 classes
                    fclose(f5);
                    
                    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% 
                    f6 = fopen(fileNam6,'a');
                    fwrite(f6,Label_matrix5(:,tauind),'double');
                    fclose(f6);                                        % save the files which contains labels
                    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
                end
            end
        end
            save([dir,'/Dat/indsinbinRC1.mat'], 'indsinbin');
      
    case 2
        
        for j=[1:nClass]
           
            fIn = [dir,'/Dat/qs','_',num2str(j),'_of_',int2str(nClass),'.dat'];
            fid = fopen(fIn,'r');
            qs = fread(fid,'double');
            fclose(fid);
            len=length(qs)/4;
            qs = reshape(qs,4,len); 
            PDs = 2*[qs(2,:).*qs(4,:) - qs(1,:).*qs(3,:); ...
                qs(1,:).*qs(2,:) + qs(3,:).*qs(4,:); ...
                qs(1,:).^2 + qs(4,:).^2 - ones(1,len)/2 ];
            %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
            fIn = [dir,'/Dat/prelabel','_',num2str(j),'_of_',int2str(nClass),'.dat'];
            fid = fopen(fIn,'r');
            label = fread(fid,'double');
            fclose(fid);
            len=length(label)/4;
            label = reshape(label,4,len);
            label = label(1,:);
            save([dir,'/Dat/label','_',num2str(j),'_of_',int2str(nClass),'.mat'], 'label');  % reduct the scale of labels, the same with Euler angles
            %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
            
            phi = [];
            theta = [];
            psi = [];
            
            for i =1:len             
                PD = PDs(:,i);
                Qr = [1+PD(3), PD(2), -PD(1), 0]';
                Qr = Qr/sqrt(sum(Qr.^2));
                [phi(i), theta(i), psi(i)] = q2Spider(Qr,0);
            end     
           
            align = [psi' theta' phi' label'];
            name = [dir,'/Dat/align_',num2str(j,'%02d'),'.dat'];
            writeSPIDERdoc(name, align);
            save([dir,'/Dat/EulerAngs',num2str(j,'%02d'),'.mat'],'qs','phi','theta','psi');
        end
      
    case 3
        for j=[1:nClass]
            fIn = [dir,'/Dat/NLSAImage','_',num2str(j),'_of_',int2str(nClass),'.dat'];
            fid = fopen(fIn,'r');
            data = fread(fid,'float32');
            fclose(fid);         
            n = size(data,1)/nPix^2;           
            data = reshape(data,nPix,nPix,n);
%             data=permute(data,[2,1,3]);
            fOu = [dir,'/Dat/imgsSPIDER_',num2str(j),'_of_',int2str(nClass),'.dat'];
            writeSPIDERfile(fOu,data,'stack');
            
        end      
end
res='ok';
