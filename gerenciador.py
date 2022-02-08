import conexao_bd as con

try:
    con.conectar()
    print("Conectado ao banco de dados com SUCESSO.")
except e:
    print("Não foi possível se conectar ao banco de dados.")
    print (e)



#import time
#import threading

#class Timer(threading.Thread):
#    def __init__(self, segundos):
#        self.runTime = segundos
#        threading.Thread.__init__(self)
#    def run(self):
#        time.sleep(self.runTime)
#        print "Executado!"

#t = Timer(10)
#t.start()

#TESTAR POSSIBILIDADE DE USAR O CRON, achei interessante
