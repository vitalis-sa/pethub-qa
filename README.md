# PetHub: Compliance, Quality Assurance & Tests (Sprint 4)

Equipe **Vitalis** · Challenge FIAP 2026 · empresa parceira CLYVO VET

## Entrega

| Item | Link |
|---|---|
| Plano de testes manuais (Azure DevOps) | [Test Plans do projeto `Sprint 4 – Azure DevOps`](https://dev.azure.com/RM565154/Sprint%204%20%E2%80%93%20Azure%20DevOps/_testPlans) |
| Backlog com os PBIs testados (Azure Boards) | [Backlog do projeto `Sprint 4 – Azure DevOps`](https://dev.azure.com/RM565154/Sprint%204%20%E2%80%93%20Azure%20DevOps/_backlogs) |
| Vídeo da automação (configuração, execução e resultados) | _cole aqui o link do YouTube (não listado)_ |
| Coleção Postman da automação | [`automacao/PetHub-API.postman_collection.json`](automacao/PetHub-API.postman_collection.json) |

## Sistema sob teste

O back-end do PetHub são duas APIs REST, publicadas no Cloud Run:

| Serviço | Responsabilidade | URL |
|---|---|---|
| Vitalis (.NET) | Responsável, login, endereços, contatos, lembretes e gateway para o Java | https://pethub-dotnet.cloud.run |
| pethub-java (Spring) | Veterinário, pets, consultas, prontuário e IA | https://pethub-java.cloud.run |

O tutor usa o aplicativo móvel, que chama essas APIs. Como a automação valida as APIs, a ferramenta é o
**Postman**, a opção que o enunciado indica para sistemas compostos por APIs.

## Parte A: testes manuais

O plano está no Azure DevOps, organização `RM565154`, projeto `Sprint 4 – Azure DevOps`. São 64 *Test Cases*
agrupados em Test Plans por semana da release. Cada caso tem objetivo e pré-condições na descrição, passos com ação e
resultado esperado, parâmetros com os dados de entrada controlados e um link *Tests* para o PBI que valida.

## Parte B: automação (Postman)

8 casos automatizados, com 36 verificações (`pm.test`) no total. Cada caso usa dados controlados: nome, senha,
endereços e pet fixos, e e-mail e CPF válido gerados a cada execução, para a coleção rodar várias vezes sem limpar o banco.

| Teste | Test Case no Azure | O que valida |
|---|---|---|
| AT01 | sem caso no Azure | Cadastro do responsável devolve 201 com token e sem a senha; e-mail repetido devolve 409 |
| AT02 | 170 | Login válido devolve 200 e um JWT do responsável certo |
| AT03 | 174 | Senha errada devolve 401 sem token; rota protegida sem token devolve 401 |
| AT04 | 170 | O tutor vê só o próprio pet (Thor); pet de outro tutor devolve 404 |
| AT05 | 246 | Consulta em horário livre nasce `AGENDADA`; mesmo veterinário no mesmo horário devolve 409 |
| AT06 | 248 | Consulta com data no passado é recusada; consulta sem pet devolve 400 |
| AT07 | 183 | O tutor recebe 403 ao pedir a análise de IA, que é do veterinário; Java sem token devolve 401 |
| AT08 | 223 | Com 2 endereços, só o último marcado fica como principal |

A pasta `00 - Preparação` cria o veterinário e a unidade de teste. A pasta `99 - Limpeza` apaga o pet criado.
As respostas principais também conferem tempo abaixo de 5 s.

### Como executar no Postman

1. Abra o Postman e clique em *Import*. Escolha `automacao/PetHub-API.postman_collection.json`.
2. A coleção já aponta para as APIs no ar (`dotnetUrl` e `javaUrl`, na aba *Variables*). Para rodar local, troque as
   duas URLs.
3. Clique nos três pontos da coleção, depois em *Run collection*, e mantenha a ordem das pastas.
4. Clique em *Run PetHub - Automação de Testes (Sprint 4)*. O resultado esperado é 36 verificações aprovadas.

### Como executar pela linha de comando (Newman)

```bash
npx newman run automacao/PetHub-API.postman_collection.json
```

Última execução contra as APIs no ar, em 04/11/2026: 20 requisições, 36 verificações, 0 falhas.
