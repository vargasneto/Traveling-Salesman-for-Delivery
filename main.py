from winreg import REG_NONE
from flask import Flask,render_template, request
import numpy as np
import random as rd


app = Flask(__name__)

@app.route("/")
def home():
  return render_template("home.html")


@app.route("/metodos",methods=['POST'])
def dados():
     tam_Matriz=int(request.form.get('tMatriz'))
     Min_D=int(request.form.get('cMin'))
     Max_D=int(request.form.get('cMax'))
     matriz_A = Gerar_Problema(tam_Matriz,Min_D,Max_D)
     solucao_I=Solucao_Inicial(tam_Matriz)
     avalia= Avalia(tam_Matriz,solucao_I,matriz_A)
     print("Matriz:",matriz_A)
     print('\nSolução:',solucao_I)
     print('\nAvalia',avalia)
     
     return render_template("metodos.html", matriz=matriz_A.tolist(),SoluIni=solucao_I.tolist(),Avalia=avalia)


def Gerar_Problema(n,me1,ma1):
    m1 = np.zeros((n,n),int)
    
    for i in range(n):
        for j in range(n):
            if i!=j:
                m1[i][j] = rd.randint(me1,ma1)
        
    return m1

def Avalia(n,s,m1):
    dist = 0
    for i in range(0,n-1):
        dist += m1[s[i]][s[i+1]]
    
    dist += m1[s[n-1]][s[0]]
    
    return dist

def Solucao_Inicial(n):
    s = np.zeros(n,int)
    
    for i in range(n):
        s[i] = i
    
    rd.shuffle(s)
    return s




if __name__ == '__main__':
    app.run(debug=True)