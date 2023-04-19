from typing import Any
import os,spwd,crypt
import datetime,calendar
import zipfile
class UserService:
    def __init__(self,oldUrl) -> None:
        self.oldUrl=oldUrl
    def verifyUser(self,login,pwd)->Any:
        f=os.popen(f'sudo cat /etc/shadow | grep {login}| wc -l' )
        n=0
        for l in f.readlines():
            n=int(l)
        if(n!=0):
            if(os.path.exists(f'/home/{login}')):
                if(crypt.crypt(pwd,spwd.getspnam(login).sp_pwdp)==spwd.getspnam(login).sp_pwdp):
                    return True
                else:
                    return 'mot de passe incorrect'
            else:
                return login + " doesn't exist"
        else:
            return login + " doesn't exist"
    def clear(self):
        file1=open('WebHomeSpace/templates/app.html','w')
        file2=open('WebHomeSpace/templates/appBackup.html','r')
        contenu=file2.read()
        file2.close()
        file1.write(contenu)
    def listContent(self,path):
        f=os.popen(f'ls -l {path}|tr -s " " " "|cut -d " " -f9-')
        liste=[]
        f.readline()
        for l in f.readlines():
            st=os.stat(f'{path}/{l[0:len(l)-1]}')
            taille=str(st.st_size)
            jour=datetime.datetime.fromtimestamp(st.st_mtime).day
            mois=calendar.month_name[datetime.datetime.fromtimestamp(st.st_mtime).month]
            annee=datetime.datetime.fromtimestamp(st.st_mtime).year
            time=(str(datetime.datetime.fromtimestamp(st.st_mtime).time()).split('.')[0]).split(':')[:-1]
            liste.append((f'{path}/{l[0:len(l)-1]}',l[0:len(l)-1],jour,mois,annee,f'{time[0]}:{time[1]}',taille))
        print('OLDURL: ',self.oldUrl)
        if(liste==[]):
            print('vide')
        return liste
    def printFile(self,path):
        f=open(path,'r')
        s=''
        for l in f.readlines():
            s=s+ l + ' <br> '
        f.close
        return s
    def navigate(self,path):
        print('OLDURL: ', self.oldUrl)
        if(os.path.isfile(path)):
            ext=path.split(".")[1]
            if(ext=="txt"):
                return self.printFile(path)
                 
        elif(os.path.isdir(path)):
            self.clear()
            return self.listContent(path)
        
    def rechercher(self,value):
        print(self.oldUrl)
        return self.infos('/home/douaa','-type f',value)
    def infos(self,path,type,value):
        f=os.popen(f"find {path} {type} -iname '*{value}*'")
        liste=[]
        for l in f.readlines():
            st=os.stat(l[0:len(l)-1])
            taille=str(st.st_size)
            jour=datetime.datetime.fromtimestamp(st.st_mtime).day
            mois=calendar.month_name[datetime.datetime.fromtimestamp(st.st_mtime).month]
            annee=datetime.datetime.fromtimestamp(st.st_mtime).year
            time=(str(datetime.datetime.fromtimestamp(st.st_mtime).time()).split('.')[0]).split(':')[:-1]
            print(time)
            liste.append((l[0:len(l)-1],jour,mois,annee,f'{time[0]}:{time[1]}',taille))
        return liste
    def compress_directory(self,directory_path):
        directory_path=str(directory_path)
        zipf = zipfile.ZipFile(directory_path+'.zip', 'w', zipfile.ZIP_DEFLATED)
        for root,subdirs,files in os.walk(directory_path):
            #print('root: ', root)
            #print('files: ', files)
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, directory_path))
        zipf.close()
    
U=UserService('/home/douaa')
U.compress_directory(U.oldUrl)