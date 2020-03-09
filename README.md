# nubankexporter

## Objetivo e Motivação

Este script foi criado para auxiliar na exportação de dados de fatura do Cartão de Crédito Nubank para que seja importado em ferramenta de controle financeiro. No meu caso, uso o [GnuCash](https://www.gnucash.org).

Apensar do Nubank permitir a exportação de dados em formato CSV e OFX, os dados contidos não me atendem. 

Portanto, preciso fazer sempre um trabalho manual de estruturar os registros para importar para o GnuCash. Eu faço esse trabalho sacal pelos seguintes motivos:

1. A cada fatura, a data que aparece em uma compra nem sempre é a data do dia que ela realmente aconteceu. Numa compra à vista, aparece ou a data do mesmo dia ou do dia seguinte.
1. Quando a compra é parcelada, ele mostra a data em que foi processado naquele mês. Ou seja olhando para a fatura, você não faz ideia qual foi a data da compra.
1. Eu sempre formato o descritivo da compra para mostrar a Data + Descritivo + Parcela (formato do CSV mais abaixo).

*OBS: Tem muito tempo que não programo (pelo menos a lógica ainda está fresca). Meu conhecimento em Python tende a ZERO. Portanto, ignore eventuais atrocidades no código.*

## Instruções

* Cada linha do CSV possui
  * DATA = data da fatura, no formato YYYY-MM-DD
  * DESCRICAO = `<DATA DA COMPRA>` - `<DESCRICAO>` `<(X/Y)>`, onde:
    * `<DATA DA COMPRA>` = data original em que foi feita a compra
    * `<DESCRICAO>` = descritivo que vem na fatura (transacao)
    * `<(X/Y)>` = se a compra for parcelada, X é a parcela corrente e Y é o total de parcelas
  * VALOR = valor do item na fatura

### Forma de Uso

```
python extrato.py <CPF> <SENHA> <DATA DE VENCIMENTO DA FATURA NO FORMATO YYYY-MM-DD>
```
*Antes dos dados serem enviados para o Nubank, será chamado o pynubank (ver dependência), que mostrará um QRCode na tela.
Você deverá seguir o mesmo procedimento que faz quando usa o site do Nubank: abrir o app e ler o QRCode. Depois que fizer isto, pressionar tecla para prosseguir. Aí sim será enviado para o Nubank os seus dados para autenticação junto com o UUID (do QRCode).*

### Saída

Exemplo de CSV de saída com 1 registro:
```
DATA;DESCRICAO;VALOR
2020-03-05;2020-02-08 - Estabelecimento XPTO (1/3);50,00
```

## Dependência

[pynubank (versao 1.0.1 que dá suporte ao QRCode)](https://github.com/andreroggeri/pynubank/tree/1.0.1)
