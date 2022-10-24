#!/usr/bin/env python
# coding: utf-8

# # Scraping

# In[1]:


import requests
import bs4
from socket import *


# In[2]:


# pegando informações do site 
def scrapin(site):
    res = requests.get('{}'.format(site))
    soup = bs4.BeautifulSoup(res.text,'lxml')
    return soup


# In[3]:


# conectando ao site
site = 'http://portaldasprefeituras-al.com.br/limoeirodeanadia/prefeitura/'
# jogando na funcao para fascilitar a manipulacao
dados = scrapin(site)
print("site conectado")


# In[4]:


# selecionando somente os dados da tabela
tratamento_aux = []
for d in dados.find_all('tr'):
        tratamento_aux.append(d.get_text())


# In[ ]:


dados_tratados = []
# retirando quebra de linha e dadso nao uteis
for e in tratamento_aux:
    aux = e.split('\n')
    while True:
        try:
            #removendo dados nao uteis
            aux.remove('')
        except:
            try:
                #removendo dados nao uteis
                aux.remove(' Visualizar com detalhes')
                aux.remove(' Exportar em CSV')
            except:
                break
                
    dados_tratados.append(aux)
############################

#remoção dos primeiros dados 
dados_tratados.pop(0)
dados_tratados.pop(0)
dados_tratados.pop(0)
# criando dicionario
lista_Empenhos = {'NE':[],'DE':[],'VE':[],'CC':[],'NC':[],'H':[]}
# NE = 'Nº do Empenho'
# DE = 'Data do Empenho (A-M-D)'
# VE = 'Valor do Empenho'
# CC = 'Codigo do Credor'
# NC = 'Nome do Credor'
# H = 'Historico'
# armazenando nas listas
for fa in dados_tratados:
    lista_Empenhos['NE'].append(int(fa[0]))
    lista_Empenhos['DE'].append(fa[1])
    lista_Empenhos['VE'].append(fa[2])
    lista_Empenhos['CC'].append(fa[3])
    lista_Empenhos['NC'].append(fa[4])
    lista_Empenhos['H'].append(fa[5])


# In[ ]:





# In[ ]:


#funcao para pesquisar 
def pesquisa (numero,opcao):
    resultados = []
    count = 0
    for num in lista_Empenhos[opcao]:
        if num == numero:
            resultados.append(count)
        count += 1
    return resultados


# # Servidor

# In[ ]:


myHost = ''
myPort = 5007


# In[ ]:


# AF_INET --> protocolo de endereço IP
# SOCK_STREAM
sockObj = socket(AF_INET,SOCK_STREAM)


# In[ ]:


# VINCULANDO O SERVIDOR COM A PORTA
sockObj.bind((myHost, myPort))


# In[ ]:


#numero de conexões simultaneas
sockObj.listen(5)
print("servidor ligado")


# In[ ]:


#Servidor
while True:
    conexao, endereco = sockObj.accept()
    print("Servidor conectado por: ",endereco)
    while True:

        # numero de bytes que a conexão ira receber
        total_bytes = 1024
        data = conexao.recv(total_bytes)
        
        
        if not data : break
        # Meu de ações
        acao = data.decode()
        acao = acao.split(',')
        print(acao)
        # verificação para verificar nas tabelas respectivas
        if acao[0] == "NE":
            resultado = ''
            # pesquisa na tabela
            for result in pesquisa(acao[1],'NE'):
                # armazenando na string
                resultado += "NC: " + str(lista_Empenhos['NC'][result]) +" | "+ "H: " + str(lista_Empenhos['H'][result]) +" | "+ "VE: " + str(lista_Empenhos['VE'][result])+" | "+ "DE: " + str(lista_Empenhos['DE'][result])
                resultado += (str("+"))
                
        elif acao[0] == "CC":
            resultado = ''
            # Pesquisa na tabela
            for result in pesquisa(acao[1],'CC'):
                # armazenando na string
                resultado += "NC: " + str(lista_Empenhos['NC'][result]) +" | "+ "H: " + str(lista_Empenhos['H'][result]) +" | "+ "VE: " + str(lista_Empenhos['VE'][result])+" | "+ "DE: " + str(lista_Empenhos['DE'][result])
                resultado += (str("+"))
                
        elif acao[0] == "NC":
            resultado = ''
            # pesquina na tabela
            for result in pesquisa(acao[1],'NC'):
                # armazena na string
                resultado += "CC: " + str(lista_Empenhos['CC'][result]) +" | "+ "H: " + str(lista_Empenhos['H'][result]) +" | "+ "VE: " + str(lista_Empenhos['VE'][result])+" | "+ "DE: " + str(lista_Empenhos['DE'][result])
                resultado += (str("+"))
        elif acao[0] == "DE":
            resultado = ''
            # pesquisa na tabela
            for result in pesquisa(acao[1],'DE'):
                # armazena na string
                resultado += "NC: " + str(lista_Empenhos['NC'][result]) +" | "+ "H: " + str(lista_Empenhos['H'][result]) +" | "+ "VE: " + str(lista_Empenhos['VE'][result])+" | "+ "DE: " + str(lista_Empenhos['DE'][result])
                resultado += (str("+"))
        else:
            # se a tabela nao existir
            resultado = "ERROR: TABLE NOT FOUND"
        # se o valor não for encontrado
        if resultado == '':
            resultado = "ERROR: VALUE NOT FOUND"
        # envio da mensagem para o cliente
        conexao.send(str.encode(str(resultado)))
    # Fechando a conexoa
    conexao.close

