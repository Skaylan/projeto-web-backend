## Iniciando


clone o projeto no reposítorio `https://github.com/Skaylan/projeto-web-backend`.

Após clonar o projeto, você vai precisar de um ambiente virtual para instalar as dependencias, para isso sera utilizado o Virtualenv:

```pip install virtualenv```

Certifique-se de estar na pasta raiz do projeto para executar:
```python -m venv venv```

Agora você deve ativar o ambiente virtual, mude para o diretorio /venv/Scripts/ e ative o ambiente:
```./activate```

Retorne para a raiz do projeto e execute:
```pip install -r requirements.txt```

Apos instalados as dependencias, você deve criar uma instancia do banco de dados na sua maquina local:

```flask db upgrade```

Agora pode rodar o projeto:
```python run.py```

## Mensagens de commit

[![Commitizen friendly](https://img.shields.io/badge/commitizen-friendly-brightgreen.svg)](http://commitizen.github.io/cz-cli/)
[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-yellow.svg)](https://conventionalcommits.org)

Sugerimos que as mensagens de commit sigam o padrão do _conventional commit_.

Para saber mais, acesse esses links:
- [Especificação do Conventional Commit](https://www.conventionalcommits.org/)
- [Regras do @commitlint/config-conventional](https://github.com/conventional-changelog/commitlint/tree/master/%40commitlint/config-conventional).

## Pull requests (PRs)

Independente da contribuição a ser feita (no código-fonte e/ou na documentação), operacionalmente falando, temos 2 formas de fazermos as *pull requests*: localmente, via linha de comando, usando o Git em conjunto com o Github, ou online, editando diretamente os arquivos no Github e solicitando uma pull request depois, tudo graficamente.

## Edição local do código

Consiste em realizar o *clone* do repositório raiz, realizar a alteração e solicitar o PR para o repositório raiz.

### Realizando PRs para o repositório raiz

- Faça um clone do respositório.
- Crie uma *branch* para *commitar* a sua *feature* ou correção: `git checkout -b my-branch`
- Faça o *commit* das mudanças: `git commit -m 'feat: My new feature'`
- Faça o *push* da sua *branch* para o *repositorio*: `git push origin my-branch`
- Vá para [Pull Requests](https://github.com/Skaylan/projeto-web-backend/pulls) do repositório raiz e crie um PR com o(s) seu(s) *commit(s)*

### Manter sua *branch* atualizada com o repositório raiz

- Apos seu *Pull Request* ter sido aprovado volte para o seu ambiente local e volta para a branch main.

`git checkout main `
- Atualize o seu repositório local a partir do remote do repositório raiz
`git pull`
- remova a branch anterior criada para realisar as alterações:
`git branch -d my-branch`