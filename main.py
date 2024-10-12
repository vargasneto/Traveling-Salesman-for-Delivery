from winreg import REG_NONE
from flask import Flask,render_template, request
import numpy as np
import random as rd
import copy as cp


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
     sub_EncostaSi,sub_EncostaVn= Subida_Encosta(solucao_I,avalia,matriz_A)
     novo,vn=sucessores_se(solucao_I,avalia,matriz_A)

     print("Matriz:",matriz_A)
     print('\nSolução:',solucao_I)
     print('\nAvalia',avalia)
     print('\nSolução da Subida Encosta',sub_EncostaSi)
     print('\nTempo da Subida Encosta',sub_EncostaVn)
     print('\nNova Melhor Solução',novo)
     print('\nNovo Melhor Valor',vn)
     return render_template("metodos.html", matriz=matriz_A.tolist(),SoluIni=solucao_I.tolist(),Avalia=avalia)


def Gerar_Problema(ponto,tMin,tMax):
    tempo = np.zeros((ponto,ponto),int)
    
    for i in range(ponto):
        for j in range(ponto):
            if i!=j:
                tempo[i][j] = rd.randint(tMin,tMax)
        
    return tempo

def Avalia(ponto,s,tempo):
    valor = 0
    for i in range(0,ponto-1):
        valor += tempo[s[i]][s[i+1]]
    
    valor += tempo[s[ponto-1]][s[0]]
    
    return valor

def Solucao_Inicial(ponto):
    s = np.zeros(ponto,int)
    
    for i in range(ponto):
        s[i] = i
    
    rd.shuffle(s)
    return s


def sucessores_se(atual,va,tempo):
    melhor = cp.deepcopy(atual)
    vm = va
    
    pos = rd.randrange(1,len(atual))
    
    for i in range(1,len(atual)):
        suc = cp.deepcopy(atual)
        
        aux      = suc[i]
        suc[i]   = suc[pos]
        suc[pos] = aux

        print (suc)
        
        vs = Avalia(len(suc),suc,tempo)
        
        if vs<vm:
            melhor = cp.deepcopy(suc)
            vm = vs
            
    return melhor, vm


def Subida_Encosta(atual,vi,tempo):
    atual = cp.deepcopy(atual)
    va = vi
    qt = 0
    while True:
        qt += 1
        novo, vn = sucessores_se(atual,va,tempo)
        if vn>=va:
            return atual, va
        else:
            atual = cp.deepcopy(novo)
            va = vn



if __name__ == '__main__':
    app.run(debug=True)