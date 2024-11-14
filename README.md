# SearchMapQgis

Este repositório contém um projeto de automação para visualização e manipulação de dados JSON, com foco na integração com o QGIS. O sistema é projetado para permitir o acesso e a análise de imagens de satélite utilizando APIs que oferecem catálogos baseados em JSON, incluindo coleções de imagens do Sentinel e do INPE.

Objetivo do Projeto
O objetivo principal deste projeto é facilitar o acesso e a análise de dados espaciais provenientes de satélites, utilizando formatos de dados JSON para comunicação com APIs. Este projeto busca otimizar processos de extração, visualização e manipulação dos dados no ambiente do QGIS, ideal para o Censipam que trabalham com dados geoespaciais.

Funcionalidades
Busca por Imagens:

O sistema permite buscar imagens de satélite de diferentes catálogos, filtrando por data de início e fim.
Exibe informações de nome e data de cada imagem disponível.
Suporte para realizar buscas por meio de uma API com padrão STAC.
Manipulação de Arquivos JSON:

Processa dados em formato JSON, incluindo leitura e extração de informações essenciais.
Adaptação fácil para diferentes catálogos de dados.
Integração com QGIS:

Interface desenvolvida para exibir as imagens no ambiente QGIS, suportando múltiplos catálogos.
Importação direta de arquivos .zip com dados das imagens para o QGIS, sem necessidade de extração manual.

Pré-Requisitos
QGIS (versão compatível com Qt5)
Python (>= versão 3.8)
Bibliotecas:
requests para requisições à API
json para manipulação de arquivos JSON
Outras: Instalar dependências adicionais listadas em requirements.txt.

Explicação sobre JSON
O projeto usa JSON para comunicação com a API e retorno dos dados, facilitando a manipulação de grandes volumes de dados. O JSON permite organizar as informações hierarquicamente, com cada imagem representada como um objeto que contém atributos como nome, data, e URL para download. Mais detalhes sobre como cada campo JSON é interpretado e manipulado estão documentados no módulo data_processor.py.
