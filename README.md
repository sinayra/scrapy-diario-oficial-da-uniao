# Leitor de seções do Diário da União
Projetinho em Python para buscar o conteúdo de um Diário da União a partir de uma data e um tipo de seção, gerando um arquivo `json` com os conteúdos encontrados. Ele utiliza a versão 3.8 do Python e o framework Scrapy.

Este projeto serviu para eu treinar Python com um framework de *crawler* bastante conhecido que até então eu não possuía experiência. Porém, uma vez que o site da Imprensa não disponibilizou os dados do DOU de forma aberta, decidi deixar este projeto público para ajudar os devs do futuro que precisam fazer algum tipo de busca nesse site do governo. Existem outros projetos que fazem a mesma coisa que esse aqui meu, mas os que achei estavam com versões bem antigas do Python e usando frameworks descontinuados.

Eu tenho **certeza** que haverão gafes aqui e ali e adoraria aprender com programadores mais experientes em como deixar esse projeto melhor. :sparkles:

## Premissas :warning:
O programa assume que:
* O DOU pode ser lido a partir do link https://www.in.gov.br/leiturajornal , com os seguintes argumentos
    * `secao`: string que pode possuir somente um dos seguintes valores:
        * dou1
        * dou2
        * dou3
    * `data`: string de data no formato *DD-MM-AAAA*
* Na página da Imprensa, existe um script do tipo *application/json* com os dados de cada seção. Estes dados incluem o objeto `jsonArray` com o campo `urlTitle`.
* Cada seção do DOU pode ser acessada a partir da concatenação do link https://www.in.gov.br/en/web/dou/-/ com `urlTitle`.

## Fluxo do programa

```python
from scrapy.crawler import CrawlerRunner
from ItemCollectorPipeline import ItemCollectorPipeline
from twisted.internet import reactor
```
Primeiramente, inclui-se no programa principal algumas dependências do *runner* do Scrapy. Também inclui-se a classe `ItemCollectorPipeline`, que é uma classe criada para acessar o pipeline do Scrapy e escrever em um arquivo temporário o resultado do *parser* que estiver executando.

```python
import loggerConfig
```
O módulo `loggerConfig` configura o nível do log que será escrito, escrevendo o resultado na pasta *log* do projeto.

```python
from crawlDou import crawlDou
from writeResult import writeResult
```
Inclui-se as funções de realizar o *Crawler* e a de escrever o resultado em um arquivo.

```python
runner  = CrawlerRunner(
    {
        'USER_AGENT': 'scrapy',
        'LOG_STDOUT': False,
        'LOG_ENABLED': True,
        'ITEM_PIPELINES': { '__main__.ItemCollectorPipeline': 100 }
    }
)
```

Define-se inicialmente como o Crawler irá executar, incluindo a adição da classe `ItemCollectorPipeline` que sobrescreve a original.

```python
crawlDou(runner, "07-08-2020", "dou3")
reactor.run()
```
A função `crawlDou` irá executar sequencialmente o *crawler* de buscar no site da Imprensa Nacional os links de cada uma das seções do diário especificado (com os argumentos `data` e `secao`), exibindo uma animação de *carregando* enquanto realiza a busca.
Já a função `run` do `reactor` irá realizar uma chamada bloquante para impedir que o resto do programa execute até o último *crawler* ser executado.

```python
if (os.path.exists("secoes-diario-oficial-da-uniao.jl") and os.path.exists("diario-oficial-da-uniao.jl")):
    writeResult("result.json", "secoes-diario-oficial-da-uniao.jl", ["secoes-diario-oficial-da-uniao.jl", "diario-oficial-da-uniao.jl"])
else:
    raise FileNotFoundError("Required files not found. Try again later")
```

Por último, verifica-se se os arquivos temporários que foram gerados na etapa de *crawler* foram criados. Se foram, escreve o resultado no arquivo `result.json` a partir do arquivo `secoes-diario-oficial-da-uniao.jl` e em seguida remove os arquivos temporários definidos no array.