#!/usr/bin/env python
# coding: utf-8

# # Cliente

# In[1]:


from socket import *


# In[2]:


# tipo de conexão, local
serverHost = 'localhost'
# porta para comunicação com o servidor (a mesma do servidor)
serverPort = 5007


# In[3]:


# Tipo de protocolo usado
# AF_INET  = IP
# SOCK_STREAM = TCP
sock_client_obj = socket(AF_INET,SOCK_STREAM)


# In[4]:


# criando a conexão
sock_client_obj.connect((serverHost,serverPort))


# In[5]:


#entrada da mensagem
print("Programa desenvolvido para coletar dados do site Portal da Transparência da cidade de Limoeiro de Anadia.",'\n')
print("indice de Abreciações:")
print('NE = Nº do Empenho',' DE = Data do Empenho (ANO-MÊS-DIA)',' VE = Valor do Empenho',' CC = Codigo do Credor',' NC = Nome do Credor',' H = Historico',"\n")
print("Digite a abreviação e o dado para consulta separado por virgulas:")
print("Exemplo: DE,2018-12-28")
entrada = input("Digite a tabela e a consulta:")
mensagem = [str.encode(entrada)]


# In[7]:


for linha in mensagem:
    sock_client_obj.send(linha)
    
    #espera o servidor responder
    data = sock_client_obj.recv(10024)
    resposta = data.decode().split("+")
    print('NE = Nº do Empenho',' DE = Data do Empenho (ANO-MÊS-DIA)',' VE = Valor do Empenho',' CC = Codigo do Credor',' NC = Nome do Credor',' H = Historico',"\n")
    for valores in resposta:
        print(valores)
sock_client_obj.close

