## Estudo do Stack Tecnológico de Dados no CEPEL

Este notebook (`script.ipynb`) consolida e transforma os dados de um survey interno sobre o **stack tecnológico de dados no CEPEL**, com foco em organizar as respostas em formato “tidy data” (formato longo) para uso em análises estatísticas, BI e modelos de machine learning.

---

### Objetivos

- **Carregar os dados** exportados do formulário (armazenados em um banco SQLite `cepel_data.db`).
- **Explorar a estrutura das tabelas** do survey.
- **Converter as respostas em formato wide** (uma coluna por tecnologia/pergunta) para **formato long/tidy** usando `pandas.melt`.
- **Organizar grupos de tecnologias** (sistemas operacionais, virtualização, linguagens, etc.) em dataframes consolidados e prontos para análise.
- **Criar uma base padronizada** por respondente, tecnologia e tipo de resposta (uso, “outro”, prioridade).

---

### Fonte de Dados

- **Banco**: `cepel_data.db`
- **Tecnologia**: SQLite
- **Leitura via Python**:
  - Biblioteca: `sqlite3`
  - Integração com `pandas` usando `pd.read_sql_query`

As principais tabelas usadas incluem (nomes originais do formulário):

- `Composição_do_Stack_Tecnológico_de_Dados_no_Cepel_Parte_0_Identificação1_21`
  - Contém informações de identificação do respondente: `ID`, `START_TIME`, `COMPLETION_TIME`, `EMAIL`, `NAME`, dados demográficos e de experiência.
- `Composição_do_Stack_Tecnológico_de_Dados_no_Cepel_Parte_3_Interface_DevOps1_18`
  - Contém a maior parte das colunas relacionadas a tecnologias (sistemas operacionais, virtualização, linguagens, IDEs, CI/CD, boas práticas, etc.).

---

### Principais Bibliotecas Utilizadas

- **pandas**: manipulação de dados, leitura de CSV/SQLite, uso intensivo de `groupby`, `agg`, `reset_index` e `melt`.
- **sqlite3**: conexão com o banco `cepel_data.db` e extração das tabelas.

---

### Estrutura Geral do Notebook

- **Blocos iniciais de teste** (podem ser ignorados):
  - Exemplos simples de `groupby` e `to_csv` para testar agregações e salvamento.
- **Carregamento do banco**:
  - Abertura de conexão com `sqlite3.connect("cepel_data.db")`.
  - Listagem de tabelas via consulta à `sqlite_master`.
  - Leitura das tabelas relevantes com `pd.read_sql_query`.

Um primeiro `display`/`head()` é feito para verificar se as colunas e o conteúdo estão corretos.

---

### Organização das Colunas em Grupos Temáticos

O notebook define um dicionário de listas chamado, por exemplo, `grupos`, com **grupos temáticos de colunas** que representam dimensões do stack tecnológico. Entre eles:

- **SISTEMA_OPERACIONAL**
  - Ex.: `WINDOWS_NT_SERVER`, `WINDOWS_1011`, `LINUX_DEBIAN_UBUNTU_MINT_KALI`, `LINUX_ARCH_MANJARO_ENDEAVOUROS`, `LINUX_RED_HAT_FEDORA_CENTOS_ROCKY`, `LINUX_SUSE`, `LINUX_ALPINE`, `MACOS`, `CHROME_OS`, `ANDROID`, `IOS`, `OUTRO6`.
- **SISTEMA_OPERACIONAL_OUTRO**
  - Ex.: `SE_VOCE_APONTOU_TER_USADO_USAR_ATUALMENTE_OU_QUERER_USAR_OUTRO_SISTEMA_OPERACIONAL_ACIMA_POR_FAVOR_IDENTIFIQUE_QUAL_ABAIXO`.
- **SISTEMA_OPERACIONAL_PRIORITARIO**
  - Ex.: `QUAIS_DOS_SEGUINTES_SISTEMAS_OPERACIONAIS_LHE_SAO_PRIORITARIOS`.
- **VIRTUALIZACAO_E_ACESSO**
  - Ex.: `SSH`, `RDP_WINDOWS`, `VNC_MULTIPLATAFORMA`, `WSL_WINDOWS_SUBSYSTEM_FOR_LINUX`, `VMWARE`, `VIRTUALBOX`, `PROXMOX`, `DOCKER`, `PODMAN`, `SINGULARITY`, `DOCKERCOMPOSE`, `DOCKERSWARM`, `KUBERNETES`, `OUTRO7`.
- **VIRTUALIZACAO_OUTRO** / **VIRTUALIZACAO_PRIORITARIO**
- **LINGUAGEM_PROGRAMACAO** e respectivos campos de “OUTRO” e “PRIORITARIO”.
- **IDEs e Ferramentas de Desenvolvimento**
- **Controle de versão**
- **Ferramentas de configuração de recursos (Infra as Code)**
- **Ferramentas de CI/CD**
- **Metodologias de gestão**
- **Boas práticas de desenvolvimento**
- **Ferramentas de apoio metodológico**
- **Ferramentas de documentação**

Esses grupos são usados depois para gerar versões em formato longo de cada bloco de perguntas.

---

### Conversão para Formato Long / Tidy Data

Um ponto central do notebook é a aplicação de **`pandas.melt`** para converter os dados do survey do formato original (wide) para o formato long, também chamado de **tidy data** (conceito difundido por Hadley Wickham).

**Objetivo do tidy data no contexto do survey:**

- Ter **uma linha por combinação**:
  - Respondente (`ID`, `EMAIL`, `NAME`)
  - Tecnologia / categoria (por exemplo, um sistema operacional específico)
  - Tipo de resposta (uso, outro texto livre, prioridade)
- Facilitar:
  - Contagens, proporções, agrupamentos por tecnologia.
  - Cruzamentos com outras dimensões (departamento, tempo de casa, experiência, etc.).
  - Visualizações em ferramentas de BI e análises em ML.

#### Exemplo: Sistemas Operacionais

O notebook cria, a partir de `table4`, três dataframes principais para sistemas operacionais:

- **`df_so`**:
  - Usa `melt` sobre colunas como:
    - `WINDOWS_NT_SERVER`, `WINDOWS_1011`, `LINUX_DEBIAN_UBUNTU_MINT_KALI`, etc.
  - Mantém como identificadores (`id_vars`):
    - `ID`, `EMAIL`, `NAME`.
  - Gera colunas:
    - `SISTEMAS_OPERACIONAIS` (nome da tecnologia / SO).
    - `RESPOSTA_SISTEMAS_OPERACIONAIS` (resposta do tipo “Já usei”, “Uso atualmente”, “Me interesso em usar”, “Não tenho opinião / Não sei”, etc.).
  - Ajuste de categorias:
    - Valores como `OUTRO6` são mapeados para uma categoria mais amigável, como `OUTRO`.

- **`df_so_`**:
  - Foca na coluna de texto livre:
    - `SE_VOCE_APONTOU_TER_USADO_USAR_ATUALMENTE_OU_QUERER_USAR_OUTRO_SISTEMA_OPERACIONAL_ACIMA_POR_FAVOR_IDENTIFIQUE_QUAL_ABAIXO`.
  - Gera:
    - `SISTEMAS_OPERACIONAIS_APONTADOS`.
    - `RESPOSTA_SISTEMAS_OPERACIONAIS_APONTADOS` (conteúdo textual preenchido pelo respondente).

- **`df_so__`**:
  - Usa a coluna de prioridades:
    - `QUAIS_DOS_SEGUINTES_SISTEMAS_OPERACIONAIS_LHE_SAO_PRIORITARIOS`.
  - Gera:
    - `SISTEMAS_PRIORITARIOS`.
    - `RESPOSTA_SISTEMAS_PRIORITARIOS` (lista de sistemas considerados prioritários).

Esses três dataframes são combinados em um **dataframe final consolidado**:

- **`df_final`**:
  - Merge por `["ID", "EMAIL", "NAME"]`:
    - Junta as informações de uso (`df_so`), texto livre (`df_so_`) e prioridades (`df_so__`).
  - Resultado:
    - Uma tabela longa, com colunas:
      - Identificação do respondente.
      - Sistema operacional (coluna categórica).
      - Status de uso.
      - Campo de texto livre (caso tenha sido preenchido).
      - Lista de sistemas prioritários.

Esse padrão (definir grupos de colunas, aplicar `melt` e depois `merge`) é a base para ser replicado com outros blocos temáticos (virtualização, linguagens, ferramentas etc.).

---

### Comentário sobre Tidy Data

O notebook inclui uma nota explicando o contexto:

- **“Survey Long Format / Tidy Data”**
- Referência a Hadley Wickham.
- Reforço de que esse é o padrão adotado em:
  - Ciência de Dados
  - BI
  - Machine Learning
  - Survey Analytics

Ou seja, toda a transformação aqui está alinhada com boas práticas modernas para análise de dados de questionários.

---

### Possíveis Próximos Passos (a partir deste Notebook)

- **Generalizar as funções de melt**:
  - Criar funções reutilizáveis para aplicar o mesmo padrão em outros grupos (`VIRTUALIZACAO`, `LINGUAGEM_PROGRAMACAO`, etc.).
- **Salvar os resultados intermediários/finais**:
  - Exportar `df_final` (e equivalentes para outros grupos) em CSV/Parquet para uso em outras ferramentas (Power BI, dashboards, etc.).
- **Análises exploratórias**:
  - Contagens e proporções de uso por tecnologia.
  - Cruzamentos por departamento, faixa etária, tempo de casa, experiência com dados/programação.
- **Visualizações**:
  - Gráficos de barras, heatmaps, redes de co-uso de tecnologias, etc.

---

### Resumo

- O notebook **conecta ao banco SQLite** que contém os dados do survey.
- **Carrega as tabelas principais** de identificação e de stack tecnológico.
- **Estrutura grupos de colunas** por tipo de tecnologia.
- **Converte os dados para formato long/tidy** usando `pandas.melt`, com uma linha por respondente–tecnologia–tipo de resposta.
- **Produz dataframes consolidados** (como `df_final`) ideais para análises posteriores, BI e modelagem.

Este documento resume a lógica e o propósito do `script.ipynb` para facilitar seu entendimento, manutenção e extensão futura.