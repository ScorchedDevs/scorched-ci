[![SonarCloud](https://sonarcloud.io/images/project_badges/sonarcloud-black.svg)](https://sonarcloud.io/summary/new_code?id=ScorchedDevs_scorched-ci)

[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=ScorchedDevs_scorched-ci&metric=coverage)](https://sonarcloud.io/summary/new_code?id=ScorchedDevs_scorched-ci) 
[![Lines of Code](https://sonarcloud.io/api/project_badges/measure?project=ScorchedDevs_scorched-ci&metric=ncloc)](https://sonarcloud.io/summary/new_code?id=ScorchedDevs_scorched-ci)
[![Duplicated Lines (%)](https://sonarcloud.io/api/project_badges/measure?project=ScorchedDevs_scorched-ci&metric=duplicated_lines_density)](https://sonarcloud.io/summary/new_code?id=ScorchedDevs_scorched-ci)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=ScorchedDevs_scorched-ci&metric=bugs)](https://sonarcloud.io/summary/new_code?id=ScorchedDevs_scorched-ci)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=ScorchedDevs_scorched-ci&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=ScorchedDevs_scorched-ci)
[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=ScorchedDevs_scorched-ci&metric=vulnerabilities)](https://sonarcloud.io/summary/new_code?id=ScorchedDevs_scorched-ci)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=ScorchedDevs_scorched-ci&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=ScorchedDevs_scorched-ci)
# Scorched-CI
This project is going to automate your releases. When you add it as an github action to your projectit will automatically merge the develop branch into the main branch, then it will, calculate a new tag, create a new release and add the release description based on the CHANGELOG.md file.

# How to use
First you need create another branch, aside from main (or master) and set it to be your default branch. Our recommendation is to protect the main branch and never push to it, so its always on pair with the lastest branch.

After that you should set up the following files:

### CHANGELOG.md

```md
# Changelog

## New Features

 - N/A

## Enhancements

 - N/A

## Fixes

 - N/A

## Compatibility Breaker

 - N/A
```
Avoid using the "-" character when writing a topic. This should be placed on the root directory of your project.

### release.yml

```yml
name: Scorched-CI-Release
description: 'Automates releases with Major, Minor and Patch options'
on:
  workflow_dispatch:
    inputs:
      release:
        type: choice
        description: Release Type
        options: 
        - major
        - minor
        - patch

jobs:
  release:
    if: ${{ github.ref == 'refs/heads/develop' }}
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.10"]
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v3
      with:
        python-version: ${{ matrix.python-version }}
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements-dev.txt
    - name: Clonning last Scorched CI version
      run: |
        git clone https://github.com/ScorchedDevs/scorched-ci.git
        cd scorched-ci
        git fetch --tags
        latestTag=$(git describe --tags `git rev-list --tags --max-count=1`)
        git checkout $latestTag
    - name: Installing dependencies
      run: |
        cd scorched-ci
        pip install -r requirements.txt
    - name: Creating the release
      run: |
        cd scorched-ci
        python -c 'import main; main.release_${{ github.event.inputs.release }}()'
      env:
        REPO_NAME: ${{ github.repository }}
        TOKEN: ${{ secrets.TOKEN }}
```

You should create a secret named token with an access token from github
After that your projects will be released in the following pattern: vx-x-x (x being a incrementing number)

## Recomenda????es

Para editar esse projeto ?? recomendado que se use o sistema operacional linux, principalmente por ser um projeto que contempla a tecnologia Docker.

## Devcontainer

Esse projeto conta com a configura????o devcontainer do VSCode, por isso o melhor jeito de trabalhar nesse projeto ?? fazer o download do VSCode, instalar a exten????o  "remote containers" e, ao abrir o projeto, clicar em "reopen in container". Dessa forma todas as dependencias e exten????es utilizadas para trabalahr nesse projeto ser??o instaladas autom??ticamente.

## Como contribuir com o projeto?

Para contribuir com o projeto ?? interessante que se siga as seguintes regras:

### Issues

A issue deve ser criada quando algo for ser implementado no c??digo. Por exemplo, para criar um esquema de autentica????o de usu??rio para acessar nossa aplica????o. Criasse uma issue para implementar o loing, uma outra issue para implementar o logout, e uma issue para alterar a senha, por exemplo. Caso, para atingir um objetivo espec??fico, como nesse caso, criar um esquema de login, voc?? precise finalizar 3 ou mais issues, seria interessante que voc?? fizesse uma Milestone linkando todas as issues, assim fica mais f??cil de acompanhar quanto falta para que determindada funcionalidade seja implementada.

### Branches

Para criar uma branch que resolve um determinado issue, seria interessante que voc?? especifique se ?? uma feature nova ou um bugfix e ent??o indique qual a issue relacionada ?? branch. Ent??o deveriamos seguir o padr??o
"tipo/issue-xxx", como por exemplo: "feature/issue-001".

### Commits

Os commits tamb??m devem seguir um padr??o para facilitar a organiza????o d o trabalho em grupo. Ent??o os commits devem seguir o seguinte padr??o "#xxx - descri????o do commit" sendo xxx o n??mero da issue relacionada ao commit. Por exemplo: "#001 - Adicionando login de usu??rios".

### Changelog

O arquivo de changelog serve como base para os releases gerados automaticamente pelo CI. O padr??o ?? substituir o N/A (e adicioanr mais linhas se necess??rio) no campo que corresponde ao que foi feito no projeto com `[#xxx](https://github.com/ScorchedDevs/scorched-movies-backend/issues/xxx) e ent??o descrever aqui o que foi feito`

### PR (Pull Requests)

Para fazer um PR ?? interessante que ele esteja linkado a uma issue, ver a [documenta????o](https://docs.github.com/en/issues/tracking-your-work-with-issues/linking-a-pull-request-to-an-issue) para fechar as issues automaticamente com as PRs.

### Actions

Esse projeto conta com algumas github actions. Isso significa que o projeto tem algumas automa????es, como por exemplo, testar o lint e validar o projeto Django. Um PR s?? ser?? aceito, caso passe todas as etapas do GitHub actions.
