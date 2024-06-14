
## CI/CD
### Branches Overview

Este repositório utiliza workflows do GitHub Actions para construir e publicar imagens Docker. As workflows são definidas nos arquivos YAML localizados na pasta .github/workflows.

### Imagens Base

As imagens base são geradas a partir dos seguintes branches:

* 14.0_development_base_image
  * Gera imagens base para o ambiente de desenvolvimento.
* 14.0_staging_base_image
  * Gera imagens base para o ambiente de staging.
* 14.0_production_base_image
  * Gera imagens base para o ambiente de produção.

### Imagens Finais

As imagens finais são geradas a partir dos seguintes branches:

* 14.0_development
  * Gera a imagem final para o ambiente de desenvolvimento.
* 14.0_staging
  * Gera a imagem final para o ambiente de staging. 
* 14.0_production
  * Gera a imagem final para o ambiente de produção.