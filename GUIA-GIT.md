# Guia: do zero ao GitHub, só terminal

## PARTE 0 — Uma vez por máquina

```bash
# 1. Instalar as ferramentas
sudo apt install git gh

# 2. Assinar seus commits com sua identidade
git config --global user.name "Jonathan Ribeiro da Silva"
git config --global user.email "jonathanrds27@gmail.com"

# 3. Logar no GitHub (interativo: GitHub.com -> HTTPS -> Y -> web browser)
gh auth login

# Conferir tudo
git --version && gh --version && gh auth status
```

Feito isso, nunca mais. Vale para todos os projetos da máquina.

---

## PARTE 1 — Por projeto, do zero

### Passo 1 — Entrar na pasta

```bash
cd "/caminho/da/sua/pasta"
```

Aspas são obrigatórias se o caminho tiver **espaço ou acento**. Confirme onde está:

```bash
pwd     # mostra o caminho atual
ls -a   # lista tudo, inclusive ocultos
```

### Passo 2 — Criar o repositório local

```bash
git init
```

> `Initialized empty Git repository in .../.git/`

Nasce a pasta oculta `.git/`. **Ela é o repositório** — todo o histórico mora ali.
Apagou `.git/`, o histórico some (os arquivos ficam).

### Passo 3 — Criar o `.gitignore` ANTES de adicionar qualquer coisa

Essa é a ordem certa: defina o lixo primeiro, para ele nunca chegar a entrar no histórico.

**Forma recomendada — heredoc (várias linhas de uma vez):**

```bash
cat > .gitignore <<'EOF'
.venv/
__pycache__/
*.pyc
.vscode/
.env
EOF
```

Como funciona: `cat > arquivo` = "escreva no arquivo". `<<'EOF'` = "leia tudo até
encontrar uma linha só com `EOF`". Digite as linhas, e `EOF` sozinho na última fecha e grava.

**Forma alternativa — linha por linha:**

```bash
echo ".venv/" > .gitignore          # >  CRIA (apaga o que existia!)
echo "__pycache__/" >> .gitignore   # >> ACRESCENTA no final
echo "*.pyc" >> .gitignore
```

**ATENÇÃO: `>` sobrescreve o arquivo inteiro. `>>` acrescenta.**
Trocar os dois apaga tudo que estava lá.

**Forma com editor:**

```bash
nano .gitignore      # Ctrl+O grava - Enter confirma - Ctrl+X sai
```

**Sempre confira o que gravou:**

```bash
cat .gitignore          # mostra o conteúdo
cat -A .gitignore       # mostra invisíveis: "$" = fim de linha, "^M" = lixo do Windows
```

#### Sintaxe do `.gitignore`

| Escreva | Significa |
|---|---|
| `pasta/` | a barra no fim = é uma pasta |
| `*.pyc` | `*` é curinga: qualquer nome terminado em `.pyc` |
| `/build` | a barra no início = só na raiz do projeto, não em subpastas |
| `!importante.log` | `!` é exceção: ignora `*.log`, **menos** esse |
| `# comentário` | linha ignorada pelo Git |

#### Receitas prontas

```bash
# Python
cat > .gitignore <<'EOF'
.venv/
venv/
__pycache__/
*.pyc
.env
.vscode/
EOF
```

```bash
# Node
cat > .gitignore <<'EOF'
node_modules/
dist/
build/
.env
*.log
.vscode/
EOF
```

**A regra, em uma frase:** não versione o que dá para **recriar** (`.venv`,
`node_modules`, `build/`, cache) nem o que é **segredo** (`.env`, chaves, tokens).

> Segredo commitado fica no histórico **para sempre**, mesmo que você apague o
> arquivo depois. Por isso o `.gitignore` vem antes do primeiro `add`.

### Passo 4 — Ver o estado

```bash
git status
```

Tudo aparece como `??` (*untracked*): "vi o arquivo, mas ainda não cuido dele".
**O que estiver no `.gitignore` não aparece** — essa é a prova de que funcionou.

Quer saber qual regra barrou o quê?

```bash
git check-ignore -v .venv
# -> .gitignore:1:.venv/    .venv
```

### Passo 5 — Pôr no palco

```bash
git add -A        # tudo (novos, modificados e apagados)
git status        # os "??" viram "A", vermelho vira verde
```

Variações quando quiser escolher:

```bash
git add src/              # só uma pasta
git add main.py           # só um arquivo
git restore --staged x.py # tira do palco (não apaga o arquivo)
```

### Passo 6 — Nomear a branch como `main`

```bash
git branch -M main
git branch --show-current     # deve responder: main
```

O Git cria como `master`; o mundo usa `main`. Faça **antes** do commit, é indolor.

### Passo 7 — Commitar

```bash
git diff --cached                          # (opcional) revisa o que vai entrar. Sai com "q"
git commit -m "Primeiro commit: descrição do projeto"
git log --oneline --decorate
```

> `[main (root-commit) ee533e7] ...` + `19 files changed`

**Mensagem que presta:** imperativo ("adiciona X", não "adicionei"), diz o que
mudou, primeira linha curta.

Se esquecer o `-m`, o Git abre um editor. Se cair no `vim`: `:q!` + Enter para sair.

### Passo 8 — Criar o repo no GitHub e subir, em um comando

```bash
gh repo create NOME-DO-REPO --public --source=. --remote=origin --push
```

| Flag | Faz |
|---|---|
| `--public` | público (use `--private` para privado) |
| `--source=.` | conteúdo vem da pasta atual |
| `--remote=origin` | apelida o endereço do GitHub como `origin` |
| `--push` | já envia os commits |

**Digite a linha inteira antes do Enter.** Se apertar Enter no meio, o comando
roda pela metade (o `--push` fica de fora e o remoto nasce com nome errado).

### Passo 9 — Confirmar

```bash
git log --oneline --decorate
# TEM que aparecer: (HEAD -> main, origin/main)
```

`origin/main` ao lado de `main` = seu PC e o GitHub estão no mesmo commit.
**Esse é o sinal de sucesso.**

```bash
git remote -v     # mostra o endereço do origin
gh repo view      # vê o repo no terminal
gh browse         # abre no navegador
```

---

## PARTE 2 — A sequência inteira, para colar

```bash
cd "/caminho/do/projeto"

git init

cat > .gitignore <<'EOF'
.venv/
__pycache__/
*.pyc
.env
.vscode/
EOF

git status
git add -A
git branch -M main
git commit -m "Primeiro commit: descrição do projeto"

gh repo create NOME-DO-REPO --public --source=. --remote=origin --push

git log --oneline --decorate
```

---

## PARTE 3 — Depois disso, o dia a dia

```bash
git status                    # o que mudou?
git add -A                    # põe no palco
git commit -m "o que mudou"   # grava local
git push                      # sobe
```

Os passos 1 a 8 são **setup de uma vez só**. No mesmo projeto, nunca mais se repetem.

---

## PARTE 4 — Socorro

| Situação | Comando |
|---|---|
| Mensagem do commit ruim (**antes** do push) | `git commit --amend -m "nova"` |
| Desfazer último commit, mantendo arquivos | `git reset --soft HEAD~1` |
| Estraguei um arquivo, quero como estava | `git restore <arquivo>` |
| Tirar do palco sem perder | `git restore --staged <arquivo>` |
| O que mudou desde o commit? | `git diff` |
| Remoto com nome errado | `git remote rename antigo novo` |
| URL do remoto errada | `git remote set-url origin <url>` |
| Remoto sobrando | `git remote remove <nome>` |
| Repo com nome errado no GitHub | `gh repo rename <novo-nome>` |
| Esqueci de subir | `git push -u origin main` |
| Deu erro | leia a **primeira** linha, não a última |

**Sem volta fácil:** commitar segredo (fica no histórico) e `git push --force`
por cima do trabalho dos outros.
