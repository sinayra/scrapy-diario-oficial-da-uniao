# Crawler do Diário Oficial da União
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

### Dependências do projeto 

Este projeto utiliza o Python 3.8.3 e o pip 20.2.2. Além deles, este projeto também depende do pacote `Scrapy` e do pacote `Json Lines`. Instale-os com o comando abaixo:

```shell
pip install Scrapy
pip install json-lines
```

## Para rodar este projeto

O código disponibilizado neste repositório irá executar o o *crawler* no Jornal da **Seção 3** do dia **07 de Agosto de 2020**. Ele no final irá retornar um arquivo *json* contendo:
1. O título do artigo (*ex: Aviso de Licitação/Extrato de termo Aditivo, etc...*);
2. O órgão do artigo;
3. O número da página do artigo; e
4. O link do artigo (*para consulta*).

Para rodar, execute o código: `python main.py`

### Modificando o projeto para as suas necessidades

No arquivo `main.py`, altere as [configurações do *crawler*](main.py#L12) e os argumentos de [crawlDou](main.py#L32) (não é necessário alterar o primeiro argumento, somente o segundo, que se refere a `data`, e o terceiro, que se refere a `seção`).

No arquivo `douSection.py`, o método [parse](douSection.py#L15) é responsável pela extração dos dados da página. Para modificá-los, é necessário um conhecimento prévio de HTML e do Selector do Scrapy (no caso, eu estou utilizando os seletores seguindo a sintaxe o *xpath* por questões pessoais mesmo, mas ele também consegue usar a sintaxe do CSS pra selecionar estes elementos, que você pode conferir aqui: https://docs.scrapy.org/en/latest/topics/selectors.html).

*PS: Minha sugestão é que antes que você altere o código, rode a primeira vez sem alterar nada, apenas para conferir se todas as dependências foram instaladas corretamente.*

## Explicação do fluxo do programa

### Imports
```python
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor
```
Primeiramente, inclui-se no programa principal alguns pacotes do *runner* do Scrapy. 

### Configuração do Log
```python
import loggerConfig
```
O módulo `loggerConfig` configura o nível do log que será escrito, escrevendo o resultado na pasta *log* do projeto.

### Módulos do programa
```python
from crawlDou import crawlDou
from writeResult import writeResult
```
Inclui-se as funções de realizar o *Crawler* e a de escrever o resultado em um arquivo.

### Configurações do crawler
```python
runner  = CrawlerRunner(
    {
        'USER_AGENT': 'Sinayra-meuCrawlerComScrapy/1.1 (sinayra@hotmail.com)',
        'LOG_STDOUT': False,
        'LOG_ENABLED': True,
        'ROBOTSTXT_OBEY' : True,
        'RANDOMIZE_DOWNLOAD_DELAY': True,
        'CONCURRENT_REQUESTS': 5,
        'RETRY_TIMES' : 5,
        'AUTOTHROTTLE_ENABLED' : True,
        'HTTPCACHE_ENABLED': True,  # for development
        'FEEDS':{
            'items.jl': {
                'format': 'jsonlines',
                'encoding': 'utf8'
            }   
        },
    }
)
```

Define-se inicialmente como o Crawler irá executar.A opção `FEED` define onde o resultado do *crawler* será escrito. No caso, definiu-se que o arquivo se chama `items.jl` e é do formato `jsonlines`. Este arquivo será usado como auxiliar ao longo do programa.

Algumas observações destas opções de configuração:
*  :exclamation: Altere o *user-agent* para melhor identificar o seu crawler. :exclamation:
* É possível alterar o número de requests simultâneos alterando a opção `CONCURRENT_REQUESTS`, o que irá melhorar o desempenho ao escrever o resultado do *parser*, mas evite colocar um número muito alto para não sobrecarregar o servidor do governo. Minha sugestão é colocar no máximo `20`.
* Enquanto você estiver alterando algum spider (como o [spider dou](dou.py) ou [spider dou section](douSection.py)), habilite a opção `HTTPCACHE_ENABLED` como verdadeira, para o Scrapy salvar em cache as páginas e não precisar fazer uma nova requisição de uma página que ele já visitou. Se está tudo certinho com o que ele tem que buscar, desabilite esta opção.

### Execução do crawler
```python
crawlDou(runner, "07-08-2020", "dou3")
reactor.run()
```
A função `crawlDou` irá executar sequencialmente o *crawler* de buscar no site da Imprensa Nacional os links de cada uma das seções do diário especificado (com os argumentos `data` e `secao`), exibindo uma animação de *carregando*. Após buscar todos os links das seções, ele executa um segundo *crawler* para buscar o conteúdo de cada uma das seções.
A função `run` do `reactor` irá realizar uma chamada bloquante para impedir que o resto do programa execute até que o último *crawler* seja executado.

### Escrevendo resultados
```python
if (os.path.exists("items.jl")):
    writeResult("result.json", "items.jl")
else:
    raise FileNotFoundError("Required files not found. Try again later")
```

Por último, verifica-se se os arquivos temporários que foram gerados na etapa de *crawler* foram criados. Se foram, escreve o resultado no arquivo `result.json` a partir do arquivo `items.jl`, removendo este logo em seguida.
