# Monta arquivo CSV com extrato de fatura em formato CSV
#
# Cada linha do CSV possui
#   DATA = data da fatura, no formato YYYY-MM-DD
#   DESCRICAO = <DATA DA COMPRA> - <DESCRICAO> <(X/Y)>, onde:
#       <DATA DA COMPRA> = data original em que foi feita a compra
#       <DESCRICAO> = descritivo que vem na fatura (transacao)
#       <(X/Y)> = se a compra for parcelada, X é a parcela corrente e Y é o total de parcelas
#       Exemplo: 2020-02-08 - Estabelecimento XPTO (1/3)
#   VALOR = valor do item na fatura
#
# Exemplo de linha no CSV:
#       2020-03-05;2020-02-08 - Estabelecimento XPTO (1/3);50,00
#   
# Forma de uso
#   python extrato.py <CPF> <SENHA> <DATA NO FORMATO YYYY-MM-DD>
#
# Dependência do pynubank (versao 1.0.1 que dá suporte ao QRCode)
#   https://github.com/andreroggeri/pynubank/tree/1.0.1

from pynubank.nubank import Nubank

import sys
import locale
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

cpf = sys.argv[1]
pwd = sys.argv[2]
bill_date = sys.argv[3]
output_file_path = 'C:\\Users\\danfc\\Documents\\GnuCash\\importacao.csv'

#busca fatura com base em uma data
def get_bill_by_date(bills, date):
    for b in bills:
        if b['summary']['due_date'] == date:
            return b
    return None

#busca transacao com base no id (href)
def get_transaction_by_id(transactions, id):
    for t in transactions:
        if t['href'] == id:
            return t
    return None

#formata a descricao da transacao
def get_formated_description(bill_item, transaction):
    description = '{} - {}'.format(transaction['time'][:10], bill_item['title'])
    if bi['charges'] > 1:
        description = description + ' ({}/{})'.format(bi['index'] + 1,  bi['charges'])
    return description

nu = Nubank()
uuid, qr_code = nu.get_qr_code()
qr_code.print_ascii(invert=True)
input('Após escanear o QRCode pressione enter para continuar')

# Somente após escanear o QRCode você pode chamar a linha abaixo
nu.authenticate_with_qr_code(cpf, pwd, uuid)

#recupera as transacoes
nubank_transactions = nu.get_card_statements()

#recupera as faturas
nubank_bills = nu.get_bills()

#busca fatura com base em uma data
nubank_bill = get_bill_by_date(nubank_bills, bill_date)

#recupera os detalhes da fatura
nubank_bill_details = nu.get_bill_details(nubank_bill)

csv_output = open(output_file_path,'w')
csv_output.write('DATA;DESCRICAO;VALOR')

for bi in nubank_bill_details['bill']['line_items']:
    if 'href' in bi:
        t = get_transaction_by_id(nubank_transactions, bi['href'])
        row = '\n' + bill_date + ';'
        row += get_formated_description(bi, t) + ';'
        row += locale.currency(bi['amount'] / 100, grouping=True, symbol=None)        
        csv_output.write(row)

csv_output.close()
