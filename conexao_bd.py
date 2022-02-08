import fdb
from datetime import date

def dia_da_semana():
#    DIAS = [
#    'Segunda-feira',
#   'Terça-feira',
#    'Quarta-feira',
#    'Quinta-Feira',
#    'Sexta-feira',
#    'Sábado',
#    'Domingo'
#    ]
    indice_da_semana = date.weekday(date.today())
    global dia_semana
    #dia_da_semana = DIAS[indice_da_semana]
    
    if indice_da_semana == 0: #segunda feira
        dia_semana = "1000000"
        #return dia_semana
    elif indice_da_semana == 1: #terca feira
        dia_semana = "0100000"
        #return dia_semana
    elif indice_da_semana == 2: #quarta feira
        dia_semana = "0010000"
        #return dia_semana
    elif indice_da_semana == 3: #quinta feira
        dia_semana = "0001000"
        #return dia_semana
    else:
        #sexta feira
        dia_semana = "0000100"
        #return dia_semana

def salvar(texto):
    data_atual = date.today()
    data_em_texto = data_atual.strftime('%d_%m_%Y')
    f = open(f'devedores_{data_em_texto}.txt', 'a')
    f.write(texto+'\n')
    f.close()
    print('arquivo salvo...')

def conectar():
    # Create a Cursor object that operates in the context of Connection con:
    con = fdb.connect(
        host='localhost', database='C:\\KOCH\\SD\\SDDB.FDB',
        user='SYSDBA', password='masterkey'
      )
    
    data_atual = date.today()
    data_em_texto = data_atual.strftime('%Y/%m/%d')
    #chama funcao para pegar o dia da semana
    dia_da_semana()
    print(dia_semana)

    cur = con.cursor()
    consulta= [data_em_texto, dia_semana]
    print(data_em_texto)
    
    # Execute the SELECT statement:
    #cur.execute("SELECT COALESCE(A.TOTALS,0.00)+COALESCE(A.TOTALC,0.00) AS MTOTAL, A.CODVEN, A.NUMERO, A.DATA, A.HORAP, B.RAZAO_SOCIAL, B.NOME_FANTASIA from PEDIDOCA A, CLIENTES B where A.CODCLI=B.CODCLI AND cast(A.DATA as DATE)=(?) AND A.NUMERO > (?) order by A.NUMERO",consulta)
    cur.execute("select a.codcli, b.razao_social, b.nome_fantasia, a.datavenc, a.valor, a.valorpag, b.vendedor, c.nome from movcli a, clientes b, vendedores c where a.datavenc < (?) and b.visita = (?) and COALESCE(a.valorpag,0.00) < a.valor and a.codcli=b.codcli and b.vendedor = c.codven order by b.vendedor, b.razao_social, a.datavenc",consulta)

    # Retrieve all rows as a sequence and print that sequence:
    lista = cur.fetchall()

    #for count,item in enumerate(lista):
    vendedor_atual = ''
    for item in lista:       
        #0 codcli
        #1 razao
        #2 fantasia
        #3 data venc
        #4 valor
        #5 valor pago
        #6 codven
        #7 nome do vendedor
        
        vendedor = item[7]
        print(vendedor)
        
        if vendedor_atual != vendedor:
            vendedor_atual = vendedor
            salvar('\n'+'*'*3+vendedor+'*'*3)
            salvar('Seguem abaixo os clientes em atraso com visita programada para hoje:')
        
        pedido=(f'Código: {int(item[0])}')
        print(pedido)
        razao = ('Razão Social: '+item[1])
        print(razao)
        fantasia = ('Fantasia: '+item[2])
        print(fantasia)
        venc = item[3]
        venc = venc.strftime('%d/%m/%Y') #funcao para converter a data
        venc = ('Data Vencimento: '+venc)
        print(venc)
        valor = item[4]
        valor = (f'Valor: R$ {float(valor)}')
        print(valor)
        valorpag = item[5]
        valorpag = (f'Valor já pago: R$ {valorpag}')
        print(valorpag)


        texto = (f'{pedido} {razao} {fantasia} {venc} {valor} {valorpag}')
        salvar(texto)
                  
    cur.close()
    con.close()
    print("Conexão finalizada...")




conectar()
