from flask import Flask,render_template, request,session
import numpy as np
import random as rd
import copy as cp
import math as ma

app = Flask(__name__)
app.secret_key="alface"
@app.route("/")
def home():
  return render_template("home.html")


@app.route("/metodos",methods=['GET','POST'])
def dados():
     if request.method =='GET':
         return render_template("metodos.html")
     
     else:
        tam_Matriz=int(request.form.get('tMatriz'))
        Min_D=int(request.form.get('cMin'))
        Max_D=int(request.form.get('cMax'))
        matriz_A = Gerar_Problema(tam_Matriz,Min_D,Max_D)
        solucao_I=Solucao_Inicial(tam_Matriz)
        avalia= Avalia(tam_Matriz,solucao_I,matriz_A)
        sub_EncostaSi,sub_EncostaVn= Subida_Encosta(solucao_I,avalia,matriz_A)
        sub_Encosta_AlteradaSi,sub_Encosta_AlteradaVn= Subida_Encosta_Alterada(solucao_I,avalia,matriz_A,len(solucao_I))
        tempSi,tempVn=Tempera_Simulada(solucao_I,avalia,matriz_A,100000,0.1,0.8)

        matriz_A= np.array(matriz_A)
    
        session['matriz']= matriz_A.tolist()
        session['ponto'] = tam_Matriz

        return render_template("metodos.html",SoluIni=solucao_I.tolist(),Avalia=avalia,EncostaSi=sub_EncostaSi.tolist(),
                            EncostaVa=sub_EncostaVn,EncostaAlt=sub_Encosta_AlteradaSi.tolist(),EncostaAltVa=sub_Encosta_AlteradaVn,TempSi=tempSi.tolist(),TempVn=tempVn)

@app.route("/ag",methods=['POST'])
def ag():
     pontos =int(session.get('ponto'))
     Matriz=session.get('matriz')
     matriz=np.asarray(Matriz)
     TP=int(request.form.get('tp'))
     TC = float(request.form.get('tc'))
     TM = float(request.form.get('tm'))         
     IG = float(request.form.get('ig')) 
     NG= int(request.form.get('ng'))
     print (type(Matriz))
     print(type(pontos))
     
     AG_solucao= AlgoritmoGenetico(pontos,matriz,TP,TC,TM,NG,IG)
     AG_valor= Avalia(pontos,AG_solucao,matriz)
    
     return render_template ("ag.html",ag_s=AG_solucao,ag_v=AG_valor)

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
    aux = 0
    for i in range(ponto):
        s[i] = i
    rd.shuffle(s)

    while s[0] != 0:
        for i in range (ponto):
            if s[i] ==0:
                aux=s[i]
                s[i]=s[0]
                s[0] = aux

    return s


def sucessores_te(atual,tempo):
    
    pos1 = rd.randrange(1,len(atual))
    pos2 = rd.randrange(1,len(atual))
    
    suc = cp.deepcopy(atual)
        
    aux       = suc[pos1]
    suc[pos1] = suc[pos2]
    suc[pos2] = aux
        
    vs = Avalia(len(suc),suc,tempo)
        
    return suc, vs

def sucessores_se(atual,va,tempo):
    melhor = cp.deepcopy(atual)
    vm = va
    
    pos = rd.randrange(1,len(atual))
    
    for i in range(1,len(atual)):
        suc = cp.deepcopy(atual)
        
        aux      = suc[i]
        suc[i]   = suc[pos]
        suc[pos] = aux        
        vs = Avalia(len(suc),suc,tempo)
        
        if vs<vm:
            melhor = cp.deepcopy(suc)
            vm = vs
            
    return melhor, vm


def Subida_Encosta(atual,vi,tempo):
    atual = cp.deepcopy(atual)
    va = vi
    while True:
        novo, vn = sucessores_se(atual,va,tempo)
        if vn>=va:
            return atual, va
        else:
            atual = cp.deepcopy(novo)
            va = vn
           


def Subida_Encosta_Alterada(atual,vi,tempo,tMax):
    atual = cp.deepcopy(atual)
    va = vi
    t=0
    while True:
        novo, vn = sucessores_se(atual,va,tempo)
        if vn>=va:
            if t>tMax:
                return atual, va
            else:
                t += 1
        else:
            atual = cp.deepcopy(novo)
            va = vn
            t = 0


def Tempera_Simulada(atual,va,tempo,t_ini,t_fim,fr):
    atual = cp.deepcopy(atual)
    va = va
    t = t_ini

    while t>t_fim:
        novo, vn = sucessores_te(atual,tempo)
        de = vn - va
        if de<0:
            atual = cp.deepcopy(novo)
            va = vn
        else:
            ale = rd.uniform(0,1)
            aux = ma.exp(-de/t)
            if ale<aux:
                atual = cp.deepcopy(novo)
                va = vn
        t = t*fr
    
    return atual, va

def Sort(p,f,qp):
    for i in range(qp-1):
        for j in range(i+1,qp):
            if f[i]>f[j]:
                aux_f = cp.deepcopy(f[i])
                f[i]  = cp.deepcopy(f[j])
                f[j]  = cp.deepcopy(aux_f)

                aux_p = cp.deepcopy(p[i])
                p[i]  = cp.deepcopy(p[j])
                p[j]  = cp.deepcopy(aux_p)
    return p, f

def Ajusta_Restricao(n,desc,qd,corte):
    for i in range(len(desc)):
        alfabeto = list(range(0,n))
        for j in range(0,corte):
            alfabeto.remove(desc[i][j])
            rd.shuffle(alfabeto)

        j = corte
        while(len(alfabeto)!=0):
            if(desc[i].count(alfabeto[0])==0):
                if(desc[i].count(desc[i][j])>1):
                    desc[i][j] = alfabeto[0]
                    del alfabeto[0]
                    j += 1
                else:
                    j += 1
            else:
                del alfabeto[0]
    
    return desc

# ROTINA ROLETA
def Roleta(f):
    ale = rd.uniform(0,1)
    ind=0
    soma = f[ind]
    
    while soma<ale:
        ind += 1
        soma += f[ind]
    return ind

# ROTINA TORNEIO
def Torneio(f,tp):
    i1 = rd.randrange(1,tp)
    i2 = rd.randrange(1,tp)
    if f[i1]>f[i2]:
        return i1
    else:
        return i2

# GERA A NOVA POPULAÇÃO
def NovaPop(pop,desc,tp,ig):
    elite = ma.ceil(tp*ig)

    j= 0
    for i in range(elite,tp):
        pop[i] = cp.deepcopy(desc[j])
        j += 1
        if j==len(desc):
            break

    return pop

# EXECUTA O OPERADOR DE MUTAÇÃO
def Mutacao(n,desc,tp,tm):
    
    # Quantidade de mutaçãoes
    qm = ma.ceil(tp*tm)
    
    # Quantidade de descendentes
    q_desc = len(desc)

    for i in range(qm):
        # Selecionar o descendente
        jd = rd.randrange(q_desc)
        
                # faz cópia do descendente

        aux = cp.deepcopy(desc[jd])
        
        
        pos1 = rd.randrange(1,n)
        pos2 = rd.randrange(1,n)

        x = aux[pos1]
        aux[pos1] = aux[pos2]
        aux[pos2] = x

        desc.append(aux)

    return desc

def Crossover(n,pop,fit,tp,tc):

    # quantidade de cruzamentos
    qc = ma.ceil(tc*tp)
    
    # um ponto de corte
    corte = rd.randrange(0,n)

    desc = []
    for i in range(qc):
        # parent_1
        p1 = Roleta(fit)

        # parent_2
        p2 = Roleta(fit)

        # primeiro descendente
        aux = []
        for j in range(0,corte):
            aux.append(pop[p1][j])
        for j in range(corte,n):
            aux.append(pop[p2][j])
        desc.append(aux)

        # segundo descendente
        aux = []
        for j in range(0,corte):
            aux.append(pop[p2][j])
        for j in range(corte,n):
            aux.append(pop[p1][j])
        desc.append(aux)

    return corte, desc

# GERA UM CROMOSSOMO
def Cromossomo(n):
    ind = np.zeros(n,int)
    aux=0
    for i in range(n):
        ind[i] = i
    rd.shuffle(ind)

    while ind[0] != 0:
        for i in range (n):
            if ind[i]==0:
                aux = ind[i]
                ind[i]=ind[0]
                ind[0]=aux
    
    return ind


# GERA A POPULAÇÃO INICIAL
def PopIni(n,tp):
    pop = np.zeros((tp,n),int)

    for i in range(tp):
        pop[i] = Cromossomo(n)

    return pop

# CALCULA APTIDÃO
def Aptidao(n,mat_d,tp,pop):
    
    f = np.zeros(tp,float)
    i = 0
    for ind in pop:
        f[i] = Avalia(n,ind,mat_d)
        i += 1
    soma = sum(f)
    
    # frequencia relativa
    f = f/soma
    
    return f

# ALGORITMO GENÉTICO
def AlgoritmoGenetico(n,mat_d,tp,tc,tm,ng,ig):
    #======> Gera população inicial
    pop = PopIni(n,tp)
   # print("\n===> População Inicial:")
    #print(pop)
    
    #======> calcula fitness da população
    fit = Aptidao(n,mat_d,tp,pop)
     #Numeros pontos - visitados -> N // matriz_distancia, Total População //População Inicial
    print("\n===> Fitness:")
    print(["{:.3f}".format(valor) for valor in fit])
       
    #======> Ciclo AG
    for g in range(ng):
        #======> Aplica cruzamento
        corte, desc = Crossover(n,pop,fit,tp,tc)
        
        # ajusta descendentes para atender a restrição do problema
        desc = Ajusta_Restricao(n,desc,len(desc),corte)

        #======> Aplica mutação
        desc = Mutacao(n,desc,tp,tm)
        
        #======> calcula fitness de descendentes
        fit_d = Aptidao(n,mat_d,len(desc),desc)
    
        #======> Ordena população atual
        pop, fit = Sort(pop,fit,tp)

        #======> Ordena descendentes
        desc, fit_d = Sort(desc,fit_d,len(desc))

        #======> Gera nova população
        pop = NovaPop(pop,desc,tp,ig)

        #======> Fitness da população
        fit = Aptidao(n,mat_d,tp,pop)

    pop, fit = Sort(pop,fit,tp)
    return pop[0]


if __name__ == '__main__':
    app.run(debug=True)

    