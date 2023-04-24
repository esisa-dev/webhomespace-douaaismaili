from typing import Any
import os,spwd,crypt
import datetime,calendar
import matplotlib.pyplot as plt
import io,base64
import matplotlib.pyplot as plt
class UserService:
    def __init__(self,oldUrl,c) -> None:
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
    def listContent(self,path):
        f=os.popen(f'sudo ls -l {path}|tr -s " " " "|cut -d " " -f9-')
        liste=[]
        f.readline()
        for l in f.readlines():
            if(os.path.isdir(f'{path}/{l[0:len(l)-1]}')):
                st=os.stat(f'{path}/{l[0:len(l)-1]}')
                taille=str(st.st_size)
                jour=datetime.datetime.fromtimestamp(st.st_mtime).day
                mois=calendar.month_name[datetime.datetime.fromtimestamp(st.st_mtime).month]
                annee=datetime.datetime.fromtimestamp(st.st_mtime).year
                time=(str(datetime.datetime.fromtimestamp(st.st_mtime).time()).split('.')[0]).split(':')[:-1]
                liste.append((f'{path}/{l[0:len(l)-1]}',l[0:len(l)-1],jour,mois,annee,f'{time[0]}:{time[1]}',taille))
        return liste
    def printFile(self,path):
        f=open(path,'r')
        s=''
        for l in f.readlines():
            s=s+ l + ' <br> '
        f.close
        return s
    def navigate(self,path):
        if(os.path.isfile(path)):
            ext=path.split(".")[1]
            if(ext=="txt"):
                return self.printFile(path)
                 
        elif(os.path.isdir(path)):
            f=os.popen(f'sudo ls -l {path}|tr -s " " " "|cut -d " " -f9-')
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
            return liste
        
    def rechercher(self,value):
        return self.infos(f'{self.oldUrl}','-type f',value)
    def infos(self,path,type,value):
        f=os.popen(f"sudo find {path} {type} -iname '*{value}*'")
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
        os.system(f'sudo zip -r {directory_path}.zip {directory_path}')  
    def filesCount(self):
        f=os.popen(f'sudo find {self.oldUrl} -type f | wc -l')
        for l in f.readlines():
            c=l[0:len(l)-1] 
        return c
    def dirsCount(self):
        f=os.popen(f'sudo find {self.oldUrl} -type d | wc -l')
        for l in f.readlines():
            c=l[0:len(l)-1] 
        return c
    def space(self):
        dic={'K':1,'M':1000,'G':10**6,'T':10**9}
        f=os.popen(f'sudo df -h {self.oldUrl}|tr -s " " " " |tail -1|cut -d " " -f2')
        s=[]
        for l in f.readlines():
            t=l[0:len(l)-1] 
        f=os.popen(f'sudo du -sh {self.oldUrl}|tr -s " " " "|cut -f1')
        for l in f.readlines():
            u=l[0:len(l)-1] 
        s.append(u)
        s.append(t)
        uu=u[len(u)-1] 
        ut=t[len(t)-1] 
        for k,v in dic.items():
            if(uu==k):
                u=float(u[0:len(u)-1].replace(',','.'))* (int(v))
            if(ut==k):
                t=float(t[0:len(t)-1].replace(',','.'))* (int(v))
        donnees = [u, abs(t-u)]
        etiquettes = ['Espace utilisé', 'Espace restant']
        couleurs = ['#FFA07A', '#ADD8E6']
        
        plt.pie(donnees, labels=etiquettes, colors=couleurs, autopct='%1.1f%%')
        l=len(str(f'{self.oldUrl}').split('/'))
        plt.title(f"Espace disque pour l'utilisateur courant: {str(self.oldUrl).split('/')[l-1]}")
        img = io.BytesIO()
        plt.savefig(img, format='png')
        plt.close()
        img.seek(0)
        img_base64 = base64.b64encode(img.getvalue()).decode()
        liste=[img_base64,s[0],s[1]]
        return liste