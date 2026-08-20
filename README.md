# Interação Abelha-Planta

Repositório para processamento e análise de dados de interações entre abelhas e plantas.

![diagram-showing-pollination](docs/pictures/diagram-showing-pollination.png)

## Execução via CLI

Para ver detalhes do comando:

```bash
interacao-abelha-planta generate-images --help
```

Para gerar as imagens:

```bash
interacao-abelha-planta generate-images --filename "<caminho do arquivo>" --pages <numero de paginas> --group-by [abelha/flor] 
```

## Ideias de adição ao projeto

- [] Incluir interface para depósito de arquivos
- [] Incluir interface para seleção dos parâmetros do processamento
  - número de páginas
  - group-by (abelha ou flor)
- [] Botão de download dos arquivos (escolhendo o path de saída)
- Renderizar os gráficos na interface
